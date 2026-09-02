import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"


def load_rows() -> list[dict]:
    rows: list[dict] = []
    if not RESULTS_DIR.exists():
        return rows

    for path in RESULTS_DIR.glob("*.jsonl"):
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    row = json.loads(line)
                    row["_source_file"] = str(path)
                    rows.append(row)
        except (OSError, json.JSONDecodeError):
            continue

    return rows


def latest_for(rows: list[dict], probe_id: str, condition: str, model: str | None) -> dict | None:
    matches = [
        row
        for row in rows
        if row.get("probe_id") == probe_id
        and row.get("genome_condition") == condition
        and (model is None or row.get("model") == model)
    ]
    if not matches:
        return None
    return max(matches, key=lambda row: row.get("timestamp_utc", ""))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show the latest saved responses for one behavioral probe across MVCG conditions."
    )
    parser.add_argument("--probe", required=True, help="Probe ID, e.g. P2_truth_vs_pleasing")
    parser.add_argument("--model", help="Optional model filter")
    parser.add_argument(
        "--conditions",
        nargs="+",
        default=["control", "ftlta_full", "ablate_t"],
        help="Genome conditions to compare",
    )
    args = parser.parse_args()

    rows = load_rows()
    if not rows:
        raise SystemExit("No saved JSONL results found under results/.")

    print()
    print(f"PROBE COMPARISON: {args.probe}")
    print("=" * 72)

    for condition in args.conditions:
        row = latest_for(rows, args.probe, condition, args.model)
        print()
        print(f"CONDITION: {condition}")
        print("-" * 72)
        if row is None:
            print("[No matching saved result found]")
            continue

        print(f"Model:     {row.get('model', 'unknown')}")
        print(f"Timestamp: {row.get('timestamp_utc', 'unknown')}")
        print()
        print(row.get("response", ""))

    print()


if __name__ == "__main__":
    main()
