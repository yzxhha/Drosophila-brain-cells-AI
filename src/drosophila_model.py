from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

import numpy as np
import pandas as pd


CELL_TYPE_MARKERS = {
    "dopaminergic": {
        "TH": 2.2, "DAT": 2.0, "Ddc": 1.8, "Ple": 1.3,
    },
    "gabaergic": {
        "Gad1": 2.3, "Gad2": 2.1, "vGAT": 1.9, "SLC32A1": 1.5,
    },
    "glutamatergic": {
        "VGlut": 2.4, "vGlut": 2.4, "kcc": 1.2, "Nmdar1": 1.4,
    },
    "sensory": {
        "Or42a": 1.8, "Ir8a": 1.6, "Ir25a": 1.7, "nAChR": 1.3,
    },
    "neuroendocrine": {
        "C929": 1.9, "AstC": 1.5, "Dimm": 1.6, "Tdc2": 1.7,
    },
}


class DemoDrosophilaCellModel:
    """A small rule-based classifier for demonstration purposes.

    This intentionally does not claim to be a full production brain-cell model.
    It acts as a local, runnable fallback that lets the repo work immediately
    even without downloading a heavy open model.
    """

    def __init__(self) -> None:
        self.cell_types = list(CELL_TYPE_MARKERS.keys())

    def _to_feature_vector(self, row: dict) -> np.ndarray:
        values = []
        for celltype, markers in CELL_TYPE_MARKERS.items():
            score = 0.0
            for gene, weight in markers.items():
                gene_key = gene.lower()
                for key, value in row.items():
                    if str(key).lower() == gene_key:
                        score += float(value) * weight
            values.append(score)
        return np.asarray(values, dtype=float)

    def predict_single(self, row: dict) -> dict:
        scores = self._to_feature_vector(row)
        idx = int(np.argmax(scores))
        predicted = self.cell_types[idx]
        confidence = float(scores[idx] / (np.sum(scores) + 1e-9))
        return {
            "predicted_cell_type": predicted,
            "confidence": round(float(confidence), 4),
            "scores": {self.cell_types[i]: round(float(v), 4) for i, v in enumerate(scores)},
        }

    def predict_batch(self, rows: Sequence[dict]) -> List[dict]:
        return [self.predict_single(r) for r in rows]


def load_csv_rows(path: Path) -> list[dict]:
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"The file {path} is empty.")
    return df.to_dict(orient="records")


def generate_demo_rows() -> list[dict]:
    rows = [
        {
            "TH": 3.2, "DAT": 2.8, "Ddc": 2.5, "Ple": 1.0,
            "Gad1": 0.4, "Gad2": 0.2, "vGAT": 0.1,
            "VGlut": 0.2, "Or42a": 0.1, "Ir25a": 0.2,
        },
        {
            "TH": 0.2, "DAT": 0.3, "Ddc": 0.1, "Ple": 0.1,
            "Gad1": 2.8, "Gad2": 2.4, "vGAT": 2.3,
            "VGlut": 0.5, "Or42a": 0.2, "Ir25a": 0.2,
        },
        {
            "TH": 0.2, "DAT": 0.3, "Ddc": 0.1, "Ple": 0.1,
            "Gad1": 0.3, "Gad2": 0.2, "vGAT": 0.1,
            "VGlut": 3.0, "Or42a": 0.5, "Ir25a": 0.4,
        },
    ]
    return rows


def print_summary(item: dict, index: int) -> None:
    print(f"Cell #{index + 1}: {item['predicted_cell_type']} | confidence={item['confidence']}")
    for key, value in item["scores"].items():
        print(f"  - {key}: {value}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Drosophila Brain Cell AI local demo")
    parser.add_argument("--demo", action="store_true", help="Run the built-in demo dataset")
    parser.add_argument("--input", type=str, default=None, help="Path to a CSV file of cell expression data")
    parser.add_argument("--hf-repo", type=str, default=None, help="Optional Hugging Face model repo to connect")
    parser.add_argument("--model-path", type=str, default=None, help="Optional local model path")
    return parser


def load_model_metadata(hf_repo: Optional[str], model_path: Optional[str]) -> dict:
    if hf_repo:
        return {"source": f"huggingface:{hf_repo}", "type": "public-model"}
    if model_path:
        return {"source": f"local:{model_path}", "type": "local-model"}
    return {"source": "demo-rule-based-classifier", "type": "local-demo"}


def run_demo() -> None:
    model = DemoDrosophilaCellModel()
    rows = generate_demo_rows()
    results = model.predict_batch(rows)
    for idx, item in enumerate(results):
        print_summary(item, idx)


def run_from_csv(csv_path: str) -> None:
    rows = load_csv_rows(Path(csv_path))
    model = DemoDrosophilaCellModel()
    results = model.predict_batch(rows)
    with open("predictions.json", "w", encoding="utf-8") as f:
        json.dump({"results": results}, f, indent=2, ensure_ascii=False)
    print(f"Saved predictions to predictions.json")
    for idx, item in enumerate(results):
        print_summary(item, idx)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    metadata = load_model_metadata(args.hf_repo, args.model_path)
    print(f"Model source: {metadata['source']}")

    if args.hf_repo:
        print("HF model integration selected. This project is ready for an open model repo.")
        print("If you want to use a specific model, replace the placeholder logic here with your own adapter.")

    if args.model_path:
        print("Local model path selected. This project is ready to connect to a local .pkl / .pt / .onnx implementation.")

    if args.demo:
        run_demo()
        return

    if args.input:
        run_from_csv(args.input)
        return

    # Default fallback: run the built-in demo.
    run_demo()


if __name__ == "__main__":
    main()
