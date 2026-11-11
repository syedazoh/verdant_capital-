"""C02 + C06 model assurance cockpit. Import safe outside Streamlit."""
from __future__ import annotations
import json
from pathlib import Path

from ui.presentation import section, stat, chip, safe
from ui.charts import precision_recall_curve, feature_attribution


SAMPLE_DIR = Path(__file__).resolve().parents[1] / "assets" / "benchmark_snapshot"


def _select_evidence_folder(data_dir: str | Path) -> tuple[Path, bool]:
    """Prefer freshly generated results; otherwise show clearly labeled bundled sample."""
    live = Path(data_dir)
    files = ["c02_report.json", "c02_pr_curve.json", "c06_report.json"]
    if all((live / path).exists() for path in files):
        return live, False
    if all((SAMPLE_DIR / path).exists() for path in files):
        return SAMPLE_DIR, True
    return live, False


def _confusion_html(trial: dict) -> str:
    tp, fp, fn, tn = (int(trial.get(n, 0)) for n in ["tp", "fp", "fn", "tn"])
    return f'''<div class="vc-confusion" role="group" aria-label="Held-out confusion matrix">
      <div class="vc-confusion-heading">Holdout predictions <span>Seed {int(trial['seed'])}</span></div>
      <div class="vc-matrix-grid">
        <div class="vc-matrix-item vc-matrix-tp"><strong>{tp:,}</strong><span>True positives</span></div>
        <div class="vc-matrix-item"><strong>{fp:,}</strong><span>False positives</span></div>
        <div class="vc-matrix-item"><strong>{fn:,}</strong><span>Missed positives</span></div>
        <div class="vc-matrix-item vc-matrix-tn"><strong>{tn:,}</strong><span>True negatives</span></div>
      </div>
      <div class="vc-matrix-caption">Actual label and model flag, held-out split. An error is shown, not hidden.</div>
    </div>'''


