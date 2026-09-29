import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.drosophila_model import DemoDrosophilaCellModel, generate_demo_rows, load_csv_rows

st.set_page_config(page_title="Drosophila Brain Cell AI - v3", layout="wide")
st.title("Drosophila Brain Cell AI - v3")
st.caption("Versioned prototype series. v1 and v2 are preserved; this is the third iteration.")

model = DemoDrosophilaCellModel()

with st.sidebar:
    st.header("Options")
    use_demo = st.button("Load demo dataset")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    download_enabled = st.checkbox("Enable result download", value=True)

rows = None
if use_demo:
    rows = generate_demo_rows()
    st.success("Demo rows loaded.")

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        rows = df.to_dict(orient="records")
        st.success(f"Loaded {len(rows)} rows from uploaded file.")
    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")
        rows = None

if rows is not None:
    results = model.predict_batch(rows)

    summary_df = pd.DataFrame([
        {
            "cell_index": i,
            "predicted_cell_type": r["predicted_cell_type"],
            "confidence": r["confidence"],
            **{f"score_{k}": v for k, v in r["scores"].items()},
        }
        for i, r in enumerate(results)
    ])

    st.subheader("Prediction summary")
    st.dataframe(summary_df, use_container_width=True)

    if download_enabled:
        payload = json.dumps({"results": results}, ensure_ascii=False, indent=2)
        st.download_button(
            label="Download predictions as JSON",
            data=payload.encode("utf-8"),
            file_name="v3_predictions.json",
            mime="application/json",
        )

    st.subheader("Detailed per-cell output")
    for i, result in enumerate(results):
        with st.expander(f"Cell {i + 1}: {result['predicted_cell_type']}"):
            st.json(result)
else:
    st.info("Choose 'Load demo dataset' or upload a CSV to start.")

st.markdown("---")
st.markdown("This v3 version is designed to be a clean, upgradeable prototype for future real open-source fruit fly cell-model integration.")
