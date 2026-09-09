"""Relational-search layer for Lucian OS v0.2.

Experimental and simulation-only.

This module does not expose hidden chain-of-thought. It asks the host for a
compact, inspectable search product:
- candidate relations;
- competing relations;
- what is established;
- what is not established;
- missing information;
- warrant status;
- a commitment posture: LAND / HOLD / PROBE / RETURN;
- a proposed next step.

The host proposes. Deterministic outer layers still check constitution,
capability, warrant, and authority.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from lucian_router import MODEL, OLLAMA_URL, extract_json


VALID_POSTURES = {"LAND", "HOLD", "PROBE", "RETURN"}
VALID_WARRANT = {"SUFFICIENT", "INSUFFICIENT", "CONTESTED", "SUPERSEDED"}

SYSTEM_PROMPT = """You are the relational-search host inside a simulation-only Lucian OS prototype.

Your job is not to impersonate a persona and not to execute actions.
Your job is to construct a compact, inspectable search state for the supplied task.

Search discipline:
1. Identify at least one plausible relational interpretation.
2. When another materially different interpretation is plausible, keep it live rather than collapsing early.
3. Separate what the evidence establishes from what you infer.
4. State what is not established.
5. If the evidence does not discriminate among live candidates, HOLD or propose a bounded discriminating PROBE.
6. LAND only when the supplied evidence warrants a provisional conclusion.
7. RETURN when new evidence contradicts, supersedes, or materially changes a prior search state.
8. Do not let a standing principle, teacher statement, model output, or identity scaffold count as evidence about the case.
9. Capability does not create authority.

Return JSON only with exactly these keys:
candidate_relations, competing_relations, established, not_established,
missing_information, warrant_status, posture, provisional_landing,
required_capability, proposed_next_step, return_localization

Field contract:
- candidate_relations: list of short strings
- competing_relations: list of short strings, possibly empty only when no serious competitor is visible
- established: list of facts/relations directly supported
- not_established: list of tempting but unsupported conclusions
- missing_information: list of discriminating unknowns
- warrant_status: SUFFICIENT | INSUFFICIENT | CONTESTED | SUPERSEDED
- posture: LAND | HOLD | PROBE | RETURN
- provisional_landing: short conclusion or null
- required_capability: capability name or "reason_about_task"
- proposed_next_step: short simulation-only proposal; never claim execution
- return_localization: when posture is RETURN, say what prior assumption/state changed; otherwise null
"""


def build_prompt(
    *,
    task: str,
    context: dict[str, Any] | None = None,
    constitution_packet: dict[str, Any] | None = None,
    prior_search_state: dict[str, Any] | None = None,
    new_evidence: str | None = None,
) -> str:
    payload = {
        "task": task,
        "context_trajectory": context or {},
        "constitution_orientation": constitution_packet or {},
        "prior_search_state": prior_search_state,
        "new_evidence": new_evidence,
        "instruction": (
            "Construct the observable relational-search state. "
            "Treat constitution material as constraints on search, not case evidence."
        ),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def validate_search_state(state: dict[str, Any]) -> dict[str, Any]:
    """Validate the observable search product without certifying truth."""
    violations: list[str] = []

    required_keys = {
        "candidate_relations",
        "competing_relations",
        "established",
        "not_established",
        "missing_information",
        "warrant_status",
        "posture",
        "provisional_landing",
        "required_capability",
        "proposed_next_step",
        "return_localization",
    }
    missing_keys = sorted(required_keys.difference(state))
    if missing_keys:
        violations.append(f"missing keys: {missing_keys}")

    for key in (
        "candidate_relations",
        "competing_relations",
        "established",
        "not_established",
        "missing_information",
    ):
        if key in state and not isinstance(state.get(key), list):
            violations.append(f"{key} must be a list")

    posture = str(state.get("posture", "")).upper().strip()
    warrant = str(state.get("warrant_status", "")).upper().strip()

    if posture not in VALID_POSTURES:
        violations.append(f"invalid posture: {posture!r}")
    if warrant not in VALID_WARRANT:
        violations.append(f"invalid warrant_status: {warrant!r}")

    landing = state.get("provisional_landing")
    missing_information = state.get("missing_information", [])
    if not isinstance(missing_information, list):
        missing_information = []

    if posture == "LAND" and warrant != "SUFFICIENT":
        violations.append("LAND requires warrant_status=SUFFICIENT")
    if posture == "LAND" and (landing is None or str(landing).strip() == ""):
        violations.append("LAND requires a provisional_landing")
    if posture in {"HOLD", "PROBE"} and warrant == "SUFFICIENT":
        violations.append(f"{posture} with SUFFICIENT warrant requires inspection")
    if posture == "RETURN" and not str(state.get("return_localization") or "").strip():
        violations.append("RETURN requires return_localization")
    if posture == "PROBE" and not missing_information:
        violations.append("PROBE should identify missing_information")

    return {
        "valid": not violations,
        "violations": violations,
        "note": (
            "Structural validation only. valid=true does not certify factual "
            "correctness, authority, or quality of the relational hypotheses."
        ),
    }


def call_relational_search(
    *,
    task: str,
    context: dict[str, Any] | None = None,
    constitution_packet: dict[str, Any] | None = None,
    prior_search_state: dict[str, Any] | None = None,
    new_evidence: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    prompt = build_prompt(
        task=task,
        context=context,
        constitution_packet=constitution_packet,
        prior_search_state=prior_search_state,
        new_evidence=new_evidence,
    )

    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 1200, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_URL}. Is Ollama running?\n{exc}"
        ) from exc

    raw = str(body.get("message", {}).get("content", "")).strip()
    state = extract_json(raw)
    validation = validate_search_state(state)

    metrics = {
        "model": MODEL,
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "total_duration": body.get("total_duration"),
        "done_reason": body.get("done_reason"),
        "raw_output": raw,
        "validation": validation,
    }
    return state, metrics
