"""Lucian OS v0.4 framing-gate integration lab.

This module places a problem-shape framing gate before the v0.3 abstract
requirement/capability-composition pipeline.

Simulation-only. No capability is executed.
"""

from __future__ import annotations

from typing import Any

from lucian_os_v003 import compose_search_state
from problem_framing_v001 import validate_framing_state


def compose_framed_search_state(
    *,
    framing_state: dict[str, Any],
    search_state: dict[str, Any],
    manifest: dict[str, Any],
    reframe_authorized: bool = False,
) -> dict[str, Any]:
    framing_validation = validate_framing_state(framing_state)

    if not framing_validation["valid"]:
        return {
            "architecture": "lucian-os-v0.4-problem-shape-gate",
            "simulation_only": True,
            "framing_validation": framing_validation,
            "composition": None,
            "disposition": "HOLD_INVALID_FRAMING_PRODUCT",
            "execution_permitted": False,
        }

    framing_disposition = framing_validation["framing_disposition"]

    if framing_disposition == "ASK_OR_HOLD":
        return {
            "architecture": "lucian-os-v0.4-problem-shape-gate",
            "simulation_only": True,
            "framing_validation": framing_validation,
            "composition": None,
            "disposition": "HOLD_FOR_FRAMING",
            "execution_permitted": False,
        }

    if framing_disposition == "REFRAME_AND_PROPOSE" and not reframe_authorized:
        return {
            "architecture": "lucian-os-v0.4-problem-shape-gate",
            "simulation_only": True,
            "framing_validation": framing_validation,
            "proposed_reframe": framing_state.get("proposed_reframe"),
            "composition": None,
            "disposition": "HOLD_FOR_REFRAME_CONFIRMATION",
            "execution_permitted": False,
        }

    downstream = compose_search_state(search_state=search_state, manifest=manifest)

    return {
        "architecture": "lucian-os-v0.4-problem-shape-gate",
        "simulation_only": True,
        "framing_validation": framing_validation,
        "reframe_authorized": bool(reframe_authorized),
        "downstream": downstream,
        "composition": downstream.get("composition"),
        "disposition": downstream.get("disposition"),
        "execution_permitted": False,
        "invariant": (
            "Preserve the human-owned objective. Challenge implementation assumptions "
            "when warranted. Do not silently convert a proposed reframe into authority."
        ),
    }
