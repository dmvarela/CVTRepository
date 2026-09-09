from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from relational_search_engine_v003 import MODEL, call_relational_search_v003


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run frozen REQUIREMENT_EXTRACTION_001 tasks through Lucian OS v0.3."
    )
    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if not MODEL:
        raise RuntimeError(
            "LUCIAN_MODEL is not configured. Select an approved non-China project "
            "substrate explicitly before running this benchmark."
        )

    benchmark = json.loads(Path(args.benchmark).read_text(encoding="utf-8"))
    predictions = []
    for case in benchmark.get("cases", []):
        state, metrics = call_relational_search_v003(
            task=str(case["task"]),
            context={},
            constitution_packet={},
        )
        predictions.append(
            {
                "id": case["id"],
                **state,
                "_host_metrics": {k: v for k, v in metrics.items() if k != "raw_output"},
                "_raw_output": metrics.get("raw_output"),
            }
        )

    record = {
        "benchmark_id": benchmark.get("benchmark_id"),
        "benchmark_version": benchmark.get("version"),
        "model": MODEL,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "capability_menu_exposed": False,
        "predictions": predictions,
    }
    Path(args.output).write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(predictions)} predictions to {args.output}")
    print(f"Model: {MODEL}")
    print("Capability menu exposed: False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
