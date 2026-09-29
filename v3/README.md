# v3 - Advanced local prototype for Drosophila brain cell AI

This folder keeps the earlier v1 and v2 versions unchanged and adds a more advanced v3 prototype.

What is included in v3:
- Local notebook-style web interface
- CSV upload and demo dataset support
- Cell-type prediction with confidence scores
- JSON export for results
- Clear separation from previously published v1 and v2 versions

Run locally:

```bash
cd v3
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
streamlit run app.py
```

Notes:
- This is still a prototype and intentionally lightweight.
- It does not ship large model weights because GitHub repository size should remain manageable.
- To replace the demo logic with a real open model, edit `src/drosophila_model.py` and the load logic in `app.py`.
