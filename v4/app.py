import streamlit as st
import pandas as pd
import json
from pathlib import Path
from typing import Optional

from src.drosophila_model import DemoDrosophilaCellModel, generate_demo_rows, load_csv_rows

# Load custom CSS
css_path = Path(__file__).parent / "static" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Drosophila Brain Cell AI - v4", layout="wide")
st.title("Drosophila Brain Cell AI — v4")
st.caption("Minimalist white UI — local prototype")

model = DemoDrosophilaCellModel()

with st.sidebar:
    st.header("Controls")
    use_demo = st.button("Use demo rows")
    uploaded = st.file_uploader("Upload CSV (genes as columns)", type=["csv"])
    display_mode = st.selectbox("Display mode", ["Cards", "Table"])
    download_enabled = st.checkbox("Enable download", value=True)

rows = None
if use_demo:
    rows = generate_demo_rows()
    st.sidebar.success("Loaded demo rows")

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        rows = df.to_dict(orient="records")
        st.sidebar.success(f"Loaded {len(rows)} rows from uploaded CSV")
    except Exception as e:
        st.sidebar.error(f"Failed to parse CSV: {e}")
        rows = None

if rows is not None:
    results = model.predict_batch(rows)

    # Build DataFrame summary
    summary_df = pd.DataFrame([
        {
            "cell_index": i + 1,
            "predicted_cell_type": r["predicted_cell_type"],
            "confidence": r["confidence"],
            **{f"score_{k}": v for k, v in r["scores"].items()},
        }
        for i, r in enumerate(results)
    ])

    if download_enabled:
        json_payload = json.dumps({"results": results}, ensure_ascii=False, indent=2)
        st.download_button(
            label="Download predictions (JSON)",
            data=json_payload.encode("utf-8"),
            file_name="v4_predictions.json",
            mime="application/json",
        )
        csv_payload = summary_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download summary (CSV)",
            data=csv_payload,
            file_name="v4_summary.csv",
            mime="text/csv",
        )

    st.subheader("Predictions")

    if display_mode == "Table":
        st.dataframe(summary_df, use_container_width=True)
    else:
        # Cards layout: 3 columns
        cols_per_row = 3
        for row_start in range(0, len(results), cols_per_row):
            cols = st.columns(cols_per_row)
            for i in range(cols_per_row):
                idx = row_start + i
                if idx >= len(results):
                    break
                res = results[idx]
                col = cols[i]
                # Render a simple card with minimal white style
                card_html = f"""
                <div class="card">
                  <div class="card-title">Cell {idx+1}</div>
                  <div class="card-type">{res['predicted_cell_type']}</div>
                  <div class="card-confidence">Confidence: <strong>{res['confidence']}</strong></div>
                  <div class="card-scores">
                    {''.join([f"<div class=\"score-row\"><span class=\"gene\">{k}</span><span class=\"val\">{v}</span></div>" for k, v in res['scores'].items()])}
                  </div>
                </div>
                """
                col.markdown(card_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Per-row details")
    for i, res in enumerate(results):
        with st.expander(f"Cell {i+1}: {res['predicted_cell_type']} (confidence={res['confidence']})"):
            st.json(res)

else:
    st.info("No data yet. Click 'Use demo rows' or upload a CSV to start.")
