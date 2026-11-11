"""Verdant Capital Studio — evidence-driven portfolio research workspace.

Start: streamlit run app.py. Visuals never determine allocation logic.
This application simulates investment decisions; it never executes trades.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

import config
from challenge.challenge_ui import render_challenge_sections
from data.feedback_store import recent_recommendations
from orchestrator.graph import _defaults, build_graph, run_pipeline
from ui.charts import allocation_donut, carbon_forecast_chart, feedback_chart, scenario_comparison
from ui.presentation import (
    agent_header, chip, clean_portfolio, decision_reason, get_dashboard_metrics,
    hero, money, percent, safe, section, stat,
)

st.set_page_config(
    page_title="Verdant Capital | Decision Intelligence", page_icon="🌿",
    layout="wide", initial_sidebar_state="auto",
    menu_items={"About": "Verdant Capital · research and investment simulation. Synthetic data is clearly labeled."},
)

# Read CSS from a bundled file so the entire application shares one visual language.
st.markdown("<style>" + (Path(__file__).parent / "ui" / "theme.css").read_text(encoding="utf-8") + "</style>",
            unsafe_allow_html=True)


def mark(html: str) -> None:
    """Render only HTML assembled from static markup and escaped values."""
    st.markdown(html, unsafe_allow_html=True)


def run_investment(inputs: dict):
    """Prefer genuine LangGraph orchestration; disclose an unavailable optional dependency."""
    try:
        return dict(build_graph().invoke(_defaults(inputs)), engine="LangGraph")
    except ImportError:
        st.warning("LangGraph is unavailable. Running the deterministic, documented fallback instead.")
        return dict(run_pipeline(inputs, persist=True), engine="Deterministic fallback")


def sidebar_controls() -> dict:
    with st.sidebar:
        mark('''<div class="vc-brand"><div class="vc-logo" aria-hidden="true">
        <svg viewBox="0 0 40 40" width="29" height="29" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round">
        <path d="M7 11 17 31 32 7"/><path d="M17 16 23 25"/><path d="M23 25 33 10"/>
        </svg></div><div><div class="vc-brand-name">Verdant <span style="color:#8CE1B6">Capital</span></div>
        <div class="vc-brand-sub">Decision Intelligence</div></div></div>''')
        mark('<div class="vc-sidebar-title">Investment mandate</div><div class="vc-sidebar-help">Configure a portfolio scenario and invite the three specialist agents to review it.</div>')
        mode_label = st.radio("Data environment", ["Fictional simulation", "Historical market cache"],
                              index=0, help="Simulation uses fictional assets. Historical mode requires cached prices and issuer reports.")
        mode = "demo" if mode_label.startswith("Fictional") else "market"
        if mode == "demo":
            mark('<div class="vc-note"><strong>SIMULATION</strong> · SOLR, WIND, and FOSS are fictional. Market history and ESG disclosures are generated for demonstration.</div>')
            choices = config.DEMO_CANDIDATES
        else:
            mark('<div class="vc-alertline">Historical data requires a local cache. Missing ESG evidence remains unverified.</div>')
            choices = config.DEFAULT_CANDIDATES
        st.divider()
        capital = st.number_input("Capital to allocate (USD)", min_value=0, max_value=100_000_000,
                                  value=100_000, step=10_000)
        risk = st.selectbox("Risk appetite", ["conservative", "moderate", "aggressive"], index=1,
                            format_func=lambda x: x.title())
        strict_esg = st.toggle("Enforce strict ESG limits", value=True,
                               help="Apply exclusion and exposure caps before capital allocation.")
        candidates = st.multiselect("Investment universe", choices, default=choices,
                                    help="Only these assets may receive noncash allocations.")
        event = "baseline"
        if mode == "demo":
            event = st.selectbox("Hypothetical stress event", ["baseline", "carbon_price_spike", "policy_tightening", "market_selloff"],
                                 format_func=lambda e: {"baseline":"Base case", "carbon_price_spike":"Carbon price shock",
                                                        "policy_tightening":"Policy tightening", "market_selloff":"Severe market drawdown"}.get(e,e))
        mandate = st.text_area("Investment principles", value="Favor verifiable sustainability claims, manage volatility and preserve capital under uncertainty.",
                               max_chars=600, height=105)
        pressed = st.button("Run investment review", type="primary", width="stretch")
        mark('<div class="vc-sidebar-tail">Independent evidence, constrained optimization, and an auditable final memo.<br><br>Not investment advice. No orders are sent to exchanges.</div>')
    return {"inputs": {"mode":mode, "candidates":candidates, "capital":capital, "risk_profile":risk,
                       "strict_esg":strict_esg, "query":mandate, "event":event}, "run":pressed}


def show_agent_cards(result: dict):
    votes = result.get("votes", [])
    esg = [v for v in votes if v["agent"] == "esg_verifier"]
    market = [v for v in votes if v["agent"] == "market_analyst"]
    metrics = result.get("portfolio_metrics", {})
    esg_verified = sum(v["payload"].get("verdict") == "credible" for v in esg)
    market_positive = sum(v["payload"].get("market_view") == "bullish" for v in market)
    summaries = [
        ("ESG Verifier", "Source-aware screening", "E", "Operational", f"{esg_verified} / {len(esg)}", "credible evidence profiles", "Documents are cited; missing verification stays unverified."),
        ("Market Analyst", "Risk and return signals", "M", "Operational", f"{market_positive} / {len(market)}", "positive market signals", "Historical trend and volatility inform the investment debate."),
        ("Portfolio Optimizer", "Constraint engine", "P", "Validated" if metrics.get("status")=="optimized" else "Risk controlled", "100%", "funding accounted for", "SciPy allocations enforce long-only, ESG limits and cash safety."),
    ]
    cols = st.columns(3, gap="medium")
    for col, (name,subtitle,letter,status,big,label,note) in zip(cols,summaries):
        with col:
            html = (f'<div class="vc-panel">{agent_header(name,subtitle,letter,status)}'
                    f'<div class="vc-agent-metric">{safe(big)} <span style="font-size:.74rem;font-weight:500;color:#A8BEB3">{safe(label)}</span></div>'
                    f'<div class="vc-agent-note">{safe(note)}</div></div>')
            mark(html)


def render_allocation(result: dict, preview: bool, inputs: dict):
    memo = result["final_memo"]
    view = get_dashboard_metrics(result)
    st.markdown(section("Allocation overview", "Mathematically constrained, evidence-informed capital deployment.", "Long-only · ESG screened"),unsafe_allow_html=True)
    cols = st.columns(4)
    cards = [
        stat("Mandate value", money(view["capital"]), "Capital available"),
        stat("Invested in assets", money(view["allocated"]), "After hard ESG constraints", "green"),
        stat("Cash protection", percent(view["cash_ratio"]), "Capital held uninvested", "gold"),
        stat("Conflicts reviewed", str(view["conflicts"]), "Documented ESG / market tensions"),
    ]
    for col, card in zip(cols,cards):
        with col: mark(card)
    left, right = st.columns([1.07,.93],gap="large")
    with left:
        st.markdown(section("Portfolio composition", "Validated weights; solver-level noise is suppressed in the view."),unsafe_allow_html=True)
        st.plotly_chart(allocation_donut(view["portfolio"]), width="stretch", config={"displayModeBar": False})
        mark('<div class="vc-panel-head">Allocation ledger</div>')
        items = sorted(view["portfolio"],key=lambda r:r["weight"],reverse=True)
        rows = "".join(f'<div class="vc-ledger"><div class="vc-ledger-symbol">{safe(r["ticker"])}</div>'
                       f'<div class="vc-ledger-track"><div class="vc-ledger-fill" style="width:{max(0,min(100,float(r["weight"])*100)):.2f}%"></div></div>'
                       f'<div class="vc-ledger-pct">{percent(r["weight"])}</div></div>' for r in items)
        mark('<div class="vc-panel">'+rows+'</div>')
    with right:
        st.markdown(section("Investment rationale", "What the optimizer accepted, constrained, or set aside."),unsafe_allow_html=True)
        metrics = memo.get("optimizer_metrics", {})
        a,b = st.columns(2)
        with a:
            mark(stat("Modeled annual return", f'{metrics["expected_return_pct"]:.2f}%' if metrics.get("expected_return_pct") is not None else "n/a", "Historical estimate, not guaranteed"))
        with b:
            mark(stat("Annualized volatility", f'{metrics["volatility_pct"]:.2f}%' if metrics.get("volatility_pct") is not None else "n/a", "Backward-looking risk estimate"))
        st.markdown("##### Policy review")
        for entry in memo.get("decision_audit", []):
            title,tone = decision_reason(entry.get("policy_reason", ""))
            weight = max(0.0,float(entry.get("weight") or 0))
            mark(f'<div class="vc-ledger"><div class="vc-ledger-symbol">{safe(entry.get("ticker", ""))}</div>'
                 f'<div style="flex:1">{chip(title,tone)}</div>'
                 f'<span class="vc-ledger-pct">{percent(weight)}</span></div>')
        st.caption("Policy codes and supporting citations are available in the Audit trail.")
        mark('<div class="vc-note"><strong>Allocation authority:</strong> Numerical weights come from the constrained optimizer, not from free-form model text. Cash remains available when an asset cannot meet the mandate.</div>')
    if inputs.get("mode") == "demo" and inputs.get("event") != "baseline":
        mark(section("What-if impact", "Base mandate versus the selected hypothetical event. No live orders are executed."))
        base_inputs = dict(inputs,event="baseline")
        base = run_pipeline(base_inputs, persist=False)
        baseline={entry["ticker"]:entry["weight"] for entry in base["final_memo"]["portfolio"]}
        st.plotly_chart(scenario_comparison(view["portfolio"],baseline),width="stretch",config={"displayModeBar":False})


def render_debate(result: dict):
    memo=result["final_memo"]
    mark(section("The decision room", "See the two analyses and the constraints that resolved them.", "Auditable judgments"))
    reviews=memo.get("evidence_review", [])
    if not reviews:
        st.info("No material disagreement was detected for these candidates and this policy.")
    else:
        for item in reviews:
            with st.expander(f"{item['ticker']}  ·  Market opportunity vs. sustainability policy",expanded=True):
                a,b=st.columns(2)
                with a:
                    mark('<div class="vc-panel-head">ESG perspective</div>')
                    st.write(item.get("esg_case",""))
                with b:
                    mark('<div class="vc-panel-head">Market perspective</div>')
                    st.write(item.get("market_case",""))
                st.markdown("**Resolution**")
                st.write(item.get("resolution",""))
                st.caption("Evidence references: " + "; ".join(item.get("citation",[])))
                st.caption(item.get("residual_uncertainty", ""))
    with st.expander("Explore each specialist's evidence and numerical signals"):
        agents=[("esg_verifier","ESG Verifier"),("market_analyst","Carbon & Market Analyst")]
        for agent_id, title in agents:
            st.markdown(f"**{title}**")
            for vote in result.get("votes",[]):
                if vote["agent"] != agent_id: continue
                p=vote["payload"]
                with st.expander(f"{vote['ticker']} · {p.get('verdict',p.get('market_view','unavailable')).replace('_',' ').title()} · {float(vote['confidence']):.0%} confidence"):
                    st.json(p)
    with st.expander("Portfolio constraints and optimizer diagnostics"):
        st.json(result.get("portfolio_metrics", {}))


def boardroom_tab(result: dict | None, inputs: dict, preview: bool):
    if not result:
        mark(section("Your boardroom is ready", "Select candidates, risk appetite and a data mode in the sidebar, then run the investment review."))
        st.info("The live market mode requires your local price cache; when inputs are missing, the optimizer retains capital in cash.")
        return
    memo=result["final_memo"]
    if preview:
        mark('<div class="vc-alertline"><strong>PREVIEW</strong> · This is a fictional scenario preview. Press <strong>Run investment review</strong> to create a tracked decision.</div>')
    elif memo.get("mode") == "demo":
        mark('<div class="vc-alertline"><strong>SYNTHETIC</strong> · Fictional issuers, generated ESG excerpts and hypothetical market data. This is not a real-world issuer assessment.</div>')
    elif result.get("market_snapshot",{}).get("source") == "unavailable":
        st.error("Market cache unavailable. Assets without usable prices are assigned zero exposure and retained as cash.")
    render_allocation(result,preview,inputs)
    mark(section("Specialist council", "Three distinct responsibilities; a single transparent investment memo."))
    show_agent_cards(result)
    render_debate(result)
    left,right=st.columns([1.25,.75])
    with left:
        mark('<div class="vc-note"><strong>Provenance:</strong> '+safe(result.get('market_snapshot',{}).get('source','Unavailable'))+'<br>LLM narratives do not override mathematical or ESG hard constraints.</div>')
    with right:
        st.download_button("Export complete decision audit", data=json.dumps(result,indent=2,default=str),
                           file_name="verdant_decision_audit.json",mime="application/json",width="stretch")


def markets_tab(result: dict | None):
    mark(section("Market intelligence", "Dated signals, transparent forecasts and feedback provenance.", "Market signals"))
    if result:
        snap=result.get("market_snapshot",{})
        stats=snap.get("stats", {})
        if stats:
            rows=[{"Asset":ticker,"Last price":v.get("last"),"30-day return %":v.get("return_30d_pct"),
                   "Annual volatility %":v.get("vol_annual_pct"),"90-day trend":v.get("trend_90d"),"As of":v.get("as_of")}
                  for ticker,v in stats.items() if isinstance(v,dict)]
            st.dataframe(pd.DataFrame(rows),width="stretch",hide_index=True)
            st.caption("Input provenance: " + str(snap.get("source","unknown")))
    summary=Path(config.DATA_DIR)/"carbon_summary.json"
    forecast=Path(config.DATA_DIR)/"carbon_forecast.csv"
    left,right=st.columns([1.32,.68],gap="large")
    with left:
        mark(section("Carbon-market proxy", "Forecast of a related ETF, not the spot carbon-credit market."))
        if summary.exists() and forecast.exists():
            try:
                d=json.loads(summary.read_text(encoding="utf-8"))
                frame=pd.read_csv(forecast)
                st.plotly_chart(carbon_forecast_chart(frame),width="stretch",config={"displayModeBar":False})
                st.caption(f"{d.get('ticker','KRBN')} · Data through {d.get('market_data_as_of','unknown')} · Holdout MAPE {d.get('backtest_mape_pct','n/a')}% · bands are not calibrated")
            except (OSError,ValueError,KeyError) as e:
                st.error(f"Forecast unavailable ({type(e).__name__}). Regenerate with `python -m data.carbon_forecast`.")
        else:
            st.info("Generate a dated market projection: `python -m data.fetch_market` then `python -m data.carbon_forecast`.")
    with right:
        mark(section("Why the carbon proxy matters", "A scenario input, not a price oracle."))
        mark('<div class="vc-panel"><div class="vc-panel-head">What the model measures</div><div class="vc-panel-desc">Historical returns of a carbon-related ETF and an indicative near-term projection. This can inform market context, but does not verify issuer ESG claims.</div></div>')
        mark('<div class="vc-note"><strong>Market integrity:</strong> Prices are historical. The application does not claim a streaming market feed or guaranteed future prices.</div>')
    mark(section("Feedback & memory", "Observe how simulated history affects agent influence without being confused with verified performance."))
    timeline=Path(config.DATA_DIR)/"feedback_timeline.json"
    if timeline.exists():
        data=json.loads(timeline.read_text(encoding="utf-8"))
        records=pd.DataFrame(data.get("days",[]))
        mark('<div class="vc-alertline">Simulation only · Agent success labels in this feedback chart are synthetically generated, not validated historical predictions.</div>')
        if not records.empty:
            st.plotly_chart(feedback_chart(records),width="stretch",config={"displayModeBar":False})
        st.caption(data.get("description",""))
    else:
        st.info("Generate the clearly labeled adaptive simulation: `python -m data.feedback_backtest`.")


def audit_tab(result: dict | None):
    mark(section("Decision audit trail", "A record that shows what the system knew, inferred and constrained.", "Read-only evidence"))
    mark('<div class="vc-note"><strong>Scope:</strong> Verdant Capital is research decision-support, not regulatory authorization, a lender, or a broker. A missing ESG document is not proof of wrongdoing. C02/C06/C13 are synthetic validation exercises.</div>')
    stored=recent_recommendations(limit=8)
    mark(section("Recommendation register", "Most recent recorded investment mandates."))
    if stored:
        st.dataframe(pd.DataFrame([{"Run":r["id"],"Timestamp (UTC)":r["ts"],"Mode":r["mode"],"Mandate":r["query"]} for r in stored]),
                     width="stretch",hide_index=True)
    else:
        st.info("No persisted decisions yet. Run an investment review to record your first audit entry.")
    if result:
        memo=result.get("final_memo",{})
        mark(section("Policy reason codes", "Every allocation and exclusion is labeled by an explicit policy result."))
        details=[]
        for item in memo.get("decision_audit",[]):
            details.append({"Asset":item.get("ticker"),"Reason code":item.get("policy_reason"),
                            "Weight %":round(100*float(item.get("weight",0)),2),
                            "ESG assessment":item.get("esg_verdict"),
                            "Evidence": "; ".join(item.get("citations",[])) or "Not applicable"})
        if details:
            st.dataframe(pd.DataFrame(details),hide_index=True,width="stretch")
        st.download_button("Download audit record (JSON)",json.dumps(result,indent=2,default=str),
                           file_name="verdant_audit.json",mime="application/json")
    mark(section("Research methodology", "Reproduce the evaluated outputs; inspect limitations."))
    with st.expander("Source truth, model limitations and commands",expanded=True):
        st.markdown("**Requirements traceability:** `docs/ARCHITECTURE.md` and `docs/CHALLENGE_EVALUATION.md`.")
        st.markdown("**Limitations:** `docs/LIMITATIONS.md` · Synthetic results are not production fraud-detection claims.")
        st.code("python -m pytest -q\npython -m challenge.c02_rare_event\npython -m challenge.c06_explainability\npython -m orchestrator.graph",language="bash")


control=sidebar_controls()
inputs=control["inputs"]
if control["run"]:
    with st.spinner("Reviewing evidence, market exposures and portfolio constraints..."):
        try:
            result=run_investment(inputs)
            st.session_state["boardroom_result"]=result
            st.session_state["boardroom_inputs"]=dict(inputs)
        except Exception as error:
            st.error(f"Review could not finish ({type(error).__name__}): {error}")

matching=st.session_state.get("boardroom_inputs")==inputs
result=st.session_state.get("boardroom_result") if matching else None
preview=False
if result is None and inputs["mode"]=="demo" and not control["run"]:
    try:
        result=run_pipeline(inputs,persist=False)
        preview=True
    except Exception:
        # The dashboard still loads if optional local dependencies are absent.
        result=None
mark(hero(mode=inputs["mode"],preview=preview,last_run=str(result.get("run_id","")) if result else ""))

board,lab,markets,audit=st.tabs(["Investment boardroom", "Risk lab · C02 / C06 / C13", "Market intelligence", "Audit trail"])
with board:
    boardroom_tab(result,inputs,preview)
with lab:
    render_challenge_sections(config.DATA_DIR)
with markets:
    markets_tab(result)
with audit:
    audit_tab(result)
mark('<div class="vc-footer"><span><b>Verdant Capital</b> · A Team Cypher research prototype</span><span>Evidence over assumption. Risk before return. · Not financial advice.</span></div>')
