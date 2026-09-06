"""Lucian OS v0.1 prototype router with identity conditioning.

Simulation-only prototype.

Purpose:
- load an embodiment manifest;
- load a machine-readable Lucian identity scaffold;
- compile a small task-relevant identity packet;
- ask a local Qwen host for an independent task interpretation;
- run a deterministic identity-residual smoke test;
- cross-check the interpretation against the manifest;
- keep identity, capability, competence, warrant, and authority separate;
- print a bounded routing decision without executing device actions.

Run from the lucian-os directory:
    py prototype/lucian_router.py

Optional environment variables:
    LUCIAN_MODEL=qwen3.5:2b-q4_K_M
    OLLAMA_URL=http://localhost:11434/api/chat
    LUCIAN_IDENTITY_MODE=compiled   # compiled | full | none
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from identity_kernel import (
    check_identity_residual,
    compile_identity_packet,
    load_identity,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "windows_dev_host.json"
MODEL = os.environ.get("LUCIAN_MODEL", "qwen3.5:2b-q4_K_M")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
IDENTITY_MODE = os.environ.get("LUCIAN_IDENTITY_MODE", "compiled").lower().strip()


SYSTEM_PROMPT = """You are serving as a development host inside Lucian OS v0.1.
Your role is limited to task interpretation and proposal generation.

You may receive a small identity packet containing standing operating constraints.
Treat those constraints as orientation, not as evidence, capability, or permission.

Rules:
1. Do not invent device capabilities.
2. Do not treat a proposed action as authorized.
3. Distinguish observed/retrieved information from inference.
4. If the task cannot be resolved from the provided manifest, say so.
5. Output JSON only.
6. This prototype is simulation-only: never claim an action was executed.

