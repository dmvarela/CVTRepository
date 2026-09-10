"""TRAVERSAL-002 generator-side harness.

This script is intentionally evaluator-blind. It loads only the generator packet,
checks for obvious evaluator-label leakage, emits condition/problem packets, and can
validate a frozen JSONL candidate file against the required output schema.

It does not call an AI model and it does not load the evaluator rubric.

Run from modern-robotics/lucian-os:
    py research/structural-traversal/prototypes/structural_traversal_v002.py --emit-packets
    py research/structural-traversal/prototypes/structural_traversal_v002.py --validate-output research/structural-traversal/results/TRAVERSAL_002_RAW_OUTPUT.jsonl
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PACKET = ROOT / "manifests" / "traversal_002_generator_packets.json"

FORBIDDEN_GENERATOR_KEYS = {
    "regime",
    "known_trap",
    "useful_new_path_criterion",
    "expected_candidate",
    "expected_analogy",
    "answer_key",
    "evaluator_label",
    "score",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_forbidden_keys(obj: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN_GENERATOR_KEYS:
                hits.append(f"{path}.{key}")
            hits.extend(find_forbidden_keys(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            hits.extend(find_forbidden_keys(value, f"{path}[{idx}]"))
    return hits


def emit_packets(data: dict[str, Any]) -> None:
    conditions = data["conditions"]
    required = data["required_output_fields"]
    for problem in data["problems"]:
        for condition, instructions in conditions.items():
            packet = {
                "experiment": data["experiment"],
                "problem": problem,
                "condition": condition,
                "condition_instructions": instructions,
                "required_output_fields": required,
                "evaluator_assets_available": False,
            }
            print(json.dumps(packet, ensure_ascii=False))


def validate_output(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    required = set(data["required_output_fields"])
    valid_problem_ids = {p["problem_id"] for p in data["problems"]}
    valid_conditions = set(data["conditions"])
    errors: list[str] = []
    rows = 0
    seen: set[tuple[str, str, str]] = set()

    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            rows += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {lineno}: invalid JSON: {exc}")
                continue
            missing = sorted(required - set(row))
            if missing:
                errors.append(f"line {lineno}: missing fields {missing}")
            if row.get("problem_id") not in valid_problem_ids:
                errors.append(f"line {lineno}: unknown problem_id {row.get('problem_id')!r}")
            if row.get("condition") not in valid_conditions:
                errors.append(f"line {lineno}: unknown condition {row.get('condition')!r}")
            key = (str(row.get("problem_id")), str(row.get("condition")), str(row.get("candidate_id")))
            if key in seen:
                errors.append(f"line {lineno}: duplicate candidate key {key}")
            seen.add(key)

    return {"rows": rows, "errors": errors, "valid": not errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-packets", action="store_true")
    parser.add_argument("--validate-output", type=Path)
    args = parser.parse_args()

    data = load_json(GENERATOR_PACKET)
    leakage = find_forbidden_keys(data)
    if leakage:
        print(json.dumps({"generator_packet_clean": False, "forbidden_keys": leakage}, indent=2))
        return 2

    if args.emit_packets:
        emit_packets(data)
        return 0
    if args.validate_output:
        report = validate_output(args.validate_output, data)
        report["generator_packet_clean"] = True
        print(json.dumps(report, indent=2))
        return 0 if report["valid"] else 2

    print(json.dumps({
        "generator_packet_clean": True,
        "problems": len(data["problems"]),
        "conditions": list(data["conditions"]),
        "note": "Use --emit-packets or --validate-output PATH. Evaluator rubric is never loaded by this harness."
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
