# v2 - Web demo (Streamlit)

This folder contains a Streamlit-based web demo for the Drosophila Brain Cell AI (v2).

How to run

1. Create venv and install:

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run Streamlit app:

   streamlit run app.py

The web app allows you to:
- Use the built-in demo rows
- Upload a CSV expression matrix
- View prediction table
- Download prediction JSON

Notes
- This demo is intentionally lightweight and does not include heavy model weights.
- Replace src/drosophila_model.py with your own model adapter to use a real open model.
