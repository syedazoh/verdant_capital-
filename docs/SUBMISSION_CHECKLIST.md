# Submission-ready demonstration checklist

**Hackathon date:** November 11, 2026. **Branch to update manually:** `zohtest`.
No files were committed by ChatGPT.

- [ ] `python -m pytest -q` passes on the presentation computer.
- [ ] `python -m challenge.c02_rare_event` generates JSON and PR data.
- [ ] `python -m challenge.c06_explainability` produces three PNGs and audit JSON.
- [ ] `python -m data.feedback_backtest` produces a clearly synthetic timeline.
- [ ] `python -m orchestrator.graph` executes the demo; log whether it used LangGraph.
- [ ] Streamlit loads all four tabs without warnings or missing-key exceptions.
- [ ] Fictional issuer names and synthetic warnings are obvious.
- [ ] The conflict between FOSS's positive momentum and its fictional ESG risk is shown.
- [ ] Every portfolio allocates 100%, including cash, respects ESG exclusions and ticker universe.
- [ ] Changing a what-if event produces a new audit and evidence review.
- [ ] C02 exact 4,950 negatives and 50 positives confirmed at each test split.
- [ ] C06 explains exactly three held-out cases with SHAP score reconstruction.
- [ ] README describes mock/real inputs accurately and includes one-run commands.
- [ ] No real issuer is presented as fraudulent based on synthetic features.
- [ ] No .env, data_cache, SQLite database or personal documents included in Git commit.
- [ ] 4-minute offline demo recorded as backup.

## Suggested 4-minute presentation

- 0:00-0:35 — Problem and three-agent design
- 0:35-1:20 — Fictional mandate, evidence citations, market context
- 1:20-2:00 — Contradictory ESG/market signals and debate policy
- 2:00-2:35 — Actual constrained portfolio and hypothetical event reallocation
- 2:35-3:15 — C02 rare-event benchmark versus 99% majority-class accuracy trap
- 3:15-3:50 — Three C06 SHAP edge-case explanations and audit record
- 3:50-4:00 — Honest limitations, adaptive feedback simulation, closing
