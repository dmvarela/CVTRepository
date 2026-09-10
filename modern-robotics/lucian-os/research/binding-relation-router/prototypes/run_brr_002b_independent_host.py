"""Run frozen BRR-002B cases on an explicitly selected local Ollama host.

No default model is provided. The caller must name the host model explicitly.
The script performs independent calls for DIRECT_RESPONSE and RELATION_VECTOR
conditions and prints one JSON result object to stdout. It does not load,
download, or switch models itself.

Example from modern-robotics/lucian-os:
    py research/binding-relation-router/prototypes/run_brr_002b_independent_host.py --model <explicit-model-name>

To preserve a run:
    py research/binding-relation-router/prototypes/run_brr_002b_independent_host.py --model <explicit-model-name> > results/brr_002b_<host>.json
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PACKETS = ROOT / "research" / "binding-relation-router" / "manifests" / "brr_002b_raw_cases.json"

RESPONSE_CLASSES = [
    "ACT",
    "MEASURE_OR_RETRIEVE",
    "REVISE",
    "TRAVERSE",
    "PROBE_COMPETENCE",
    "ESCALATE_INTELLIGENCE",
    "DISCOVER_OR_CALIBRATE",
    "RECONFIGURE_OR_RECRUIT",
    "ASK_OR_HOLD",
    "REFUSE",
    "SCHEDULE_OR_SIMPLIFY",
    "REPORT_INFEASIBLE",
    "PRESERVE_OR_REPORT_INFEASIBLE",
    "SEARCH_OR_HOLD",
    "ABSTAIN",
]

DEFAULT_VECTOR = {
    "evidence": "PASS",
    "representation": "PASS",
    "competence": "SUFFICIENT",
    "capability": "AVAILABLE",
    "authority": "PASS",
    "resources": "SUFFICIENT",
    "viability": "OPEN",
    "search_path": "AVAILABLE",
}

DIRECT_SYSTEM = f"""You are participating in a simulation-only problem-diagnosis experiment.
Use only the supplied problem facts. Do not infer a negative fact from missing information.
Choose exactly one next-response class from this fixed vocabulary:
{', '.join(RESPONSE_CLASSES)}
Return JSON only with keys case_id, response, reason_short.
Do not expose private chain-of-thought; reason_short should be one concise evidence-bound explanation.
"""

VECTOR_SYSTEM = """You are participating in a simulation-only problem-diagnosis experiment.
Use only the supplied problem facts. Do not infer a negative fact from missing information, and do not soften an explicit blocker into uncertainty.

Return JSON only with keys:
case_id, relation_vector, binding_relation, reason_short

relation_vector must contain exactly:
evidence: PASS | UNKNOWN | CONTRADICTED
representation: PASS | BLOCKED
competence: SUFFICIENT | UNKNOWN | INSUFFICIENT
capability: AVAILABLE | UNKNOWN | ABSENT
authority: PASS | UNKNOWN | FAIL
resources: SUFFICIENT | TIGHT | INFEASIBLE
viability: OPEN | UNCERTAIN | CLOSED
search_path: AVAILABLE | UNKNOWN | ABSENT

binding_relation must be one of:
NONE
EVIDENCE_UNKNOWN
EVIDENCE_CONTRADICTED
REPRESENTATION_BLOCKED
COMPETENCE_UNKNOWN
COMPETENCE_INSUFFICIENT
CAPABILITY_UNKNOWN
CAPABILITY_ABSENT
AUTHORITY_UNKNOWN
AUTHORITY_FAIL
RESOURCES_TIGHT
RESOURCES_INFEASIBLE
VIABILITY_UNCERTAIN
VIABILITY_CLOSED
SEARCH_PATH_UNKNOWN
SEARCH_PATH_ABSENT

