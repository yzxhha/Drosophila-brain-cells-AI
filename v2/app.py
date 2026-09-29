import streamlit as st
import pandas as pd
import json
from pathlib import Path
from v2_src.drosophila_model import DemoDrosophilaCellModel, generate_demo_rows, load_csv_rows

st.set_page_config(page_title="Drosophila Brain Cell AI (v2)", layout="centered")
st.title("Drosophila Brain Cell AI — Web demo (v2)")

st.markdown("Upload a CSV expression matrix with genes as columns. Or use the built-in demo.")

model = DemoDrosophilaCellModel()

use_demo = st.button("Use demo rows")
uploaded = st.file_uploader("Upload CSV", type=["csv"])

rows = None
if use_demo:
    rows = generate_demo_rows()
    st.success("Loaded demo rows")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    rows = df.to_dict(orient="records")
    st.success(f"Loaded {len(rows)} rows from uploaded CSV")

if rows is not None:
    results = model.predict_batch(rows)
    df_out = pd.DataFrame([{**r} for r in [{"predicted_cell_type": res["predicted_cell_type"], **{f"score_{k}": v for k, v in res["scores"].items()}, "confidence": res["confidence"]} for res in results]])
    st.dataframe(df_out)

    json_bytes = json.dumps({"results": results}, ensure_ascii=False, indent=2).encode("utf-8")
    st.download_button("Download predictions (JSON)", data=json_bytes, file_name="v2_predictions.json", mime="application/json")

    st.markdown("### Per-row breakdown")
    for i, res in enumerate(results):
        st.write(f"Row {i+1}: {res['predicted_cell_type']} (confidence={res['confidence']})")
        st.json(res)

else:
    st.info("No data yet. Upload a CSV or click 'Use demo rows'.")
