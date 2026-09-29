from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from src.drosophila_model import DemoDrosophilaCellModel, generate_demo_rows, load_csv_rows, print_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="v1 - Drosophila Brain Cell CLI")
    parser.add_argument("--demo", action="store_true", help="Run built-in demo")
    parser.add_argument("--input", type=str, default=None, help="Path to CSV input file")
    parser.add_argument("--model-path", type=str, default=None, help="Optional local model path (not used in demo)")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print("v1 - Command-line Drosophila Brain Cell Classifier")
    if args.demo:
        model = DemoDrosophilaCellModel()
        rows = generate_demo_rows()
        results = model.predict_batch(rows)
        for i, r in enumerate(results):
            print_summary(r, i)
        with open("v1_predictions.json", "w", encoding="utf-8") as f:
            json.dump({"results": results}, f, indent=2, ensure_ascii=False)
        print("Saved v1_predictions.json")
        return

    if args.input:
        rows = load_csv_rows(Path(args.input))
        model = DemoDrosophilaCellModel()
        results = model.predict_batch(rows)
        for i, r in enumerate(results):
            print_summary(r, i)
        out = Path("v1_predictions.json")
        with out.open("w", encoding="utf-8") as f:
            json.dump({"results": results}, f, indent=2, ensure_ascii=False)
        print(f"Saved {out}")
        return

    print("No mode selected, running demo by default.")
    model = DemoDrosophilaCellModel()
    rows = generate_demo_rows()
    results = model.predict_batch(rows)
    for i, r in enumerate(results):
        print_summary(r, i)


if __name__ == "__main__":
    main()