Return exactly these keys:
interpretation, required_capability, epistemic_status, risk_guess,
local_reasoning_sufficient, escalation_reason, proposed_next_step, uncertainties.
"""


KEYWORD_CAPABILITIES: list[tuple[tuple[str, ...], str]] = [
    (("delete", "remove", "erase"), "delete_file"),
    (("write", "save", "edit", "modify", "change file"), "write_file"),
    (("read file", "open file", "inspect file", "show file"), "read_file"),
    (("internet", "web", "online", "uplink", "remote ai", "central ai"), "network_uplink"),
]


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def capability_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {c["name"]: c for c in manifest.get("capabilities", [])}


def heuristic_required_capability(task: str) -> str:
    lowered = task.lower()
    for keywords, capability in KEYWORD_CAPABILITIES:
        if any(k in lowered for k in keywords):
            return capability
    return "reason_about_task"


def compact_manifest_for_model(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "embodiment_id": manifest.get("embodiment_id"),
        "simulation_only": manifest.get("identity", {}).get("simulation_only", True),
        "available_models": manifest.get("available_models", []),
        "capabilities": [
            {
                "name": c.get("name"),
                "kind": c.get("kind"),
                "risk_level": c.get("risk_level"),
                "enabled": c.get("enabled", False),
                "requires_confirmation": c.get("requires_confirmation", False),
            }
            for c in manifest.get("capabilities", [])
        ],
        "authority_defaults": manifest.get("authority_defaults", {}),
    }


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Model did not return complete JSON. Raw output:\n{text}")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned malformed or truncated JSON. Raw output:\n{text}") from exc


def call_qwen(
    task: str,
    manifest: dict[str, Any],
    identity_packet: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    model_visible_identity = identity_packet.get("model_visible", {})
    user_prompt = {
        "task": task,
        "identity_packet": model_visible_identity,
        "embodiment_manifest": compact_manifest_for_model(manifest),
        "instruction": "Interpret the task. Do not execute it. Return JSON only.",
    }

    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 800, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_URL}. Is Ollama running?\n{exc}"
        ) from exc

    content = body.get("message", {}).get("content", "")
    try:
        model_view = extract_json(content)
    except ValueError as exc:
        raise ValueError(
            "Host output could not be parsed as complete JSON. "
            f"done_reason={body.get('done_reason')!r}, eval_count={body.get('eval_count')!r}.\n{exc}"
        ) from exc

    metrics = {
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "total_duration": body.get("total_duration"),
        "load_duration": body.get("load_duration"),
        "prompt_eval_duration": body.get("prompt_eval_duration"),
        "eval_duration": body.get("eval_duration"),
        "done_reason": body.get("done_reason"),
        "identity_packet_chars": len(json.dumps(model_visible_identity, ensure_ascii=False)),
    }
    return model_view, metrics


def triangulate(
    task: str,
    manifest: dict[str, Any],
    model_view: dict[str, Any],
    identity_packet: dict[str, Any],
    identity_residual: dict[str, Any],
    host_metrics: dict[str, Any],
) -> dict[str, Any]:
    """Cross-check model interpretation against deterministic rules + manifest.

    Qwen may suggest a capability, but Qwen cannot create one and cannot grant authority.
    Identity may restrict or contest a proposal, but identity cannot create authority.
    Authority failure is terminal: stronger intelligence cannot manufacture permission.
    """

    caps = capability_index(manifest)
    authority = manifest.get("authority_defaults", {})
    permitted = set(authority.get("permitted", []))
    prohibited = set(authority.get("prohibited", []))

    deterministic_cap = heuristic_required_capability(task)
    model_cap = str(model_view.get("required_capability", "")).strip()

    # If deterministic parsing detects an explicit operation, it wins over a vague model label.
    required_cap = deterministic_cap if deterministic_cap != "reason_about_task" else model_cap
    if required_cap not in caps:
        required_cap = deterministic_cap

    cap = caps.get(required_cap)
    exists = cap is not None
    enabled = bool(cap and cap.get("enabled", False))
    authorized = bool(required_cap in permitted and required_cap not in prohibited)
    requires_confirmation = bool(cap and cap.get("requires_confirmation", False))

    capability_reasons: list[str] = []
    authority_reasons: list[str] = []

    if not exists:
        capability_reasons.append("required capability is not declared by the embodiment")
    elif not enabled:
        capability_reasons.append("required capability is declared but disabled in this prototype")

    if exists and not authorized:
        authority_reasons.append("current authority envelope does not permit the capability")

    network_cap = caps.get("network_uplink", {})
    uplink_available = bool(network_cap.get("enabled", False))

    # Routing invariant:
    # - unauthorized => BLOCK
    # - authorized but locally unavailable/incompetent => ESCALATE if possible
    # - authorized and locally available => LOCAL
    if authority_reasons:
        disposition = "BLOCK"
        escalation = "NOT_ALLOWED"
        reasons = authority_reasons + capability_reasons
    elif capability_reasons:
        disposition = "ESCALATE"
        escalation = (
            "BUILD_BOUNDED_ESCALATION_PACKET"
            if uplink_available
            else "UNAVAILABLE_IN_V0.1"
        )
        reasons = capability_reasons
    else:
        disposition = "LOCAL_PROPOSAL_ONLY"
        escalation = "NOT_REQUIRED"
        reasons = []

    proposal_review = (
        "REQUIRED"
        if identity_residual.get("residual_level") == "HIGH"
        else "NO_IDENTITY_CONFLICT_DETECTED"
    )

    return {
        "task": task,
        "embodiment_id": manifest.get("embodiment_id"),
        "simulation_only": True,
        "identity": {
            "mode": identity_packet.get("mode"),
            "identity_id": identity_packet.get("identity_id"),
            "active_invariants": identity_packet.get("selected_ids", []),
            "residual": identity_residual,
            "proposal_review": proposal_review,
            "invariant": "Identity may constrain search or contest a proposal but may not manufacture authority or fact.",
        },
        "triangulation": {
            "human_input": task,
            "model_interpretation": model_view,
            "deterministic_required_capability": deterministic_cap,
            "manifest_required_capability": required_cap,
        },
        "capability_check": {
            "exists": exists,
            "enabled": enabled,
            "risk_level": cap.get("risk_level") if cap else "unknown",
            "requires_confirmation": requires_confirmation,
        },
        "authority_check": {
            "authorized": authorized,
            "mode": authority.get("mode"),
            "permitted": sorted(permitted),
            "prohibited": sorted(prohibited),
        },
        "routing": {
            "disposition": disposition,
            "escalation": escalation,
            "reasons": reasons,
        },
        "host_metrics": host_metrics,
        "routing_invariant": (
            "Authority is evaluated before escalation. A stronger reasoning tier may "
            "increase competence but may not create permission."
        ),
        "epistemic_note": (
            "The model interpretation is a proposal. Capability and authority are "
            "determined by the manifest and policy, not by model confidence."
        ),
        "execution": "NONE — simulation-only prototype",
    }


def main() -> int:
    manifest = load_manifest()
    identity = load_identity()

    print("Lucian OS v0.1 — Identity-Conditioned Capability & Escalation Router")
    print(f"Embodiment: {manifest.get('embodiment_id')}")
    print(f"Host model: {MODEL}")
    print(f"Identity mode: {IDENTITY_MODE}")
    print("Mode: SIMULATION ONLY")
    print()

    task = " ".join(sys.argv[1:]).strip()
    if not task:
        task = input("Task> ").strip()
    if not task:
        print("No task supplied.")
        return 1

    deterministic_cap = heuristic_required_capability(task)
    identity_packet = compile_identity_packet(
        identity,
        task=task,
        required_capability=deterministic_cap,
        context={"embodiment_id": manifest.get("embodiment_id")},
        mode=IDENTITY_MODE,
    )

    print("\n[1/4] Compiling task-relevant identity packet...")
    print(f"Active invariants: {identity_packet.get('selected_ids', [])}")

    print("[2/4] Asking host model for an independent interpretation...")
    model_view, host_metrics = call_qwen(task, manifest, identity_packet)

    print("[3/4] Checking host proposal against identity + embodiment reality + authority...")
    identity_residual = check_identity_residual(model_view, identity_packet)
    decision = triangulate(
        task,
        manifest,
        model_view,
        identity_packet,
        identity_residual,
        host_metrics,
    )

    print("[4/4] Routing decision:\n")
    print(json.dumps(decision, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
