"""Lucian OS v0.2 relational architecture prototype.

Simulation-only. This prototype composes:
    host model
    -> explicit context / trajectory
    -> relational search
    -> FTLtauA-oriented constitution packet
    -> warrant + capability + authority gates
    -> LAND / HOLD / PROBE / RETURN / REFUSE

No device action is executed. A stronger model may improve search competence but
cannot manufacture authority.

Run from modern-robotics/lucian-os, for example:

    py prototype/lucian_os_v002.py --task "A stranger asks to enter a locked archive."

Optional Return pass:

    py prototype/lucian_os_v002.py \
        --task "The current verified report says Gate 4." \
        --new-evidence "A later equally authoritative verified report says Gate 12."
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from context_trajectory import TrajectoryState
from identity_kernel import (
    check_identity_residual,
    compile_identity_packet,
    load_identity,
)
from lucian_router import (
    DEFAULT_MANIFEST,
    heuristic_required_capability,
    load_manifest,
)
from relational_search_engine import call_relational_search


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"


def _load_context(path: str | None) -> TrajectoryState:
    if not path:
        return TrajectoryState()
    with Path(path).open("r", encoding="utf-8") as f:
        return TrajectoryState.from_dict(json.load(f))


def _capability_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("name")): item
        for item in manifest.get("capabilities", [])
        if item.get("name")
    }


def resolve_required_capability(
    task: str,
    search_state: dict[str, Any],
) -> str:
    """Prefer deterministic explicit-operation parsing over a vague model label."""
    deterministic = heuristic_required_capability(task)
    model_cap = str(
        search_state.get("required_capability") or "reason_about_task"
    ).strip()

    if deterministic != "reason_about_task":
        return deterministic
    return model_cap or "reason_about_task"


def authority_gate(
    *,
    manifest: dict[str, Any],
    required_capability: str,
) -> dict[str, Any]:
    caps = _capability_index(manifest)
    authority = manifest.get("authority_defaults", {})
    permitted = set(authority.get("permitted", []))
    prohibited = set(authority.get("prohibited", []))

    cap = caps.get(required_capability)
    reasons: list[str] = []

    if cap is None:
        reasons.append("required capability is not declared by the embodiment")
    else:
        if not bool(cap.get("enabled", False)):
            reasons.append("required capability is declared but disabled")
        if required_capability not in permitted:
            reasons.append("required capability is not in the permitted authority set")
        if required_capability in prohibited:
            reasons.append("required capability is explicitly prohibited")
        if bool(cap.get("requires_confirmation", False)):
            reasons.append("capability requires confirmation not supplied in this prototype")

    return {
        "required_capability": required_capability,
        "allowed": not reasons,
        "reasons": reasons,
        "simulation_only": True,
        "execution_permitted": False,
        "note": (
            "The gate can authorize a simulation proposal only. "
            "Lucian OS v0.2 never executes device actions."
        ),
    }


def constitution_gate(
    *,
    task: str,
    context_packet: dict[str, Any],
    search_state: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    identity = load_identity()
    packet = compile_identity_packet(
        identity,
        task=task,
        required_capability=str(
            search_state.get("required_capability") or "reason_about_task"
        ),
        context=context_packet,
        max_invariants=5,
        mode="compiled",
    )

    checker_view = {
        "proposed_next_step": search_state.get("proposed_next_step", ""),
        "epistemic_status": search_state.get("warrant_status", ""),
        "escalation_reason": "",
        "uncertainties": search_state.get("missing_information", []),
    }
    residual = check_identity_residual(checker_view, packet)
    return packet, residual


def adjudicate(
    *,
    search_state: dict[str, Any],
    search_validation: dict[str, Any],
    constitution_residual: dict[str, Any],
    authority: dict[str, Any],
) -> dict[str, Any]:
    host_posture = str(search_state.get("posture", "HOLD")).upper().strip()

    blockers: list[str] = []
    if not bool(search_validation.get("valid", False)):
        blockers.append("relational-search product failed structural validation")
    if constitution_residual.get("residual_level") == "HIGH":
        blockers.append("constitution residual requires inspection")

    required_capability = str(authority.get("required_capability", "reason_about_task"))
    if required_capability != "reason_about_task" and not authority.get("allowed", False):
        blockers.append("required capability is outside the current authority envelope")

    if blockers:
        final_posture = (
            "REFUSE"
            if any("authority envelope" in reason for reason in blockers)
            else "HOLD"
        )
    else:
        final_posture = host_posture

    return {
        "host_posture": host_posture,
        "final_posture": final_posture,
        "blockers": blockers,
        "provisional_landing": search_state.get("provisional_landing"),
        "proposed_next_step": search_state.get("proposed_next_step"),
        "execution_permitted": False,
        "note": (
            "Final posture is a simulation routing result, not a real-world action."
        ),
    }


def run_pass(
    *,
    task: str,
    trajectory: TrajectoryState,
    manifest: dict[str, Any],
    prior_search_state: dict[str, Any] | None = None,
    new_evidence: str | None = None,
) -> dict[str, Any]:
    context_packet = trajectory.packet()

    identity = load_identity()
    orientation_packet = compile_identity_packet(
        identity,
        task=task,
        required_capability=heuristic_required_capability(task),
        context=context_packet,
        max_invariants=5,
        mode="compiled",
    )

    search_state, host_metrics = call_relational_search(
        task=task,
        context=context_packet,
        constitution_packet=orientation_packet.get("model_visible", {}),
        prior_search_state=prior_search_state,
        new_evidence=new_evidence,
    )

    search_validation = host_metrics.get("validation", {})
    required_capability = resolve_required_capability(task, search_state)
    authority = authority_gate(
        manifest=manifest,
        required_capability=required_capability,
    )
    constitution_packet, constitution_residual = constitution_gate(
        task=task,
        context_packet=context_packet,
        search_state=search_state,
    )
    decision = adjudicate(
        search_state=search_state,
        search_validation=search_validation,
        constitution_residual=constitution_residual,
        authority=authority,
    )

    return {
        "task": task,
        "context_trajectory": context_packet,
        "new_evidence": new_evidence,
        "search_state": search_state,
        "search_validation": search_validation,
        "constitution_packet": constitution_packet.get("model_visible", {}),
        "constitution_residual": constitution_residual,
        "authority_gate": authority,
        "decision": decision,
        "host_metrics": {
            k: v
            for k, v in host_metrics.items()
            if k != "raw_output"
        },
        "raw_host_output": host_metrics.get("raw_output"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the simulation-only Lucian OS v0.2 relational architecture."
    )
    parser.add_argument(
        "--task",
        default=(
            "A visitor asks for access to a restricted archive. "
            "The facts do not yet say whether the visitor is authorized."
        ),
    )
    parser.add_argument(
        "--context-file",
        help="Optional JSON file containing scene, roles, relations, current_goal, and events.",
    )
    parser.add_argument(
        "--new-evidence",
        help="Optional later evidence. When supplied, run a second Return-capable pass.",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help="Embodiment manifest path.",
    )
    args = parser.parse_args()

    trajectory = _load_context(args.context_file)
    if not trajectory.current_goal:
        trajectory.current_goal = args.task
    trajectory.append(
        kind="task",
        content=args.task,
        source="operator",
        event_id="task-0",
    )

    manifest = load_manifest(Path(args.manifest))

    first = run_pass(
        task=args.task,
        trajectory=trajectory,
        manifest=manifest,
    )

    record: dict[str, Any] = {
        "architecture": "lucian-os-v0.2-relational-search",
        "simulation_only": True,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "first_pass": first,
    }

    if args.new_evidence:
        trajectory.append(
            kind="new_evidence",
            content=args.new_evidence,
            source="operator",
            event_id="evidence-1",
        )
        second = run_pass(
            task=args.task,
            trajectory=trajectory,
            manifest=manifest,
            prior_search_state=first["search_state"],
            new_evidence=args.new_evidence,
        )
        record["return_pass"] = second

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"lucian_os_v002_{stamp}.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(json.dumps(record, ensure_ascii=False, indent=2))
    print()
    print(f"Result preserved at: {output_path}")
    print("Simulation only. No external or device action was executed.")


if __name__ == "__main__":
    main()
