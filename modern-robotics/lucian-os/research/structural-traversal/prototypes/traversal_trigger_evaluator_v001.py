"""Posthoc evaluator for TRAVERSAL-003 frozen trigger decisions.

This file is intentionally downstream of the raw-decision freeze. It compares
GATED_TRAVERSAL_v0.01 with two deliberately simple baselines:
- ALWAYS_TRAVERSE
- ALWAYS_STAY

Run from modern-robotics/lucian-os:
    py research/structural-traversal/prototypes/traversal_trigger_evaluator_v001.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "TRAVERSAL_003_RAW_DECISIONS.json"
RUBRIC = ROOT / "manifests" / "traversal_003_evaluator_rubric.json"


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def score(decisions: dict[str, str], expected: dict[str, str], costs: dict[str, float], wrong_penalty: float) -> dict[str, Any]:
    n = len(expected)
    correct = sum(decisions[k] == expected[k] for k in expected)
    wrong = n - correct
    action_cost = round(sum(float(costs[decisions[k]]) for k in expected), 4)
    wasted = sum(decisions[k] == "TRAVERSE" and expected[k] != "TRAVERSE" for k in expected)
    missed = sum(decisions[k] != "TRAVERSE" and expected[k] == "TRAVERSE" for k in expected)
    premature = sum(decisions[k] in {"STAY", "TRAVERSE"} and expected[k] == "WAIT" for k in expected)
    unnecessary_moves = sum(decisions[k] != "STAY" and expected[k] == "STAY" for k in expected)
    return {
        "cases": n,
        "correct": correct,
        "accuracy": round(correct / n, 3),
        "wrong": wrong,
        "action_cost": action_cost,
        "total_loss": round(action_cost + wrong_penalty * wrong, 4),
        "wasted_traversals": wasted,
        "missed_beneficial_traversals": missed,
        "premature_commitments_when_wait_expected": premature,
        "unnecessary_moves_when_stay_expected": unnecessary_moves,
    }


def main() -> int:
    raw = load(RAW)
    rubric = load(RUBRIC)
    expected = {row["case_id"]: row["expected_action"] for row in rubric["cases"]}
    gated = {row["case_id"]: row["decision"] for row in raw["decisions"]}
    always_traverse = {k: "TRAVERSE" for k in expected}
    always_stay = {k: "STAY" for k in expected}
    costs = rubric["action_costs"]
    penalty = float(rubric["wrong_decision_penalty"])

    mismatches = [
        {"case_id": k, "expected": expected[k], "observed": gated[k]}
        for k in expected
        if expected[k] != gated[k]
    ]

    report = {
        "experiment": "TRAVERSAL-003",
        "mode": "SIMULATION_ONLY",
        "warning": "Synthetic posthoc evaluation; same assistant authored packets and rubric. Commit order prevents forward repository label leakage but does not create evaluator independence.",
        "metrics": {
            "GATED_TRAVERSAL_v0.01": score(gated, expected, costs, penalty),
            "ALWAYS_TRAVERSE": score(always_traverse, expected, costs, penalty),
            "ALWAYS_STAY": score(always_stay, expected, costs, penalty),
        },
        "gated_mismatches": mismatches,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
