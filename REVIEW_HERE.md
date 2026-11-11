# Review this before replacing your repository files

This ZIP is a **complete project folder** built from the previous Verdant Capital full source release, with a redesigned Streamlit frontend. It is not a Git commit or pull request. Your GitHub branch is untouched.

## Highest-impact changes

- New `app.py`: fully rebuilt investment boardroom and supporting screens.
- New `ui/`: presentation helpers, chart styling and reusable CSS.
- New `.streamlit/config.toml`: matching native Streamlit theme.
- Updated `challenge/challenge_ui.py`: improved C02/C06 audit experience.
- Updated `challenge/c06_explainability.py`: matching downloadable dark-theme SHAP figures; the explained model and numerical logic are unchanged.
- New `assets/benchmark_snapshot/`: honestly labeled, precomputed synthetic benchmark evidence.
- New `tests/test_ui_presentation.py`, `tools/ui_smoke_test.py` and `docs/FRONTEND_HANDOFF.md`.
- New `docs/STUDIO_PREVIEW.html` and PNG screenshots: **static visual previews only**, not actual Streamlit runtime screenshots.

## Safe review path

1. Extract this ZIP outside your existing Git checkout.
2. Run the test/demo commands in `docs/FRONTEND_HANDOFF.md`.
3. Compare source files and merge into `zohtest` locally after checking. The ZIP does not contain `.git` or private keys.
4. Never copy an `.env` file or synthetic SQLite file into Git.

## Current readiness

The source has local regression tests and an isolated UI smoke check, but **full live Streamlit/browser verification is required on your Windows machine**. See `docs/FRONTEND_HANDOFF.md` for the exact checklist.
