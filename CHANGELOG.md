# Changelog

## Illustrated submission report — 2026-11-12

- Added a 23-page PDF, editable Word document, standalone HTML and Markdown source.
- Included 15 actual screenshots and analytical figures covering the mission, specialist calculations, C02/C06/C13 results and conclusions.
- Added report evidence JSON and the validation-loss curve CSV; investment and evaluation logic are unchanged.

## Windows report-write fix — 2026-11-12

- Serialize in-process report writes and retry bounded Windows access/sharing violations during atomic replacement.
- Preserve the previous report and propagate permanent failures.
- Added transient/permanent-error regressions; retained the original concurrent-write test and Windows CI job.

## Palette update — 2026-11-12

- Changed the studio to charcoal surfaces, warm ivory text and gold accents.
- Matched interactive charts, exported SHAP plots and runtime screenshots to the new palette.
- Layout, workflow and numerical results remain unchanged.

## Submission candidate — 2026-11-11

### Added

- C13 explicit USD cost matrix, exact validation threshold selection, independent test confusion matrix, baseline policies and JSON evidence.
- Adversarial regressions for malformed inputs, caches, provider payloads, concurrent migrations and idempotent outcomes.
- Failure-injected real Streamlit flows, optional multi-viewport browser/axe runner, cross-platform check command, and constrained development dependencies.
- Actual runtime screenshots, QA evidence and licensing/attribution status.

### Changed

- Editorial dark studio with a prominent mandate action, lazy workspace navigation, direct C13 selection, accessible allocation strip, purposeful motion and reduced-motion support.
- Historical return display separated from the optimizer's ESG-adjusted objective.
- Exact 30/90-session offsets; corrupted/missing price caches fail closed.
- Finite capital/influence validation, reserved cash symbol, stronger ESG response shape validation, safe recoverable UI failures.
- Serialized SQLite migration/write transactions and duplicate-outcome protection for legacy schemas.
- Atomic report/provider-cache writes and non-destructive simulation database replacement.
- Local-only default binding, enabled XSRF/CORS, disabled telemetry and traceback display, constrained container install and sanitized source-only packaging.

### Removed

- Fake Streamlit smoke framework, obsolete static design specimen, stale release instructions and unused analyst/review prompts.
- Heavy boardroom donut rendering; the same weights now have a lightweight labeled allocation graphic and ledger.

### Known limits

- Synthetic benchmark validity, optional provider/RAG validation, shared single-operator storage, pending licensing, framework performance and unavailable browser coverage are explicitly triaged in QA_REPORT.md.
