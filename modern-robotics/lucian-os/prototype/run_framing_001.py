"""Run FRAMING_001 against a local Ollama host.

Simulation only. No external actions are executed.
Run from modern-robotics/lucian-os:
    py prototype/run_framing_001.py

Optional environment variables:
    LUCIAN_MODEL=qwen3.5:2b-q4_K_M
    OLLAMA_URL=http://localhost:11434/api/chat

The runner preserves raw model products plus structural validation. It does not
score semantic correctness automatically; compare against the frozen manifest.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lucian_router import extract_json
from problem_framing_v001 import validate_framing_state

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = PROJECT_ROOT / "manifests" / "framing_001_cases.json"
RESULTS_DIR = PROJECT_ROOT / "results"
MODEL = os.environ.get("LUCIAN_MODEL", "qwen3.5:2b-q4_K_M")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")

SYSTEM_PROMPT = """You are a development host inside a simulation-only Lucian OS framing experiment.
Your task is to represent the shape of a human request before any capability composition or action.

Rules:
1. Preserve the human-owned objective and all explicit constraints.
2. Distinguish the stated objective from implementation assumptions.
3. Do not invent hidden desires or a deeper objective merely to appear insightful.
4. Reframe only when there is a material structural mismatch between the stated implementation and the objective.
5. A proposed reframe is not authorization to act.
6. If the objective is materially underspecified, use ASK_OR_HOLD rather than manufacturing intent.
7. If the request is already adequate, use EXECUTE_AS_FRAMED; do not reframe for novelty.
8. Use only the supplied request. Do not claim any action was executed.
9. Return JSON only. Do not expose private hidden chain-of-thought.

Return exactly these top-level keys:
surface_request, objective, constraints, implementation_assumptions,
problem_shape, structural_mismatch, framing_disposition, proposed_reframe

Schema:
- objective = {"text": string, "source": "USER"|"CONTEXT"|"INFERRED"}
- constraints = [{"text": string, "source": "USER"|"CONTEXT"|"INFERRED"}, ...]
- implementation_assumptions = [{"text": string, "source": "USER"|"CONTEXT"|"INFERRED"}, ...]
- structural_mismatch = {"present": boolean, "basis": string}
- framing_disposition = "EXECUTE_AS_FRAMED" | "REFRAME_AND_PROPOSE" | "ASK_OR_HOLD"
- proposed_reframe = string; use empty string unless framing_disposition is REFRAME_AND_PROPOSE
"""


def load_cases() -> dict[str, Any]:
    with CASES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def call_host(request_text: str) -> tuple[dict[str, Any], dict[str, Any], str]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 1000, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "human_request": request_text,
                        "instruction": "Produce the framing product only. Do not execute anything.",
                    },
                    ensure_ascii=False,
                ),
            },
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_URL}. Is Ollama running?\n{exc}"
        ) from exc

    raw_content = body.get("message", {}).get("content", "")
    model_view = extract_json(raw_content)
    metrics = {
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "total_duration": body.get("total_duration"),
        "load_duration": body.get("load_duration"),
        "prompt_eval_duration": body.get("prompt_eval_duration"),
        "eval_duration": body.get("eval_duration"),
        "done_reason": body.get("done_reason"),
    }
    return model_view, metrics, raw_content


def main() -> None:
    suite = load_cases()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_model = MODEL.replace(":", "_").replace("/", "_")
    output_path = RESULTS_DIR / f"FRAMING_001_{safe_model}_{timestamp}.json"

    records: list[dict[str, Any]] = []
    for case in suite.get("cases", []):
        case_id = str(case.get("case_id"))
        request_text = str(case.get("request"))
        try:
            model_view, metrics, raw_content = call_host(request_text)
            validation = validate_framing_state(model_view)
            record = {
                "case_id": case_id,
                "request": request_text,
                "expected_disposition": case.get("expected_disposition"),
                "model_product": model_view,
                "structural_validation": validation,
                "host_metrics": metrics,
                "raw_content": raw_content,
                "error": None,
            }
        except Exception as exc:  # preserve failure instead of hiding it
            record = {
                "case_id": case_id,
                "request": request_text,
                "expected_disposition": case.get("expected_disposition"),
                "model_product": None,
                "structural_validation": None,
                "host_metrics": None,
                "raw_content": None,
                "error": f"{type(exc).__name__}: {exc}",
            }
        records.append(record)
        print(
            case_id,
            "expected=",
            case.get("expected_disposition"),
            "observed=",
            (record.get("model_product") or {}).get("framing_disposition"),
            "valid=",
            (record.get("structural_validation") or {}).get("valid"),
        )

    artifact = {
        "experiment_id": suite.get("experiment_id"),
        "suite_version": suite.get("version"),
        "model": MODEL,
        "ollama_url": OLLAMA_URL,
        "run_utc": timestamp,
        "simulation_only": True,
        "semantic_scoring_status": "UNSCORED",
        "records": records,
    }

    output_path.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nPreserved run: {output_path}")
    print("Semantic scoring remains manual/frozen-rubric; do not retune from this run.")


if __name__ == "__main__":
    main()
