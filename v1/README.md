# v1 - Command-line Drosophila Brain Cell Classifier

This folder contains a command-line version (v1) of the Drosophila Brain Cell AI demo. It is intended to be run locally on a workstation and shows how to load a CSV expression matrix, run a simple demo classifier (rule-based fallback) and save prediction outputs.

How to run

1. Create venv and install:

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run demo:

   python app.py --demo

3. Run with CSV input:

   python app.py --input data/example_cell_expression.csv

Notes
- This demo is intentionally lightweight and does not include heavy model weights.
- Replace src/drosophila_model.py with your own model adapter to use a real open model.
