"""Transparent 30-day SIMULATION of adaptation. No real misconduct allegations.

Simulated accuracy is NOT a measured improvement on real finance outcomes.
Run: python -m data.feedback_backtest
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import config
from data.feedback_store import save_recommendation, record_outcome, agent_weights

DAYS = 30


def _real_returns(tickers, days=DAYS):
    """Historical returns, with explicit ticker headers; never treats Close as a column."""
    path = Path(config.DATA_DIR) / "prices.csv"
    if not path.exists():
        return {}
    try:
        frame = pd.read_csv(path, index_col=0, parse_dates=True)
    except (OSError, ValueError):
        return {}
    if isinstance(frame.columns, pd.MultiIndex) or "Ticker" in frame.index.astype(str):
        from data.fetch_market import load_cached_prices
        frame = load_cached_prices()
    output = {}
    for ticker in tickers:
        if ticker not in frame.columns:
            continue
        series = pd.to_numeric(frame[ticker], errors="coerce").dropna()
        if len(series) < days + 5 or not series.gt(0).all():
            continue
        # Compute truly observed forward return after the first observation.
        output[ticker] = float(series.iloc[days] / series.iloc[0] - 1)
    return output


def main():
    root = Path(config.DATA_DIR)
    root.mkdir(parents=True, exist_ok=True)
    # Separate, deliberately disposable demo DB; user feedback.db untouched.
    database = root / "simulation_feedback.db"
    if database.exists():
        database.unlink()
    rng = np.random.default_rng(42)
    timeline = []
    for day in range(1, DAYS + 1):
        rec_id = save_recommendation(f"Synthetic scenario day {day}",
                                     {"mode": "synthetic_demo", "day": day},
                                     db_path=database, mode="demo")
        for ticker in ("SOLR", "WIND", "FOSS"):
            for agent in ("esg_verifier", "market_analyst"):
                # Predetermined fictional skill differences, not measured market outcomes.
                skill = 0.78 if agent == "esg_verifier" else 0.62
                right = int(rng.random() < skill)
                record_outcome(rec_id, ticker, agent, "demo_classification", 0.0,
                               correct=right, db_path=database,
                               label_source="synthetic_demo", case_key=f"sim-{day}")
        weights = agent_weights(db_path=database, allowed_sources={"synthetic_demo"})
        timeline.append({"day": day, "esg_weight": weights["esg_verifier"],
                         "mkt_weight": weights["market_analyst"]})
    report = {"mode": "synthetic", "source": "seeded Bernoulli outcomes (not external truth)",
              "description": "Demonstrates feedback update mechanics, not real prediction accuracy.",
              "days": timeline}
    (root / "feedback_timeline.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"mode": report["mode"], "last_day": timeline[-1]}, indent=2))

if __name__ == "__main__":
    main()
