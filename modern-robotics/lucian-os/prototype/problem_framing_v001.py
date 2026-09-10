"""Lucian OS problem-shape framing gate v0.01.

Simulation-only structural validator.

The host may propose that a surface request and the underlying problem shape differ,
but it may not silently replace a human-owned objective or treat a proposed reframe
as authorization to act.
"""

from __future__ import annotations

from typing import Any

DISPOSITIONS = {
    "EXECUTE_AS_FRAMED",
    "REFRAME_AND_PROPOSE",
    "ASK_OR_HOLD",
}

PROVENANCE = {"USER", "CONTEXT", "INFERRED"}


def validate_framing_state(state: dict[str, Any]) -> dict[str, Any]:
    """Validate the framing contract without certifying semantic correctness."""
    violations: list[str] = []

    surface_request = str(state.get("surface_request") or "").strip()
    if not surface_request:
        violations.append("surface_request is required")

    objective = state.get("objective")
    if not isinstance(objective, dict):
        violations.append("objective must be an object")
    else:
        if not str(objective.get("text") or "").strip():
            violations.append("objective.text is required")
        source = str(objective.get("source") or "").strip().upper()
        if source not in PROVENANCE:
            violations.append("objective.source must be USER | CONTEXT | INFERRED")

    constraints = state.get("constraints")
    if not isinstance(constraints, list):
        violations.append("constraints must be a list")
    else:
        for index, item in enumerate(constraints):
            if not isinstance(item, dict):
                violations.append(f"constraints[{index}] must be an object")
                continue
            if not str(item.get("text") or "").strip():
                violations.append(f"constraints[{index}].text is required")
            source = str(item.get("source") or "").strip().upper()
            if source not in PROVENANCE:
                violations.append(
                    f"constraints[{index}].source must be USER | CONTEXT | INFERRED"
                )

    assumptions = state.get("implementation_assumptions")
    if not isinstance(assumptions, list):
        violations.append("implementation_assumptions must be a list")
    else:
        for index, item in enumerate(assumptions):
            if not isinstance(item, dict):
                violations.append(f"implementation_assumptions[{index}] must be an object")
                continue
            if not str(item.get("text") or "").strip():
                violations.append(
                    f"implementation_assumptions[{index}].text is required"
                )
            source = str(item.get("source") or "").strip().upper()
            if source not in PROVENANCE:
                violations.append(
                    f"implementation_assumptions[{index}].source must be USER | CONTEXT | INFERRED"
                )

    problem_shape = str(state.get("problem_shape") or "").strip()
    if not problem_shape:
        violations.append("problem_shape is required")

    disposition = str(state.get("framing_disposition") or "").strip().upper()
    if disposition not in DISPOSITIONS:
        violations.append(
            "framing_disposition must be EXECUTE_AS_FRAMED | REFRAME_AND_PROPOSE | ASK_OR_HOLD"
        )

    mismatch = state.get("structural_mismatch")
    if not isinstance(mismatch, dict):
        violations.append("structural_mismatch must be an object")
        mismatch_present = False
        mismatch_basis = ""
    else:
        mismatch_present = bool(mismatch.get("present"))
        mismatch_basis = str(mismatch.get("basis") or "").strip()
        if mismatch_present and not mismatch_basis:
            violations.append("structural_mismatch.basis is required when present=true")

    proposed_reframe = str(state.get("proposed_reframe") or "").strip()

    if disposition == "REFRAME_AND_PROPOSE":
        if not mismatch_present:
            violations.append(
                "REFRAME_AND_PROPOSE requires structural_mismatch.present=true"
            )
        if not proposed_reframe:
            violations.append("REFRAME_AND_PROPOSE requires proposed_reframe")

    if disposition == "EXECUTE_AS_FRAMED" and proposed_reframe:
        violations.append(
            "EXECUTE_AS_FRAMED must not carry an unused proposed_reframe"
        )

    execution_allowed_by_framing = disposition == "EXECUTE_AS_FRAMED"

    return {
        "valid": not violations,
        "violations": violations,
        "framing_disposition": disposition if disposition in DISPOSITIONS else None,
        "execution_allowed_by_framing": execution_allowed_by_framing,
        "note": (
            "Structural validation only. valid=true does not prove that the inferred "
            "objective, problem shape, mismatch, or reframe is correct. A proposed "
            "reframe does not manufacture user authorization."
        ),
    }
