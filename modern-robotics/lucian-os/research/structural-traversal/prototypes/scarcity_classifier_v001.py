"""TRAVERSAL-004 — Scarcity Classification, simulation only.

The classifier diagnoses what appears to be scarce BEFORE deciding whether
structural traversal is warranted. It consumes only generator-side signals from
traversal_004_scarcity_packets.json and never loads evaluator labels.

Scarcity classes:
- STRUCTURE: the current representation is the active bottleneck;
- EVIDENCE: missing reality is the active bottleneck;
- SEARCH: no sufficiently warranted alternative path/representation is available;
- NONE: no material scarcity currently justifies leaving the target representation.

The classifier also preserves the second-ranked scarcity and a MIXED flag when
scores are close. This is a hand-authored synthetic policy, not a learned model.

Run from modern-robotics/lucian-os:
    py research/structural-traversal/prototypes/scarcity_classifier_v001.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKETS = ROOT / "manifests" / "traversal_004_scarcity_packets.json"

MIXED_MARGIN = 0.12
MIXED_MIN_SCORE = 0.60


def load_packets(path: Path = DEFAULT_PACKETS) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def scarcity_scores(s: dict[str, float]) -> dict[str, float]:
    progress = float(s["target_progress"])
    contradiction = float(s["contradiction_persistence"])
    repetition = float(s["reformulation_repetition"])
    missing = float(s["evidence_missing"])
    evidence_cost = float(s["evidence_acquisition_cost"])
    evidence_power = float(s["evidence_discriminating_power"])
    alt_quality = float(s["alternative_representation_quality"])
    alt_availability = float(s["alternative_representation_availability"])
    native_quality = float(s["domain_native_path_quality"])
    constraint_clarity = float(s["target_constraint_clarity"])

    structure = (
        0.24 * (1.0 - progress)
        + 0.18 * contradiction
        + 0.16 * repetition
        + 0.20 * alt_quality
        + 0.12 * alt_availability
        + 0.10 * (1.0 - native_quality)
    )

    evidence = (
        0.42 * missing
        + 0.23 * (1.0 - evidence_cost)
        + 0.22 * evidence_power
        + 0.13 * contradiction
    )

    search = (
        0.28 * (1.0 - progress)
        + 0.26 * (1.0 - alt_quality)
        + 0.22 * (1.0 - alt_availability)
        + 0.14 * (1.0 - native_quality)
        + 0.10 * repetition
    )

    none = (
        0.42 * progress
        + 0.30 * native_quality
        + 0.16 * (1.0 - contradiction)
        + 0.12 * constraint_clarity
    )

    return {
        "STRUCTURE": round(structure, 4),
        "EVIDENCE": round(evidence, 4),
        "SEARCH": round(search, 4),
        "NONE": round(none, 4),
    }


def classify(signals: dict[str, float]) -> dict[str, Any]:
    scores = scarcity_scores(signals)
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    primary, primary_score = ranked[0]
    secondary, secondary_score = ranked[1]
    margin = round(primary_score - secondary_score, 4)
    mixed = bool(primary_score >= MIXED_MIN_SCORE and margin < MIXED_MARGIN)

    if mixed and "EVIDENCE" in {primary, secondary}:
        evidence_is_cheap = float(signals["evidence_acquisition_cost"]) <= 0.25
        evidence_is_discriminating = float(signals["evidence_discriminating_power"]) >= 0.75
        if evidence_is_cheap and evidence_is_discriminating:
            action = "WAIT"
            action_reason = "mixed scarcity; cheap discriminating evidence should be acquired before representation change"
        elif primary == "STRUCTURE":
            action = "TRAVERSE"
            action_reason = "mixed scarcity; structure leads and missing evidence is not cheap enough to dominate"
        else:
            action = "WAIT"
            action_reason = "mixed scarcity with evidence leading"
    elif primary == "STRUCTURE":
        action = "TRAVERSE"
        action_reason = "structural scarcity dominates"
    elif primary == "EVIDENCE":
        action = "WAIT"
        action_reason = "evidence scarcity dominates"
    elif primary == "SEARCH":
        action = "ABSTAIN"
        action_reason = "search scarcity dominates; no warranted alternative representation is ready"
    else:
        action = "STAY"
        action_reason = "no material scarcity justifies leaving the current representation"

    return {
        "primary_scarcity": primary,
        "secondary_scarcity": secondary,
        "score_margin": margin,
        "mixed": mixed,
        "scores": scores,
        "recommended_action": action,
        "action_reason": action_reason,
    }


def main() -> int:
    packets = load_packets()
    rows = []
    for case in packets["cases"]:
        result = classify(case["signals"])
        rows.append({"case_id": case["id"], **result})

    report = {
        "experiment": "TRAVERSAL-004",
        "mode": "SIMULATION_ONLY",
        "policy": "SCARCITY_FIRST_v0.01",
        "warning": (
            "The scores and thresholds are hand-authored. This prototype tests explicit "
            "scarcity diagnosis and uncertainty preservation, not a validated general classifier."
        ),
        "decisions": rows,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
