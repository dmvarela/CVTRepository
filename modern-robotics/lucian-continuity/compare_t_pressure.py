import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
PROBE_FILE = ROOT / "probes" / "t_pressure_probes_v004.json"
PROTOCOL_VERSION = "t-pressure-0.04"
CONDITION_ORDER = ["control", "full_v003", "minus_t_v003"]


def load_probes() -> list[dict]:
    return json.loads(PROBE_FILE.read_text(encoding="utf-8"))


def load_rows(model: str) -> list[dict]:
    rows = []
    for path in sorted(RESULTS_DIR.glob("*_t_pressure_v004.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                if (
                    row.get("protocol_version") == PROTOCOL_VERSION
                    and row.get("model") == model
                ):
                    rows.append(row)
    return rows


def latest_by_probe_condition(rows: list[dict]) -> dict[tuple[str, str], dict]:
    latest = {}
    for row in rows:
        key = (row["probe_id"], row["condition"])
        previous = latest.get(key)
        if previous is None or row["timestamp_utc"] > previous["timestamp_utc"]:
            latest[key] = row
    return latest


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare v0.04 T pressure responses.")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    probes = load_probes()
    rows = load_rows(args.model)
    latest = latest_by_probe_condition(rows)

    if not rows:
        raise SystemExit(
            f"No {PROTOCOL_VERSION} results found for model {args.model!r} in {RESULTS_DIR}."
        )

    print("T PRESSURE COMPARISON v0.04")
    print("=" * 80)

    for probe in probes:
        probe_id = probe["id"]
        print(f"\nPROBE: {probe_id}")
        print("=" * 80)
        for condition in CONDITION_ORDER:
            print(f"\nCONDITION: {condition}")
            print("-" * 72)
            row = latest.get((probe_id, condition))
            if row is None:
                print("[No result found]")
                continue
            print(f"Model:     {row['model']}")
            print(f"Timestamp: {row['timestamp_utc']}")
            print()
            print(row["response"])


if __name__ == "__main__":
    main()
