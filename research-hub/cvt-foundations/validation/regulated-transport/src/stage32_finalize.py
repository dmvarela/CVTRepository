from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


def _strict(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {str(key): _strict(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_strict(item) for item in value]
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finalize(output_dir: str | Path) -> None:
    output = Path(output_dir)
    selection_path = output / "selection.json"
    lock_path = output / "model_lock_manifest.json"

    selection = _strict(json.loads(selection_path.read_text(encoding="utf-8")))
    selection_path.write_text(
        json.dumps(selection, indent=2, allow_nan=False),
        encoding="utf-8",
    )

    lock = _strict(json.loads(lock_path.read_text(encoding="utf-8")))
    lock["selection_sha256"] = _sha256(selection_path)
    lock_path.write_text(
        json.dumps(lock, indent=2, allow_nan=False),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/stage3_2")
    arguments = parser.parse_args()
    finalize(arguments.output)


if __name__ == "__main__":
    main()
