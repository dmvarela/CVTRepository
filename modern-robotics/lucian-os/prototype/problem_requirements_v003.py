"""Observable problem-requirement contract for Lucian OS v0.3.

Simulation-only support module.

The host may describe what a problem requires, but these requirements are not
capabilities, permissions, or evidence that a provider exists.
"""

from __future__ import annotations

import re
from typing import Any

REQUIREMENT_FIELDS = (
    "required_observations",
    "required_transformations",
    "required_actions",
    "required_external_interfaces",
)

_NEED_RE = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)+$")


def validate_problem_requirements(state: dict[str, Any]) -> dict[str, Any]:
    """Check the observable contract without certifying semantic correctness."""
    violations: list[str] = []

    for field in REQUIREMENT_FIELDS:
        value = state.get(field)
        if not isinstance(value, list):
            violations.append(f"{field} must be a list")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                violations.append(f"{field}[{index}] must be an object")
                continue
            need = str(item.get("need") or "").strip()
            purpose = str(item.get("purpose") or "").strip()
            if not need:
                violations.append(f"{field}[{index}] missing need")
            elif not _NEED_RE.match(need):
                violations.append(
                    f"{field}[{index}].need must be a dotted abstract namespace"
                )
            if not purpose:
                violations.append(f"{field}[{index}] missing purpose")

    constraints = state.get("constraints")
    if not isinstance(constraints, list):
        violations.append("constraints must be a list")
    else:
        for index, item in enumerate(constraints):
            if not isinstance(item, dict):
                violations.append(f"constraints[{index}] must be an object")
                continue
            if not str(item.get("constraint") or "").strip():
                violations.append(f"constraints[{index}] missing constraint")
            source = str(item.get("source") or "").strip().upper()
            if source not in {"USER", "CONTEXT", "INFERRED"}:
                violations.append(
                    f"constraints[{index}].source must be USER | CONTEXT | INFERRED"
                )

    return {
        "valid": not violations,
        "violations": violations,
        "note": (
            "Structural validation only. valid=true does not prove that the "
            "requirements are complete, necessary, feasible, or authorized."
        ),
    }


def flatten_requirements(state: dict[str, Any]) -> list[dict[str, Any]]:
    """Return ordered abstract requirements for outer capability discovery."""
    records: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for field in REQUIREMENT_FIELDS:
        category = field.removeprefix("required_")
        for index, item in enumerate(state.get(field, []) or []):
            if not isinstance(item, dict):
                continue
            need = str(item.get("need") or "").strip()
            purpose = str(item.get("purpose") or "").strip()
            if not need:
                continue
            key = (category, need)
            if key in seen:
                continue
            seen.add(key)
            records.append(
                {
                    "category": category,
                    "requirement": need,
                    "purpose": purpose,
                    "source_field": field,
                    "source_index": index,
                }
            )
    return records