def render_challenge_sections(data_dir: str = "data_cache") -> None:
    import pandas as pd
    import streamlit as st

    root, bundled = _select_evidence_folder(data_dir)
    st.markdown(section("Model assurance", "Rare-event robustness and transparent, inspectable explanations.", "C02 / C06 evaluation"),unsafe_allow_html=True)
    st.markdown('<div class="vc-note"><strong>Controlled scientific benchmark.</strong> Model inputs and labels are <strong>synthetic ESG disclosure features</strong>. Numbers below are not validated greenwashing-detection accuracy on real issuers.</div>', unsafe_allow_html=True)
    if bundled:
        st.caption("Showing a bundled, reproducible synthetic benchmark snapshot. Run the evaluation scripts to generate results on this machine.")

    p_report, p_curve = root / "c02_report.json", root / "c02_pr_curve.json"
    if not (p_report.exists() and p_curve.exists()):
        st.info("Evaluation not generated. Run `python -m challenge.c02_rare_event` and `python -m challenge.c06_explainability`.")
        return
    try:
        report = json.loads(p_report.read_text(encoding="utf-8"))
        curve = json.loads(p_curve.read_text(encoding="utf-8"))
    except (OSError,ValueError) as err:
        st.error(f"Benchmark report could not be loaded: {type(err).__name__}. Re-run evaluation scripts.")
        return

    st.markdown(section("C02 — Rare-event stress", "A held-out 99:1 imbalance, scored beyond majority-class accuracy.", "Isolation Forest · Five seeds"),unsafe_allow_html=True)
    cards = [
        stat("Mean PR-AUC", f'{report.get("pr_auc_mean",0):.3f}', "Across independent seeds", "green"),
        stat("Average precision", f'{report.get("average_precision_mean",0):.3f}', "Ranking quality above 1% baseline"),
        stat("Recall at threshold", f'{report.get("recall_mean",0):.1%}', "Actual positives detected"),
        stat("Imbalance", f'{int(report.get("negative_count",0)):,}:{int(report.get("positive_count",0)):,}', "Held-out negatives : positives", "gold"),
    ]
    for col, html in zip(st.columns(4), cards):
        with col: st.markdown(html,unsafe_allow_html=True)
    left,right=st.columns([1.45,.9],gap="large")
    with left:
        st.markdown(section("Precision–recall profile", "The relevant comparison for a rare-event classification problem."),unsafe_allow_html=True)
        st.plotly_chart(precision_recall_curve(curve,float(report.get("positive_rate",0.01))),width="stretch",config={"displayModeBar":False})
        st.caption("Reference: the dotted line is approximately the 1% prevalence baseline for random ranking. PR-AUC is not classification accuracy.")
    with right:
        st.markdown(section("Evidence of detection", "Held-out classification at the documented operating threshold."),unsafe_allow_html=True)
        trial = (report.get("trials") or [{}])[0]
        if trial:
            st.markdown(_confusion_html(trial),unsafe_allow_html=True)
        if report.get("no_majority_collapse"):
            st.markdown('<div class="vc-note"><strong>Passed controlled collapse check.</strong> The model detected positive examples in every evaluated split.</div>',unsafe_allow_html=True)
        else:
            st.error("At least one split failed the collapse check. Review the saved per-seed results.")
    with st.expander("Inspect methodology and per-seed model metrics"):
        st.write(report.get("methodology",""))
        st.dataframe(pd.DataFrame(report.get("trials", [])),width="stretch",hide_index=True)
        st.download_button("Download C02 evaluation JSON",p_report.read_text(encoding="utf-8"),"c02_evaluation.json",mime="application/json")

    st.markdown(section("C06 — Explainability audit", "Three actual held-out cases from the same C02 model, with feature contributions.", "Permutation SHAP"),unsafe_allow_html=True)
    p_c06=root / "c06_report.json"
    if not p_c06.exists():
        st.info("Run `python -m challenge.c06_explainability` to generate SHAP feature-attribution reports.")
        return
    try:
        c06 = json.loads(p_c06.read_text(encoding="utf-8"))
    except (OSError,ValueError):
        st.error("C06 report could not be read. Regenerate it with `python -m challenge.c06_explainability`.")
        return
    records = c06.get("cases",[])
    if not records:
        st.warning("No explainable cases are present in the C06 audit report.")
        return
    summary_cards=[]
    for record in records[:3]:
        case_name=record.get("case_type","unknown").replace("_"," ").title()
        label="Flagged" if record.get("predicted_label")==1 else "Not flagged"
        summary_cards.append((case_name,label,record))
    for col,(name,label,record) in zip(st.columns(3),summary_cards):
        with col:
            tone = "positive" if record.get("case_type")=="true_positive" else "warning"
            st.markdown(f'<div class="vc-case"><div class="vc-case-head"><div class="vc-case-name">{safe(name)}</div>{chip(label,tone)}</div>'
                        f'<div class="vc-case-meta">Observed label: {"positive" if record.get("true_label") else "negative"}<br>Score: {float(record.get("anomaly_score",0)):+.4f} · Cutoff: {float(record.get("decision_threshold",0)):+.4f}</div></div>', unsafe_allow_html=True)
    tabs=st.tabs([r.get("case_type","Case").replace("_"," ").title() for r in records[:3]])
    for case_tab, record in zip(tabs, records[:3]):
        with case_tab:
            left,right=st.columns([1.45,.65],gap="large")
            with left:
                st.markdown(section("Feature contribution", "Positive bars increase the anomaly score; negative bars reduce it."),unsafe_allow_html=True)
                st.plotly_chart(feature_attribution(record),width="stretch",config={"displayModeBar":False})
            with right:
                st.markdown(section("Decision record", "The numerical decision and its limitations."),unsafe_allow_html=True)
                st.metric("Model anomaly score", f'{float(record.get("anomaly_score",0)):+.4f}')
                st.metric("Decision threshold",f'{float(record.get("decision_threshold",0)):+.4f}')
                top=(record.get("attributions") or [{}])[0]
                st.markdown(f'**Dominant influence**  \n{top.get("feature","unknown").replace("_"," ").title()}')
                st.caption("This is a model attribution, not a causal explanation of fraud or regulatory approval.")
                if record.get("case_type","").startswith("borderline_substitute"):
                    st.warning("No example of the requested error occurred; this is a disclosed real borderline substitute.")
                path=root / "c06_plots" / record.get("plot","")
                if path.is_file():
                    st.download_button("Export attribution PNG",path.read_bytes(),file_name=path.name,mime="image/png",key=f'c06_download_{record.get("case_id",0)}')
            with st.expander("Feature values and additive reconstruction"):
                st.dataframe(pd.DataFrame(record.get("attributions",[])),hide_index=True,width="stretch")
                st.write("Baseline + SHAP sum = reconstructed score; numerical consistency checked by the C06 pipeline.")
                st.json({key:record.get(key) for key in ["base_score","reconstructed_score","anomaly_score","feature_values","eval_index"]})
    st.caption("SHAP identifies contributors to the Isolation Forest anomaly score; it does not prove a company is fraudulent, establish causality, or provide a calibrated fraud probability.")
    st.download_button("Download complete C06 audit (JSON)",p_c06.read_text(encoding="utf-8"),"c06_shap_audit.json",mime="application/json")
