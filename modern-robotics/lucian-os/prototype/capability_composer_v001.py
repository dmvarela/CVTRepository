"""Lucian OS capability discovery & composition lab v0.01.

Simulation-only.

This prototype tests one narrow architectural change:

    task
    -> abstract capability requirements
    -> capability discovery from declared `provides`
    -> per-step authority / availability gates
    -> bounded composition plan

It deliberately does NOT execute capabilities and does NOT invoke an LLM. The
first experiment isolates composition mechanics from semantic-model quality.

Run from modern-robotics/lucian-os:

    py prototype/capability_composer_v001.py \
        --task "Inspect the manifest and reason about the task"

The default manifest is the composition-lab manifest so the stable v0.1
embodiment contract remains untouched.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "windows_dev_host_composition_lab.json"

# Conservative, inspectable requirement extraction for the first lab.
# Important: these map natural-language evidence to ABSTRACT REQUIREMENTS,
# not to concrete capability names.
REQUIREMENT_PATTERNS: list[tuple[str, str]] = [
    (r"\b(inspect|list|show|check)\b.{0,32}\b(manifest|capabilit(?:y|ies))\b", "capability.enumerate"),
    (r"\b(reason|analy[sz]e|think|plan|interpret|compare|evaluate)\b", "reason.task"),
    (r"\b(read|open|inspect|show)\b.{0,32}\bfile\b", "filesystem.read"),
    (r"\b(write|save|edit|modify|create)\b.{0,32}\b(file|copy)\b", "filesystem.write"),
    (r"\b(delete|remove|erase)\b.{0,32}\b(file|copy)\b", "filesystem.delete"),
    (r"\b(web|internet|online|remote|uplink)\b", "network.request"),
]

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "unknown": 3}


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def derive_requirements(task: str) -> list[dict[str, Any]]:
    """Derive ordered abstract needs from explicit task language.

    v0.01 is intentionally conservative. If no explicit need is recognized,
    it falls back to `reason.task` rather than inventing a concrete operation.
    """
    lowered = task.lower()
    hits: list[tuple[int, int, str, str]] = []

    for pattern, requirement in REQUIREMENT_PATTERNS:
        for match in re.finditer(pattern, lowered):
            hits.append((match.start(), match.end(), requirement, match.group(0)))

    hits.sort(key=lambda item: (item[0], item[1]))

    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for start, end, requirement, evidence in hits:
        if requirement in seen:
            continue
        seen.add(requirement)
        result.append(
            {
                "requirement": requirement,
                "evidence": evidence,
                "span": [start, end],
                "status": "DERIVED_FROM_TASK_TEXT",
            }
        )

    if not result:
        result.append(
            {
                "requirement": "reason.task",
                "evidence": "fallback: open-ended task requires interpretation",
                "span": None,
                "status": "CONSERVATIVE_FALLBACK",
            }
        )

    return result


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
    exists = bool(name)
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
        "exists": exists,
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


def compose_plan(
    task: str,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    requirements = derive_requirements(task)
    steps: list[dict[str, Any]] = []

    for index, requirement_record in enumerate(requirements, start=1):
        requirement = requirement_record["requirement"]
        candidates = capabilities_for_requirement(manifest, requirement)
        ranked = sorted(
            candidates,
            key=lambda capability: candidate_rank(capability, manifest),
        )

        if not ranked:
            steps.append(
                {
                    "step": index,
                    "requirement": requirement,
                    "requirement_evidence": requirement_record,
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
                "requirement": requirement,
                "requirement_evidence": requirement_record,
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
        "architecture": "lucian-capability-composition-lab-v0.01",
        "task": task,
        "embodiment_id": manifest.get("embodiment_id"),
        "simulation_only": True,
        "requirements": requirements,
        "composition": steps,
        "disposition": disposition,
        "execution_permitted": False,
        "invariants": [
            "Requirements are abstract needs, not concrete capability names.",
            "Capability discovery is separate from task decomposition.",
            "Authority is evaluated independently for every composed step.",
            "Authority granted to one step does not propagate to another.",
            "A blocked or missing step is not silently skipped.",
            "No capability is executed by this prototype.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a simulation-only capability composition plan."
    )
    parser.add_argument("--task", required=True)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    plan = compose_plan(args.task, manifest)
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
