import streamlit as st
import pandas as pd
import json
from pathlib import Path

from src.drosophila_model import DemoDrosophilaCellModel, generate_demo_rows

# Load CSS
css_path = Path(__file__).parent / "static" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(page_title="Drosophila Brain Cell AI - v4", layout="wide")


def metric_card(title: str, value: str, hint: str):
    return f"""
    <div class="metric-card">
      <div class="metric-title">{title}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-hint">{hint}</div>
    </div>
    """


def render_score_track(label: str, score: float, max_score: float) -> str:
    if max_score <= 0:
        pct = 0
    else:
        pct = max((score / max_score) * 100, 6)
    return f"""
    <div class="score-item">
      <div class="score-meta">
        <span>{label}</span>
        <span>{score:.3f}</span>
      </div>
      <div class="score-track">
        <div class="score-fill" style="width: {pct}%"></div>
      </div>
    </div>
    """


st.markdown(
    """
    <div class="main-header">
      <div>
        <div class="eyebrow">Prototype v4</div>
        <h1>Drosophila Brain Cell AI</h1>
      </div>
      <div class="header-tag">Minimal white UI</div>
    </div>
    """,
    unsafe_allow_html=True,
)

model = DemoDrosophilaCellModel()

with st.sidebar:
    st.header("Controls")
    st.button("Use demo rows", key="demo_rows")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    display_mode = st.selectbox("Display mode", ["Cards", "Table"])
    download_enabled = st.checkbox("Enable download", value=True)

rows = None
if st.session_state.get("demo_rows"):
    rows = generate_demo_rows()
    st.sidebar.success("Loaded demo rows")

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        rows = df.to_dict(orient="records")
        st.sidebar.success(f"Loaded {len(rows)} rows")
    except Exception as e:
        st.sidebar.error(f"Failed to parse CSV: {e}")
        rows = None

if rows is not None:
    results = model.predict_batch(rows)
    summary_df = pd.DataFrame(
        [
            {
                "cell_index": i + 1,
                "predicted_cell_type": r["predicted_cell_type"],
                "confidence": r["confidence"],
                **{f"score_{k}": v for k, v in r["scores"].items()},
            }
            for i, r in enumerate(results)
        ]
    )

    label_counts = pd.Series([r["predicted_cell_type"] for r in results]).value_counts()
    dominant_label = label_counts.idxmax() if not label_counts.empty else "—"
    avg_confidence = float(sum(r["confidence"] for r in results) / len(results)) if results else 0.0
    max_score = max(max(r["scores"].values()) for r in results) if results else 0.0

    col_a, col_b, col_c = st.columns(3)
    col_a.markdown(metric_card("Cells", str(len(results)), "Analyzed rows"), unsafe_allow_html=True)
    col_b.markdown(metric_card("Dominant type", str(dominant_label), "Most frequent label"), unsafe_allow_html=True)
    col_c.markdown(metric_card("Avg confidence", f"{avg_confidence:.3f}", "Across all cells"), unsafe_allow_html=True)

    st.markdown("---")

    if display_mode == "Table":
        st.subheader("Prediction table")
        st.dataframe(summary_df, use_container_width=True)
    else:
        st.subheader("Prediction cards")
        for chunk_start in range(0, len(results), 3):
            cols = st.columns(3)
            for offset in range(3):
                idx = chunk_start + offset
                if idx >= len(results):
                    break
                res = results[idx]
                col = cols[offset]
                scores_html = "".join(
                    render_score_track(k, v, max_score) for k, v in res["scores"].items()
                )
                card_html = f"""
                <div class="result-card">
                  <div class="result-head">
                    <div class="result-index">Cell {idx + 1}</div>
                  </div>
                  <div class="result-type">{res['predicted_cell_type']}</div>
                  <div class="result-confidence">Confidence: <strong>{res['confidence']}</strong></div>
                  <div class="score-list">{scores_html}</div>
                </div>
                """
                col.markdown(card_html, unsafe_allow_html=True)

    if download_enabled:
        st.markdown("---")
        json_payload = json.dumps({"results": results}, ensure_ascii=False, indent=2)
        col_json, col_csv = st.columns(2)
        col_json.download_button(
            label="Download JSON",
            data=json_payload.encode("utf-8"),
            file_name="v4_predictions.json",
            mime="application/json",
        )
        col_csv.download_button(
            label="Download CSV",
            data=summary_df.to_csv(index=False).encode("utf-8"),
            file_name="v4_summary.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.subheader("Detailed results")
    for i, res in enumerate(results):
        with st.expander(f"Cell {i + 1}: {res['predicted_cell_type']} — confidence {res['confidence']}"):
            st.json(res)

else:
    empty_box = """
    <div class="empty-box">
      <div class="empty-title">No dataset loaded</div>
      <div class="empty-copy">Click “Use demo rows” or upload a CSV file to start analysis.</div>
    </div>
    """
    st.markdown(empty_box, unsafe_allow_html=True)

    with st.sidebar:
        st.caption("Tip: upload genes as columns, such as TH, Gad1, VGlut, Or42a.")
