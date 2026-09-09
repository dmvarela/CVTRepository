"""Offline smoke tests for Lucian OS v0.2 deterministic layers.

No Ollama call and no external action.
Run from modern-robotics/lucian-os:
    py prototype/test_lucian_os_v002.py
"""

from __future__ import annotations

from context_trajectory import TrajectoryState
from lucian_os_v002 import adjudicate, authority_gate
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
    valid_land = validate_search_state(_state(posture="LAND", warrant="SUFFICIENT"))
    assert valid_land["valid"], valid_land

    bad_land = validate_search_state(_state(posture="LAND", warrant="INSUFFICIENT"))
    assert not bad_land["valid"], bad_land

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

    decision = adjudicate(
        search_state=_state(posture="LAND", warrant="INSUFFICIENT"),
        search_validation=bad_land,
        constitution_residual={"residual_level": "LOW"},
        authority=reasoning,
    )
    assert decision["final_posture"] == "HOLD", decision
    assert decision["execution_permitted"] is False

    print("Lucian OS v0.2 deterministic smoke tests: PASS")


if __name__ == "__main__":
    main()
