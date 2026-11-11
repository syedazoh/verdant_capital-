# Locally verified evaluation record — 11 November 2026

**Code source:** `challenge/c02_rare_event.py` and `challenge/c06_explainability.py`.
**Data source:** Completely **synthetic generated feature dataset**, not a
real issuer misconduct benchmark. This project does not make fraud allegations.

## C02 evaluation

- 99:1 held-out ratio: 4950 negatives and 50 positives per evaluation.
- PR-AUC mean: 0.9583, across 5 independent seeds.
- Average Precision mean: 0.9586 (random ranking baseline 0.0100).
- Precision mean: 0.9021; recall mean: 0.9040.
- First-seed confusion matrix: TP 47, FP 6, FN 3, TN 4944.
- Majority-class collapse: not observed in controlled tests.

## C06 attribution cases

Three separate held-out cases from the seed-7 detector; model-agnostic
permutation SHAP attributions reconstruct the exact anomaly score.

| Case | Prediction | Main attributed feature | File |
|---|---|---|---|
| true_positive | flag_for_review | `no_third_party_verif` | `c06_plots/c06_case_1.png` |
| false_positive | flag_for_review | `missing_baseline` | `c06_plots/c06_case_2.png` |
| false_negative | not_flagged | `missing_baseline` | `c06_plots/c06_case_3.png` |

## Local verification

```
python -m pytest -q
# 15 tests passed (unit/regression/evaluation); Streamlit and LangGraph server
# were not available in this isolated tool environment.
python -m challenge.c02_rare_event
python -m challenge.c06_explainability
python -m orchestrator.graph
```

The CLI `orchestrator.graph` was executed in labeled deterministic fallback
mode here because the `langgraph` dependency was not installed. Confirm real
LangGraph and Streamlit execution on the team's computer before submission.
