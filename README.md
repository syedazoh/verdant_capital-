# 🌿 Verdant Capital — Decision Intelligence Studio

**Team Cypher hackathon MVP** · [Original repository](https://github.com/Fayaz-Ali56/Verdant-Capital/tree/zohtest)

Verdant Capital is an **auditable research and investment-decision simulator**. A
LangGraph boardroom coordinates **exactly three specialists**: (1) ESG Verifier,
(2) Carbon & Market Analyst, (3) Portfolio Optimizer. A persistence layer logs
recommendations. A separate, clearly labeled synthetic feedback simulation
illustrates how evaluation outcomes can modify future influence weights.

The **Risk Lab** solves the assigned challenge demonstrations:

- **C02 — Rare-event stress:** held-out 99:1 synthetic class split,
  PR-AUC, average precision, precision, recall, F1, confusion matrix,
  majority-class baseline, top-1% alert precision, five-seed repeatability.
- **C06 — Regulatory XAI:** three real held-out observations from the **same
  Isolation Forest** with permutation SHAP feature-attribution PNGs, audit JSON,
  model scores and checked additive reconstruction.

**Important:** The C02/C06 dataset is **synthetically generated**. The scores
are NOT validated fraud detection on real companies. Fictional demo issuers
`SOLR`, `WIND` and `FOSS` are not listed securities. The software neither
approves loans nor trades assets.

## New: redesigned research workspace

The Streamlit frontend has been rebuilt as a premium dark operational workspace with four focused views: **Investment boardroom**, **Risk Lab (C02/C06)**, **Market intelligence**, and **Audit trail**. It includes an instant *fictional preview*, transparent policy ledger, interactive charts, model explainability panels and downloadable audit reports. See [`DESIGN.md`](DESIGN.md) and [`docs/FRONTEND_HANDOFF.md`](docs/FRONTEND_HANDOFF.md).

A static (noninteractive) design specimen is at `docs/STUDIO_PREVIEW.html`; screenshots are also in `docs/`. They are not captures of the live Streamlit application. The Risk Lab includes an explicitly synthetic benchmark snapshot so its evaluation is visible on a fresh checkout.

## Quick start — Windows PowerShell

From the project folder with Python 3.11 or 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# All of these work without an LLM API key or market network:
python -m pytest -q
python -m challenge.c02_rare_event
python -m challenge.c06_explainability
python -m data.feedback_backtest
python -m orchestrator.graph
streamlit run app.py
```

Open `http://localhost:8501`. The default is **fictional demo mode**.
You can convene the boardroom, inspect evidence and conflicts, run a
**hypothetical** carbon-price shock, compare allocations, and visit the
**Risk Lab** tab to show the PR curve and three SHAP figures.

`python -m orchestrator.graph` uses LangGraph after installing requirements;
a *labeled* pure-Python execution path is available for isolated testing.

### Real market mode (optional)

```powershell
python -m data.fetch_market
python -m data.carbon_forecast
```

Market mode uses **dated locally cached prices** fetched by yfinance. It does
not claim streaming live market feeds. The carbon price input `KRBN` is an ETF
proxy, **not** the spot price of carbon allowances. If market data is missing,
assets are excluded from investment and the optimizer safely retains cash.

For issuer-scoped RAG, optionally install:

```powershell
python -m pip install -r requirements-rag.txt
```

Add PDFs as `data_cache/pdfs/TICKER__report.pdf` and then run:

```powershell
python -m data.build_rag
```

A user-uploaded ESG report is not independently verified or certified. RAG
retrieval returns filenames and **page citations**, filters by issuer, and does
not assert a numeric ESG rating without valid analysis. Optional LLMs require:

```powershell
python -m pip install -r requirements-llm.txt
Copy-Item .env.example .env
# Add keys to .env locally. Never commit that file.
```

Both `GEMINI_API_KEY` and `OPENROUTER_API_KEY` are optional. With no LLM,
market-mode ESG classifications remain **unverified**, rather than producing
false claims. The demo has **explicit synthetic fixture** assessments and never
uses real issuer accusations.

## Architecture

```text
Investment mandate / ESG policy / event scenario
                     │
         LangGraph state + provenance
                     │
       ┌─────────────┴───────────────┐
       ↓                             ↓
 ESG Verifier                  Carbon & Market Analyst
 Issuer-scoped RAG              Cached prices + KRBN proxy
 Company citations              Dated statistical signals
       └─────────────┬───────────────┘
                     ↓
       Genuine ESG-risk vs upside conflict?
                     ↓
       Evidence review (bounded at 1 round)
                     ↓
             Portfolio Optimizer
       SciPy constrained, long-only + CASH
                     ↓
      Deterministic validated allocation memo
                     ↓
       SQLite recommendation audit + evidence

External evaluation path:
 Synthetic disclosure features → IsolationForest
                             ├─ C02: held-out 99:1 PR testing
                             └─ C06: SHAP on three test cases

Outcome data (verified and dated only in market mode)
                  → smoothed agent weights
                  → next portfolio soft preferences
```

### Design rules

1. **Three specialists only.** Synthesis is deterministic, not a fourth agent.
2. **The LLM cannot invent allocation weights.** SciPy enforces full funding,
   max holdings, no shorts, ESG caps/exclusions, and cash fallback.
3. **No ESG evidence ≠ greenwashing.** With no authenticated citation or
   validated model response, classification is `unverified` and numerical ESG
   scores are `null`.
4. **No test leakage.** The C02 fit uses training observations without labels,
   and the held-out evaluation is used for metrics and SHAP cases only.
5. **Feedback provenance matters.** Synthetic feedback resides in a separate
   SQLite file and does not count as verified market performance.

## Reproduce the hackathon evidence

```powershell
python -m challenge.c02_rare_event
python -m challenge.c06_explainability
python -m pytest -q
```

Expected generated files (not committed by default):

- `data_cache/c02_report.json`
- `data_cache/c02_pr_curve.json`
- `data_cache/c06_report.json`
- `data_cache/c06_plots/c06_case_1.png`, `c06_case_2.png`, `c06_case_3.png`
- `data_cache/feedback_timeline.json`

The exact reported metrics are derived at runtime; **do not manually type
favorable numbers into the dashboard**.

## File map

| Path | Responsibility |
|---|---|
| `app.py` | Redesigned four-section Streamlit investment workspace |
| `orchestrator/graph.py` | LangGraph nodes, state channels, bounded review |
| `agents/` | Source-bound prompts and optional LLM provider fallback |
| `data/build_rag.py` | Issuer- and page-scoped PDF indexing and retrieval |
| `data/fetch_market.py` | yfinance normalization and market provenance |
| `data/carbon_forecast.py` | Dated KRBN ETF-proxy forecast and holdout |
| `data/portfolio.py` | Constrained SciPy optimizer and policy audit |
| `data/feedback_store.py` | SQLite audit and source-aware influence weights |
| `data/feedback_backtest.py` | Clearly synthetic 30-day feedback example |
| `challenge/c02_rare_event.py` | Reproducible rare-event performance evaluation |
| `challenge/c06_explainability.py` | Three SHAP edge-case reports and plots |
| `tests/` | Regression and acceptance tests |
| `docs/` | Architecture, requirements mapping, evidence and limitations |

## Deployment and final review

- Local: `streamlit run app.py`
- Docker: `docker build -t verdant-capital .` then
  `docker run -p 8501:8501 verdant-capital`
- Jenkins pipeline and GitHub Actions example are included for automated tests.
- **No AWS EC2, MongoDB Atlas, or real-time distributed event bus is claimed.**
  They were aspirations in the original proposal, not implemented capabilities.

Before submitting, run all tests, verify the dashboard on your machine,
inspect source citations, and record a short demo showing the three agents,
conflict review, optimizer, Risk Lab and provenance labels.

**Research prototype only.** Not investment, credit, or compliance advice.
