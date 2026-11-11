"""View-model and safe presentation helpers; never change investment decisions."""
from __future__ import annotations

from html import escape
from typing import Any


def money(amount: float | int | None, compact: bool = False) -> str:
    """Format USD without obscuring small values or inventing market data."""
    value = float(amount or 0.0)
    if compact and abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}m"
    if compact and abs(value) >= 1000:
        return f"${value / 1000:,.1f}k"
    return f"${value:,.0f}"


def percent(value: float | int | None, digits: int = 1) -> str:
    return f"{float(value or 0) * 100:.{digits}f}%"


def clean_portfolio(rows: list[dict]) -> list[dict]:
    """Suppress solver-level numerical noise in the visual table only."""
    result = []
    for item in rows:
        if not isinstance(item, dict) or not item.get("ticker"):
            continue
        entry = dict(item)
        weight = float(item.get("weight") or 0)
        entry["weight"] = 0.0 if abs(weight) < 1e-8 else weight
        result.append(entry)
    return result


def get_dashboard_metrics(result: dict) -> dict[str, Any]:
    """Produce labels from an actual result; no fabricated totals."""
    memo = result.get("final_memo") or {}
    allocation = clean_portfolio(memo.get("portfolio") or [])
    weights = {p["ticker"]: p["weight"] for p in allocation}
    capital = float(memo.get("capital") or 0)
    conflicts = memo.get("conflicts") or []
    cash = float(weights.get("CASH", 0))
    metrics = memo.get("optimizer_metrics") or {}
    return {
        "capital": capital,
        "allocated": capital * max(0.0, min(1.0, 1.0 - cash)),
        "cash_ratio": cash,
        "cash_amount": capital * cash,
        "conflicts": len(conflicts),
        "return_estimate": metrics.get("expected_return_pct"),
        "volatility": metrics.get("volatility_pct"),
        "portfolio": allocation,
        "status": metrics.get("status", "unavailable"),
    }


def safe(text: Any) -> str:
    return escape(str(text), quote=True)


def chip(text: str, kind: str = "neutral") -> str:
    if kind not in {"neutral", "positive", "warning", "negative", "info"}:
        kind = "neutral"
    return f'<span class="vc-chip vc-chip--{kind}">{safe(text)}</span>'


def section(title: str, detail: str = "", aside: str = "") -> str:
    subtitle = f'<p class="vc-section-desc">{safe(detail)}</p>' if detail else ""
    aside_html = f'<span class="vc-section-aside">{safe(aside)}</span>' if aside else ""
    return (f'<div class="vc-section-top"><div><h2>{safe(title)}</h2>{subtitle}</div>'
            f'{aside_html}</div>')


def stat(label: str, value: str, note: str = "", tone: str = "") -> str:
    note_html = f'<div class="vc-stat-note">{safe(note)}</div>' if note else ''
    tone_name = tone if tone in {"green", "gold", "red"} else ""
    return (f'<div class="vc-stat"><div class="vc-stat-label">{safe(label)}</div>'
            f'<div class="vc-stat-value {"vc-" + tone_name if tone_name else ""}">{safe(value)}</div>'
            f'{note_html}</div>')


def hero(*, mode: str, preview: bool, last_run: str = "") -> str:
    demonstration = mode == "demo"
    provenance = "Fictional simulation" if demonstration else "Historical market cache"
    status = "Preview · not saved" if preview else ("Analysis complete" if last_run else "Ready for analysis")
    return f'''<section class="vc-hero" aria-label="Verdant Capital workspace introduction">
      <div class="vc-hero-main">
        <div class="vc-hero-topline"><span class="vc-presence"><i></i> Verdant intelligence</span><span class="vc-hero-rule"></span><span>{safe(provenance)}</span></div>
        <h1>Capital decisions,<br><em>made accountable.</em></h1>
        <p>Three specialists. One evidence-led investment mandate. Every allocation traced back to the signal that shaped it.</p>
        <div class="vc-hero-tags">{chip(status, 'positive' if not preview and last_run else 'info')}{chip('C02 · Rare-event stress')}{chip('C06 · Explainability')}</div>
      </div>
      <div class="vc-hero-aside">
        <div class="vc-aside-heading">Decision framework <span>03 SPECIALISTS</span></div>
        <div class="vc-aside-row"><span class="vc-aside-index">A</span><span>Verify sustainability</span><b>ESG</b></div>
        <div class="vc-aside-row"><span class="vc-aside-index">B</span><span>Read the market</span><b>RISK</b></div>
        <div class="vc-aside-row"><span class="vc-aside-index">C</span><span>Constrain allocation</span><b>OPT</b></div>
        <div class="vc-aside-foot">No automated trading. No unsupported certainty.</div>
      </div>
    </section>'''


def agent_header(title: str, subtitle: str, letter: str, status: str = "Operational") -> str:
    return (f'<div class="vc-agent-head"><div class="vc-agent-identity"><span class="vc-agent-symbol">{safe(letter)}</span>'
            f'<div><div class="vc-agent-name">{safe(title)}</div><div class="vc-agent-sub">{safe(subtitle)}</div></div></div>'
            f'<span class="vc-mini-status">{safe(status)}</span></div>')


def decision_reason(reason: str) -> tuple[str, str]:
    """Map documented policy codes to restrained UI labels."""
    mapping = {
        "ALLOCATED_CONSTRAINT_VALIDATED": ("Allocated", "positive"),
        "EXCLUDED_HIGH_ESG_RISK": ("Excluded", "negative"),
        "LIMITED_UNVERIFIED_ESG": ("Restricted", "warning"),
        "CASH_SAFETY_RESERVE": ("Cash reserve", "info"),
    }
    return mapping.get(str(reason), ("Review required", "neutral"))
