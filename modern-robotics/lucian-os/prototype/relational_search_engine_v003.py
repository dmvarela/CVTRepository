"""Relational-search contract for Lucian OS v0.3.

The host produces both a relational search state and an abstract description of
what the problem requires. The outer architecture—not the host—discovers
providers, checks authority, and decides whether the requirements are satisfiable.

No device action is executed.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from lucian_router import OLLAMA_URL, extract_json
from problem_requirements_v003 import validate_problem_requirements

MODEL = os.environ.get("LUCIAN_MODEL", "").strip()

VALID_POSTURES = {"LAND", "HOLD", "PROBE", "RETURN"}
VALID_WARRANT = {"SUFFICIENT", "INSUFFICIENT", "CONTESTED", "SUPERSEDED"}

SYSTEM_PROMPT = """You are the relational-search host inside a simulation-only Lucian OS prototype.

Your role is to describe the problem and its abstract requirements, not to pick
installed applications, grant authority, or claim that a provider exists.

Search discipline:
1. Keep materially different relational interpretations live when warranted.
2. Separate established from not-established.
3. LAND only when evidence warrants a provisional conclusion.
4. HOLD or PROBE when discrimination is still needed.
5. RETURN when later evidence changes a prior search state.
6. Capability does not create authority.
7. Describe needs using abstract dotted namespaces such as filesystem.read,
   document.summarize, network.request, image.inspect, or reason.compare.
8. A named need is not proof that the embodiment can satisfy it.

Return JSON only with exactly these keys:
candidate_relations, competing_relations, established, not_established,
missing_information, warrant_status, posture, provisional_landing,
required_observations, required_transformations, required_actions,
required_external_interfaces, constraints, proposed_next_step,
return_localization

Each required_* field is a list of objects:
{"need": "abstract.namespace", "purpose": "why the problem requires it"}

constraints is a list of:
{"constraint": "short text", "source": "USER|CONTEXT|INFERRED"}

Do not output concrete installed capability names unless the task itself is about
those names. Do not claim execution.
"""


def build_prompt(
    *,
    task: str,
    context: dict[str, Any] | None = None,
    constitution_packet: dict[str, Any] | None = None,
    prior_search_state: dict[str, Any] | None = None,
    new_evidence: str | None = None,
) -> str:
    return json.dumps(
        {
            "task": task,
            "context_trajectory": context or {},
            "constitution_orientation": constitution_packet or {},
            "prior_search_state": prior_search_state,
            "new_evidence": new_evidence,
            "instruction": (
                "Construct the observable relational-search state and abstract "
                "problem requirements. Do not select providers or grant authority."
            ),
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def validate_search_state_v003(state: dict[str, Any]) -> dict[str, Any]:
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
        "required_observations",
        "required_transformations",
        "required_actions",
        "required_external_interfaces",
        "constraints",
        "proposed_next_step",
        "return_localization",
    }
    missing = sorted(required_keys.difference(state))
    if missing:
        violations.append(f"missing keys: {missing}")

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

    if posture == "LAND" and warrant != "SUFFICIENT":
        violations.append("LAND requires warrant_status=SUFFICIENT")
    if posture == "LAND" and not str(state.get("provisional_landing") or "").strip():
        violations.append("LAND requires a provisional_landing")
    if posture == "RETURN" and not str(state.get("return_localization") or "").strip():
        violations.append("RETURN requires return_localization")
    if posture == "PROBE" and not (state.get("missing_information") or []):
        violations.append("PROBE should identify missing_information")

    req_validation = validate_problem_requirements(state)
    violations.extend(req_validation["violations"])

    return {
        "valid": not violations,
        "violations": violations,
        "requirements_valid": req_validation["valid"],
        "note": (
            "Structural validation only. It does not certify truth, completeness "
            "of decomposition, provider availability, or authority."
        ),
    }


def call_relational_search_v003(
    *,
    task: str,
    context: dict[str, Any] | None = None,
    constitution_packet: dict[str, Any] | None = None,
    prior_search_state: dict[str, Any] | None = None,
    new_evidence: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not MODEL:
        raise RuntimeError(
            "LUCIAN_MODEL is not configured. v0.3 intentionally has no default "
            "host model; select an approved project substrate explicitly."
        )

    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 1800, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_prompt(
                    task=task,
                    context=context,
                    constitution_packet=constitution_packet,
                    prior_search_state=prior_search_state,
                    new_evidence=new_evidence,
                ),
            },
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
    validation = validate_search_state_v003(state)
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
