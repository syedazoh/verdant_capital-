# Verdant Capital — Frontend Release Handoff

## Changes in this release

**Replaced the previous plain four-tab Streamlit app** with an institutional research interface, without changing the three-agent backend contracts or committing to GitHub.

- Sidebar: branded SVG wordmark, explicit data environment, capital, risk, candidate universe, strict ESG policy, fictional stress events and mandate input.
- Boardroom: first-load fictional **preview** (no writes), investment scorecards, interactive allocation donut, policy ledger, historical risk estimates, specialist council, disagreement review, event comparison and JSON export.
- Risk Lab: 99:1 C02 KPI summary, interactive PR curve, honest confusion matrix, per-seed table, three case-selection tabs with interactive C06 SHAP charts, model score and available downloadable PNGs.
- Market intelligence: source-labeled price table, carbon-related ETF forecast, synthetic feedback timeline.
- Audit: latest recorded recommendations, decision reason codes, evidence attribution, audit JSON download.
- Accessibility: reduced motion, mobile reflow, explicit status text (not color-only), focus outlines, native widgets, no remote assets.

## How to run on Windows

In PowerShell, from this folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m challenge.c02_rare_event
python -m challenge.c06_explainability
streamlit run app.py
```

Open `http://localhost:8501`.

The *Investment boardroom* tab shows a fictional preview immediately. Choose the data environment in the sidebar, configure a mandate, and click **Run investment review** to persist a reviewed decision. Switch the stress-event menu and rerun to show asset-to-cash reallocation.

The *Risk Lab* contains a **bundled synthetic benchmark snapshot** so judges can inspect example figures on a fresh checkout. Re-running the C02/C06 scripts generates and displays fresh outputs from the same model in `data_cache`. Bundled plots are real outputs of the synthetic test harness, not independently validated real-issuer results.

## Demo script (~4 minutes)

1. **30s — Problem and policy:** the original finance workflow struggles with fragmented ESG evidence and greenwashing. Show strict ESG policy and three specialists.
2. **75s — Investment boardroom:** run the fictional default mandate; explain allocation, cash reserve and reason codes. Use the FOSS conflict to show that market upside cannot override sustainability policy.
3. **45s — Event simulation:** select a fictional severe market drawdown and re-run. Show baseline vs event allocations without suggesting real automated trading.
4. **60s — Risk Lab C02:** the 99:1 evaluation and 1% baseline; explain why accuracy is insufficient. Cite held-out confusion matrix and repeated splits.
5. **45s — Risk Lab C06:** compare true positive, false positive and false negative on the same synthetic model, including feature contributions.
6. **25s — Audit:** show reason codes, JSON download, explicit limitations and reproducible test commands.

## Important limits

- Full Streamlit browser interaction could **not** be executed in the creation environment because Streamlit could not be installed offline. The code was Python-compiled, the source tests passed, and the UI was exercised with a local component stub. Check the live UI on Windows before submitting.
- UI screenshots in `docs/` are generated from a **static visual specimen**, not captures from Streamlit.
- Do not claim C02/C06 demonstrate production greenwashing detection; the training and evaluation features are synthetic.
- Deploy only after validating local dependencies and keeping `.env` keys outside the repository.

## Review checklist

- [ ] Confirm Windows Streamlit loads each of the four sections.
- [ ] Run a new fictional boardroom decision; ensure portfolio total equals 100%.
- [ ] Switch to hypothetical severe market drawdown; compare allocation to baseline.
- [ ] Inspect both C02/C06 after regenerating local data.
- [ ] Confirm `data_cache/c06_plots/` exports three PNGs.
- [ ] Confirm audit JSON downloads and contains documented reason codes.
- [ ] Review small/mobile widths using browser device emulation.
- [ ] Commit only the files you approve to the `zohtest` branch.
