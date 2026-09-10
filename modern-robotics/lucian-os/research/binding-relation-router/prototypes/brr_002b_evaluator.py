"""Evaluate frozen BRR-002B outputs against the post-freeze key.

This script does not call a model. It scores already-frozen outputs only.
Run from modern-robotics/lucian-os:
    py research/binding-relation-router/prototypes/brr_002b_evaluator.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research" / "binding-relation-router"
OUTPUT = BASE / "results" / "BRR_002B_FROZEN_ASSISTANT_OUTPUT.json"
KEY = BASE / "manifests" / "brr_002b_evaluator_key.json"

DEFAULT_VECTOR = {
    "evidence": "PASS",
    "representation": "PASS",
    "competence": "SUFFICIENT",
    "capability": "AVAILABLE",
    "authority": "PASS",
    "resources": "SUFFICIENT",
    "viability": "OPEN",
    "search_path": "AVAILABLE",
}


def expected_vector(active_relation: str, active_state: str) -> dict[str, str]:
    vector = dict(DEFAULT_VECTOR)
    vector[active_relation] = active_state
    return vector


def main() -> None:
    frozen = json.loads(OUTPUT.read_text(encoding="utf-8"))
    key = json.loads(KEY.read_text(encoding="utf-8"))
    expected = key["expected"]
    rows = {row["case_id"]: row for row in frozen["rows"]}

    metrics = {
        "cases": len(expected),
        "active_relation_state_correct": 0,
        "exact_vector_correct": 0,
        "binding_relation_correct": 0,
        "direct_response_correct": 0,
        "routed_response_correct": 0,
        "kernel_recoveries": 0,
        "kernel_degradations": 0,
        "pair_consistency": 0,
        "pairs": len(key["pairs"]),
        "false_escalations": 0,
        "false_actions": 0,
        "false_refusals": 0,
    }

    details = []
    for case_id, exp in expected.items():
        row = rows[case_id]
        vector = row["relation_vector"]
        exp_vector = expected_vector(exp["active_relation"], exp["active_state"])

        active_ok = vector.get(exp["active_relation"]) == exp["active_state"]
        exact_ok = vector == exp_vector
        binding_ok = row["binding_relation"] == exp["binding_relation"]
        direct_ok = row["direct_response"] == exp["response"]
        routed_ok = row["routed_response"] == exp["response"]

        metrics["active_relation_state_correct"] += int(active_ok)
        metrics["exact_vector_correct"] += int(exact_ok)
        metrics["binding_relation_correct"] += int(binding_ok)
        metrics["direct_response_correct"] += int(direct_ok)
        metrics["routed_response_correct"] += int(routed_ok)
        metrics["kernel_recoveries"] += int((not direct_ok) and routed_ok)
        metrics["kernel_degradations"] += int(direct_ok and (not routed_ok))

        if row["direct_response"] == "ESCALATE_INTELLIGENCE" and exp["response"] != "ESCALATE_INTELLIGENCE":
            metrics["false_escalations"] += 1
        if row["direct_response"] == "ACT" and exp["response"] != "ACT":
            metrics["false_actions"] += 1
        if row["direct_response"] == "REFUSE" and exp["response"] != "REFUSE":
            metrics["false_refusals"] += 1

        details.append({
            "case_id": case_id,
            "active_ok": active_ok,
            "exact_vector_ok": exact_ok,
            "binding_ok": binding_ok,
            "direct_ok": direct_ok,
            "routed_ok": routed_ok,
        })

    for left, right in key["pairs"]:
        l = next(d for d in details if d["case_id"] == left)
        r = next(d for d in details if d["case_id"] == right)
        if all(l[k] and r[k] for k in ("active_ok", "binding_ok", "direct_ok", "routed_ok")):
            metrics["pair_consistency"] += 1

    print(json.dumps({"experiment": "BRR-002B", "metrics": metrics, "details": details}, indent=2))


if __name__ == "__main__":
    main()
