"""Lucian OS capability discovery & composition v0.02.

Consumes abstract problem requirements produced by a host-visible search state.
It discovers concrete providers from an embodiment manifest and independently
gates every step. Simulation-only: nothing is executed.
"""

from __future__ import annotations

from typing import Any

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "unknown": 3}


def capabilities_for_requirement(
    manifest: dict[str, Any],
    requirement: str,
) -> list[dict[str, Any]]:
    return [
        capability
        for capability in manifest.get("capabilities", [])
        if requirement in capability.get("provides", [])
    ]


def gate_capability(
    capability: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    authority = manifest.get("authority_defaults", {})
    permitted = set(authority.get("permitted", []))
    prohibited = set(authority.get("prohibited", []))

    name = str(capability.get("name", ""))
    enabled = bool(capability.get("enabled", False))
    explicitly_permitted = name in permitted
    explicitly_prohibited = name in prohibited
    confirmation_required = bool(capability.get("requires_confirmation", False))

    if explicitly_prohibited or not explicitly_permitted:
        status = "AUTHORITY_BLOCKED"
    elif not enabled:
        status = "UNAVAILABLE"
    elif confirmation_required:
        status = "CONFIRMATION_REQUIRED"
    else:
        status = "AVAILABLE"

    return {
        "status": status,
        "enabled": enabled,
        "permitted": explicitly_permitted,
        "prohibited": explicitly_prohibited,
        "requires_confirmation": confirmation_required,
        "risk_level": capability.get("risk_level", "unknown"),
        "reversible": capability.get("reversible"),
        "verification": capability.get("verification"),
    }


def candidate_rank(
    capability: dict[str, Any],
    manifest: dict[str, Any],
) -> tuple[int, int, int, int, str]:
    gate = gate_capability(capability, manifest)
    status_rank = {
        "AVAILABLE": 0,
        "CONFIRMATION_REQUIRED": 1,
        "UNAVAILABLE": 2,
        "AUTHORITY_BLOCKED": 3,
    }.get(gate["status"], 4)

    reversible = capability.get("reversible")
    reversible_rank = 0 if reversible is True else 1 if reversible == "sometimes" else 2
    confirmation_rank = 1 if gate["requires_confirmation"] else 0

    return (
        status_rank,
        RISK_ORDER.get(str(gate["risk_level"]).lower(), 3),
        reversible_rank,
        confirmation_rank,
        str(capability.get("name", "")),
    )


def compose_requirements(
    requirements: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    steps: list[dict[str, Any]] = []

    for index, record in enumerate(requirements, start=1):
        requirement = str(record.get("requirement") or "").strip()
        candidates = capabilities_for_requirement(manifest, requirement)
        ranked = sorted(
            candidates,
            key=lambda capability: candidate_rank(capability, manifest),
        )

        if not ranked:
            steps.append(
                {
                    "step": index,
                    "category": record.get("category"),
                    "requirement": requirement,
                    "purpose": record.get("purpose"),
                    "selected_capability": None,
                    "candidate_capabilities": [],
                    "gate": {
                        "status": "MISSING_CAPABILITY",
                        "reason": "no declared capability provides this abstract requirement",
                    },
                    "execution_permitted": False,
                }
            )
            continue

        selected = ranked[0]
        gate = gate_capability(selected, manifest)
        steps.append(
            {
                "step": index,
                "category": record.get("category"),
                "requirement": requirement,
                "purpose": record.get("purpose"),
                "selected_capability": selected.get("name"),
                "candidate_capabilities": [
                    {
                        "name": candidate.get("name"),
                        "kind": candidate.get("kind"),
                        "gate_status": gate_capability(candidate, manifest)["status"],
                    }
                    for candidate in ranked
                ],
                "gate": gate,
                "execution_permitted": False,
            }
        )

    statuses = [step["gate"]["status"] for step in steps]
    if "MISSING_CAPABILITY" in statuses:
        disposition = "UNSATISFIABLE"
    elif "AUTHORITY_BLOCKED" in statuses:
        disposition = "REFUSE"
    elif "UNAVAILABLE" in statuses:
        disposition = "HOLD"
    elif "CONFIRMATION_REQUIRED" in statuses:
        disposition = "HOLD_FOR_CONFIRMATION"
    else:
        disposition = "READY_FOR_SIMULATION"

    return {
        "architecture": "lucian-capability-composition-v0.02",
        "simulation_only": True,
        "requirements": requirements,
        "composition": steps,
        "disposition": disposition,
        "execution_permitted": False,
        "invariants": [
            "A requirement is not evidence that a provider exists.",
            "A provider is not permission to invoke it.",
            "Authority is evaluated independently for every composed step.",
            "Authority granted to one step does not propagate to another.",
            "Missing or blocked steps are never silently skipped.",
            "No capability is executed by this module.",
        ],
    }
