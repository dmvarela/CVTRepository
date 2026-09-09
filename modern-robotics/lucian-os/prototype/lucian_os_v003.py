"""Lucian OS v0.3 search-to-capability integration lab.

This module connects an observable relational-search state to abstract problem
requirements and then to embodiment-specific capability discovery/composition.

Simulation-only. No capability is executed.
"""

from __future__ import annotations

from typing import Any

from capability_composer_v002 import compose_requirements
from problem_requirements_v003 import (
    flatten_requirements,
    validate_problem_requirements,
)
from relational_search_engine_v003 import validate_search_state_v003


def compose_search_state(
    *,
    search_state: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    search_validation = validate_search_state_v003(search_state)
    requirements_validation = validate_problem_requirements(search_state)

    if not search_validation["valid"] or not requirements_validation["valid"]:
        return {
            "architecture": "lucian-os-v0.3-search-to-capability",
            "simulation_only": True,
            "search_validation": search_validation,
            "requirements_validation": requirements_validation,
            "composition": None,
            "disposition": "HOLD_INVALID_SEARCH_PRODUCT",
            "execution_permitted": False,
        }

    requirements = flatten_requirements(search_state)
    composition = compose_requirements(requirements, manifest)

    return {
        "architecture": "lucian-os-v0.3-search-to-capability",
        "simulation_only": True,
        "search_validation": search_validation,
        "requirements_validation": requirements_validation,
        "abstract_requirements": requirements,
        "composition": composition,
        "disposition": composition["disposition"],
        "execution_permitted": False,
        "invariant": (
            "The host describes needs. The embodiment advertises providers. "
            "The outer architecture controls authority and composition."
        ),
    }
