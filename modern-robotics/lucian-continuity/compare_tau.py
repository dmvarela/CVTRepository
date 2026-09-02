import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
CONDITIONS = ["trace_full", "trace_distilled", "trace_none"]


def load_latest(model: str) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    files = sorted(RESULTS_DIR.glob("*.jsonl"))

    for path in files:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("model") != model:
                    continue
                if row.get("probe_id") != "TAU1_decision_recovery":
                    continue
                condition = row.get("trace_condition")
                if condition not in CONDITIONS:
                    continue
                previous = latest.get(condition)
                if previous is None or row.get("timestamp_utc", "") > previous.get("timestamp_utc", ""):
                    latest[condition] = row
    return latest


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare latest transversal tau trace outputs.")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    latest = load_latest(args.model)
    print("TAU TRACE COMPARISON: TAU1_decision_recovery")
    print("=" * 72)

    for condition in CONDITIONS:
        print(f"\nCONDITION: {condition}")
        print("-" * 72)
        row = latest.get(condition)
        if row is None:
            print("No result found.")
            continue
        print(f"Model:     {row.get('model')}")
        print(f"Timestamp: {row.get('timestamp_utc')}")
        print()
        print(row.get("response", ""))


if __name__ == "__main__":
    main()
