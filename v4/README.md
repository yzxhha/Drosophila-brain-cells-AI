# v4 — Minimalist Streamlit UI

This folder contains a v4 Streamlit prototype with a clean white minimalist interface (no logo).

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run v4/app.py
```

Features
- Upload CSV or use built-in demo rows
- Card-based or table display
- Download predictions (JSON / CSV)
- Minimalist white UI with rounded cards and subtle shadows

This v4 reuses the core model in `src/drosophila_model.py` (DemoDrosophilaCellModel).
