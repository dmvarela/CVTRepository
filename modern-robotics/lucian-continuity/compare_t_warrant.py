import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
CONDITION_ORDER = ["control", "full_v003", "minus_t_v003"]


def load_latest(model: str) -> tuple[Path, list[dict]]:
    safe_model = model.replace("/", "_").replace(":", "_")
    matches = sorted(RESULTS_DIR.glob(f"*_{safe_model}_t_warrant_v003.jsonl"))
    if not matches:
        raise FileNotFoundError(
            f"No v0.03 T-warrant result file found for {model} in {RESULTS_DIR}"
        )
    path = matches[-1]
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return path, rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare v0.03 warrant-sensitive T results.")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    path, rows = load_latest(args.model)
    probe_ids = []
    for row in rows:
        if row["probe_id"] not in probe_ids:
            probe_ids.append(row["probe_id"])

    print(f"T WARRANT COMPARISON v0.03 — {path.name}")
    print("=" * 88)

    for probe_id in probe_ids:
        print(f"\nPROBE: {probe_id}")
        print("=" * 88)
        probe_rows = [r for r in rows if r["probe_id"] == probe_id]
        for condition in CONDITION_ORDER:
            matching = [r for r in probe_rows if r["condition"] == condition]
            if not matching:
                continue
            row = matching[-1]
            print(f"\nCONDITION: {condition}")
            print("-" * 72)
            print(f"Model:     {row['model']}")
            print(f"Timestamp: {row['timestamp_utc']}")
            print()
            print(row["response"])


if __name__ == "__main__":
    main()
