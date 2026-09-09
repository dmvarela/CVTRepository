"""Offline safety/plumbing tests for Lucian OS v0.2 deterministic layers.

No Ollama call and no external action.
Run from modern-robotics/lucian-os:
    py prototype/test_lucian_os_v002.py

IMPORTANT:
A PASS here does NOT certify semantic correctness of host reasoning. These tests
only check deterministic contracts, authority boundaries, identity selection,
and the rule that a host cannot certify its own LAND decision.
"""

from __future__ import annotations

from context_trajectory import TrajectoryState
from lucian_os_v002 import (
    V002_IDENTITY,
    adjudicate,
    authority_gate,
    independent_warrant_gate,
)
from lucian_router import load_manifest
from relational_search_engine import validate_search_state


def _state(*, posture: str, warrant: str) -> dict:
    return {
        "candidate_relations": ["candidate A"],
        "competing_relations": ["candidate B"],
        "established": ["fact 1"],
        "not_established": ["stronger claim"],
        "missing_information": [] if posture == "LAND" else ["discriminator"],
        "warrant_status": warrant,
        "posture": posture,
        "provisional_landing": "provisional conclusion" if posture == "LAND" else None,
        "required_capability": "reason_about_task",
        "proposed_next_step": "Preserve the conclusion as provisional.",
        "return_localization": "new evidence changed fact 1" if posture == "RETURN" else None,
    }


def main() -> None:
    # Structural validator: checks shape and posture/warrant consistency only.
    valid_land = validate_search_state(_state(posture="LAND", warrant="SUFFICIENT"))
    assert valid_land["valid"], valid_land

    bad_land = validate_search_state(_state(posture="LAND", warrant="INSUFFICIENT"))
    assert not bad_land["valid"], bad_land

    bad_return = _state(posture="RETURN", warrant="SUPERSEDED")
    bad_return["return_localization"] = None
    assert not validate_search_state(bad_return)["valid"]

    bad_probe = _state(posture="PROBE", warrant="INSUFFICIENT")
    bad_probe["missing_information"] = []
    assert not validate_search_state(bad_probe)["valid"]

    # Explicitly demonstrate the validator's limitation: a structurally valid
    # state can still contain a semantically unsupported landing. Therefore the
    # validator must never be treated as a truth judge.
    unsupported_but_well_formed = _state(posture="LAND", warrant="SUFFICIENT")
    unsupported_but_well_formed["provisional_landing"] = "An unsupported claim"
    assert validate_search_state(unsupported_but_well_formed)["valid"]

    # The independent warrant gate is what prevents host self-certification.
    no_external_verifier = independent_warrant_gate(
        search_state=_state(posture="LAND", warrant="SUFFICIENT")
    )
    assert not no_external_verifier["allowed_to_land"], no_external_verifier

    externally_verified = independent_warrant_gate(
        search_state=_state(posture="LAND", warrant="SUFFICIENT"),
        independent_verification={
            "verified": True,
            "verifier": "offline-test-fixture",
            "evidence": "frozen typed fixture",
        },
    )
    assert externally_verified["allowed_to_land"], externally_verified

    # v0.2 must not silently fall back to the historical v0.01 identity JSON.
    assert V002_IDENTITY.name == "lucian_identity_v002.json"
    assert V002_IDENTITY.exists(), V002_IDENTITY

    trajectory = TrajectoryState(scene="test")
    trajectory.append(kind="observation", content="Gate 4", event_id="e0")
    trajectory.append(
        kind="new_evidence",
        content="Gate 12",
        supersedes_event_id="e0",
        event_id="e1",
    )
    packet = trajectory.packet()
    assert len(packet["ordered_events"]) == 2
    assert packet["ordered_events"][0]["content"] == "Gate 4"
    assert packet["ordered_events"][1]["supersedes_event_id"] == "e0"

    manifest = load_manifest()
    reasoning = authority_gate(
        manifest=manifest,
        required_capability="reason_about_task",
    )
    assert reasoning["allowed"], reasoning

    write = authority_gate(
        manifest=manifest,
        required_capability="write_file",
    )
    assert not write["allowed"], write
    assert not write["execution_permitted"], write

    # Even a structurally valid host LAND is held unless independently verified.
    proposed_land = _state(posture="LAND", warrant="SUFFICIENT")
    proposed_land_validation = validate_search_state(proposed_land)
    decision = adjudicate(
        search_state=proposed_land,
        search_validation=proposed_land_validation,
        constitution_residual={"residual_level": "LOW"},
        authority=reasoning,
        warrant_gate=no_external_verifier,
    )
    assert decision["final_posture"] == "HOLD", decision
    assert "LAND lacks independent warrant certification" in decision["blockers"]
    assert decision["execution_permitted"] is False

    # Invalid search products also HOLD.
    decision_invalid = adjudicate(
        search_state=_state(posture="LAND", warrant="INSUFFICIENT"),
        search_validation=bad_land,
        constitution_residual={"residual_level": "LOW"},
        authority=reasoning,
        warrant_gate=no_external_verifier,
    )
    assert decision_invalid["final_posture"] == "HOLD", decision_invalid

    print("Lucian OS v0.2 deterministic safety/plumbing audit: PASS")
    print("Semantic correctness: NOT CERTIFIED by this test.")


if __name__ == "__main__":
    main()