Do not expose private chain-of-thought; reason_short should be one concise evidence-bound explanation.
"""


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("No JSON object found in model response")
    return json.loads(text[start : end + 1])


def chat(url: str, model: str, system: str, user: str) -> tuple[str, dict[str, Any] | None]:
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {"temperature": 0},
    }
    req = urllib.request.Request(
        url.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    raw = body.get("message", {}).get("content", "")
    try:
        parsed = extract_json(raw)
    except Exception:
        parsed = None
    return raw, parsed


def route_vector(v: dict[str, str]) -> tuple[str | None, str | None]:
    checks = [
        (v.get("authority") == "FAIL", "AUTHORITY_FAIL", "REFUSE"),
        (v.get("viability") == "CLOSED", "VIABILITY_CLOSED", "PRESERVE_OR_REPORT_INFEASIBLE"),
        (v.get("resources") == "INFEASIBLE", "RESOURCES_INFEASIBLE", "REPORT_INFEASIBLE"),
        (v.get("evidence") == "CONTRADICTED", "EVIDENCE_CONTRADICTED", "REVISE"),
        (v.get("authority") == "UNKNOWN", "AUTHORITY_UNKNOWN", "ASK_OR_HOLD"),
        (v.get("evidence") == "UNKNOWN", "EVIDENCE_UNKNOWN", "MEASURE_OR_RETRIEVE"),
        (v.get("viability") == "UNCERTAIN", "VIABILITY_UNCERTAIN", "MEASURE_OR_RETRIEVE"),
        (v.get("capability") == "UNKNOWN", "CAPABILITY_UNKNOWN", "DISCOVER_OR_CALIBRATE"),
        (v.get("capability") == "ABSENT", "CAPABILITY_ABSENT", "RECONFIGURE_OR_RECRUIT"),
        (v.get("competence") == "UNKNOWN", "COMPETENCE_UNKNOWN", "PROBE_COMPETENCE"),
        (v.get("competence") == "INSUFFICIENT", "COMPETENCE_INSUFFICIENT", "ESCALATE_INTELLIGENCE"),
        (v.get("representation") == "BLOCKED", "REPRESENTATION_BLOCKED", "TRAVERSE"),
        (v.get("search_path") == "UNKNOWN", "SEARCH_PATH_UNKNOWN", "SEARCH_OR_HOLD"),
        (v.get("search_path") == "ABSENT", "SEARCH_PATH_ABSENT", "ABSTAIN"),
        (v.get("resources") == "TIGHT", "RESOURCES_TIGHT", "SCHEDULE_OR_SIMPLIFY"),
    ]
    for active, relation, response in checks:
        if active:
            return relation, response
    if all(v.get(k) == val for k, val in DEFAULT_VECTOR.items()):
        return "NONE", "ACT"
    return None, None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Explicit local Ollama model name; no project default is inherited.")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434", help="Local Ollama base URL.")
    args = parser.parse_args()

    data = json.loads(PACKETS.read_text(encoding="utf-8"))
    rows = []

    for case in data["cases"]:
        case_id = case["case_id"]
        problem = case["problem"]
        user = f"case_id: {case_id}\nproblem: {problem}"

        direct_raw, direct = chat(args.ollama_url, args.model, DIRECT_SYSTEM, user)
        vector_raw, vector_product = chat(args.ollama_url, args.model, VECTOR_SYSTEM, user)

        detected_vector = None
        routed_binding = None
        routed_response = None
        if isinstance(vector_product, dict) and isinstance(vector_product.get("relation_vector"), dict):
            detected_vector = vector_product["relation_vector"]
            routed_binding, routed_response = route_vector(detected_vector)

        rows.append({
            "case_id": case_id,
            "direct_raw": direct_raw,
            "direct_parsed": direct,
            "vector_raw": vector_raw,
            "vector_parsed": vector_product,
            "kernel_binding_relation": routed_binding,
            "kernel_response": routed_response,
        })

    result = {
        "experiment": "BRR-002B",
        "run_class": "independent_host_candidate",
        "model": args.model,
        "ollama_url": args.ollama_url,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "temperature": 0,
        "raw_packet_commit": "2459ecc4f45952a321a03c81a0ae08f40b3d7731",
        "note": "Evaluator labels are not loaded by this runner. Model selection is explicit and no project default model is inherited.",
        "rows": rows,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as exc:
        raise SystemExit(f"Local model call failed: {exc}") from exc
