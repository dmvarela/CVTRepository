import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
PROBE_ID = "TAU2_state_vs_provenance"
CONDITIONS = ["provenance_settled", "provenance_absent"]


def load_latest(model: str, condition: str) -> dict | None:
    candidates = sorted(RESULTS_DIR.glob("*_tau2_provenance.jsonl"), reverse=True)
    for path in candidates:
        with path.open("r", encoding="utf-8") as handle:
            rows = [json.loads(line) for line in handle if line.strip()]
        for row in rows:
            if (
                row.get("model") == model
                and row.get("probe_id") == PROBE_ID
                and row.get("provenance_condition") == condition
            ):
                return row
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare latest tau provenance responses.")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    print(f"TAU PROVENANCE COMPARISON: {PROBE_ID}")
    print("=" * 72)

    for condition in CONDITIONS:
        row = load_latest(args.model, condition)
        print(f"\nCONDITION: {condition}")
        print("-" * 72)
        if row is None:
            print("No result found.")
            continue
        print(f"Model:     {row.get('model')}")
        print(f"Timestamp: {row.get('timestamp_utc')}")
        print()
        print(row.get("response", ""))


if __name__ == "__main__":
    main()
