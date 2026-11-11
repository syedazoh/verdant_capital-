"""Market price ingestion, controlled real/synthetic data provenance."""
import json
from pathlib import Path
import pandas as pd
import numpy as np
import config
from data.demo import price_frame


def normalize_download(data, tickers):
    """Support recent yfinance single- and multi-ticker MultiIndex layouts."""
    requested = [t.upper() for t in tickers]
    if data is None or data.empty:
        raise ValueError("The market-data provider returned no prices")
    if isinstance(data.columns, pd.MultiIndex):
        if "Close" in data.columns.get_level_values(0):
            close = data["Close"]
        elif "Close" in data.columns.get_level_values(1):
            close = data.xs("Close", axis=1, level=1)
        else:
            raise ValueError("Market response does not include Close prices")
    elif "Close" in data.columns and len(requested) == 1:
        close = data[["Close"]].rename(columns={"Close": requested[0]})
    else:
        close = data.copy()  # already flattened ticker columns
    if isinstance(close, pd.Series):
        close = close.to_frame(name=requested[0])
    close.columns = [str(t).upper() for t in close.columns]
    found = [t for t in requested if t in close.columns]
    if not found:
        raise ValueError("No requested ticker has a valid Close series")
    frame = close[found].apply(pd.to_numeric, errors="coerce").sort_index()
    return frame.dropna(how="all")


def fetch(tickers, period="1y"):
    import yfinance as yf
    tickers = list(dict.fromkeys(t.upper() for t in tickers))
    data = yf.download(tickers, period=period, auto_adjust=True,
                       progress=False, group_by="column", threads=False)
    return normalize_download(data, tickers)


def price_stats(frame: pd.DataFrame) -> dict:
    out = {}
    for ticker in frame.columns:
        s = pd.to_numeric(frame[ticker], errors="coerce").dropna()
        if len(s) < 3 or not s.gt(0).all():
            continue
        returns = s.pct_change().dropna()
        trend = "insufficient_history" if len(s) < 90 else ("up" if s.iloc[-1] > s.iloc[-90] else "down")
        out[str(ticker)] = {
            "last": round(float(s.iloc[-1]), 4),
            "return_30d_pct": (round(float((s.iloc[-1] / s.iloc[-30] - 1) * 100), 3)
                               if len(s) >= 30 else None),
            "vol_annual_pct": round(float(returns.std() * (252 ** .5) * 100), 3),
            "trend_90d": trend, "observations": int(len(s)),
            "as_of": str(pd.Timestamp(s.index[-1]).date()) if hasattr(s.index[-1], "date") else str(s.index[-1]),
        }
    return out


def load_cached_prices():
    path = Path(config.DATA_DIR) / "prices.csv"
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path, index_col=0, parse_dates=True)
    # Backward compatibility if a user saved yfinance's two-row header CSV.
    if "Ticker" in frame.index.astype(str) or "Date" in frame.index.astype(str):
        try:
            frame = pd.read_csv(path, header=[0, 1], index_col=0, parse_dates=True)
            frame = normalize_download(frame, list(config.DEFAULT_CANDIDATES) + [config.CARBON_TICKER])
        except (ValueError, KeyError):
            return pd.DataFrame()
    frame.columns = [str(t).upper() for t in frame.columns]
    return frame.apply(pd.to_numeric, errors="coerce").sort_index()


def main(mode="market"):
    tickers = list(config.DEFAULT_CANDIDATES) + [config.CARBON_TICKER]
    if mode == "demo":
        prices = price_frame(config.DEMO_CANDIDATES)
        source = "SYNTHETIC deterministic price generator"
    else:
        prices = fetch(tickers)
        source = "Yahoo Finance via yfinance (historical adjusted closes)"
    dest = Path(config.DATA_DIR)
    dest.mkdir(parents=True, exist_ok=True)
    filename = "demo_prices.csv" if mode == "demo" else "prices.csv"
    prices.to_csv(dest / filename)
    (dest / ("demo_price_stats.json" if mode == "demo" else "price_stats.json")).write_text(
        json.dumps({"mode": mode, "source": source, "tickers": price_stats(prices)}, indent=2),
        encoding="utf-8")
    print(f"Saved {filename} ({len(prices)} observations), {source}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["market", "demo"], default="market")
    main(parser.parse_args().mode)
