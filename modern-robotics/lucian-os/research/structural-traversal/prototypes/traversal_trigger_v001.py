"""TRAVERSAL-003 — Triggering and Search Value, simulation only.

This prototype decides whether to STAY, TRAVERSE, WAIT, or ABSTAIN before any
structural traversal is attempted. It consumes only generator-side visible
signals from traversal_003_trigger_packets.json. It does not load evaluator
labels.

Run from modern-robotics/lucian-os:
    py research/structural-traversal/prototypes/traversal_trigger_v001.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKETS = ROOT / "manifests" / "traversal_003_trigger_packets.json"


def load_packets(path: Path = DEFAULT_PACKETS) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def gate(signals: dict[str, float]) -> dict[str, Any]:
    progress = float(signals["domain_progress"])
    repetition = float(signals["representation_repetition"])
    contradiction = float(signals["structural_contradiction"])
    missing = float(signals["missing_evidence"])
    visibility = float(signals["target_structure_visibility"])
    support = float(signals["candidate_transfer_support"])
    risk = float(signals["false_transfer_risk"])
    gain = float(signals["estimated_search_gain"])
    cost = float(signals["traversal_cost"])

    bottleneck = round(
        0.45 * repetition
        + 0.35 * contradiction
        + 0.20 * (1.0 - progress),
        4,
    )
    net_search_value = round(
        gain + 0.25 * support - cost - 0.50 * risk,
        4,
    )

    # Evidence shortage can dominate, but this first version intentionally uses
    # a conservative conjunction. Boundary failures are part of the experiment.
    if missing >= 0.75 and contradiction < 0.50 and repetition < 0.65:
        decision = "WAIT"
        reason = "target evidence appears more limiting than representation"
    elif visibility >= 0.75 or progress >= 0.72:
        decision = "STAY"
        reason = "target-domain structure is already visible or ordinary search is progressing"
    elif bottleneck >= 0.65 and net_search_value >= 0.20:
        decision = "TRAVERSE"
        reason = "representation bottleneck is high and expected search value clears cost/risk"
    elif support < 0.35 or risk >= 0.75 or net_search_value < 0.10:
        decision = "ABSTAIN"
        reason = "cross-domain transfer is weak, risky, or low-value"
    else:
        decision = "STAY"
        reason = "no positive-value case for leaving the current representation"

    return {
        "decision": decision,
        "bottleneck_score": bottleneck,
        "net_search_value": net_search_value,
        "reason": reason,
    }


def main() -> int:
    data = load_packets()
    rows = []
    for case in data["cases"]:
        result = gate(case["signals"])
        rows.append({
            "case_id": case["id"],
            "decision": result["decision"],
            "bottleneck_score": result["bottleneck_score"],
            "net_search_value": result["net_search_value"],
            "reason": result["reason"],
        })

    report = {
        "experiment": "TRAVERSAL-003",
        "mode": "SIMULATION_ONLY",
        "policy": "GATED_TRAVERSAL_v0.01",
        "warning": "No evaluator labels are loaded by this prototype. This is a hand-authored synthetic trigger policy, not a learned or validated general policy.",
        "decisions": rows,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
