# Run from the repository root: powershell -ExecutionPolicy Bypass -File .\scripts\prepare_demo.ps1
$ErrorActionPreference = "Stop"
if (!(Test-Path "requirements.txt")) { throw "Run from Verdant-Capital-Complete root" }
if (!(Test-Path ".venv")) { py -3.12 -m venv .venv }
$python = Join-Path (Get-Location) ".venv\Scripts\python.exe"
& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt
& $python -m pytest -q
& $python -m challenge.c02_rare_event
& $python -m challenge.c06_explainability
& $python -m data.feedback_backtest
& $python -m orchestrator.graph
Write-Host "Verdant demo evidence generated. Streamlit available at localhost:8501."
& $python -m streamlit run app.py
