"""Technical JSON-schema bench for the locked Ministral/Ollama runtime.

From modern-robotics/lucian-os:
    py prototype/run_ministral_json_schema_bench_001.py

This is NOT an RVT experimental run. It uses unrelated synthetic routing cards
and exists only to choose the response-interface policy for RVT-INTERP-003.
No selective retries are performed.
"""

from __future__ import annotations

import hashlib
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PROJECT_ROOT / "manifests" / "ministral_json_schema_bench_001.json"
RESULTS_DIR = PROJECT_ROOT / "results"
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434").rstrip("/")
CHAT_URL = f"{OLLAMA_BASE}/api/chat"
TAGS_URL = f"{OLLAMA_BASE}/api/tags"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_digest(value: str) -> str:
    value = value.strip().lower()
    if value.startswith("sha256:"):
        value = value.split(":", 1)[1]
    return value


def load_manifest() -> tuple[dict[str, Any], str]:
    raw = MANIFEST_PATH.read_text(encoding="utf-8")
    m = json.loads(raw)
    if m.get("status") != "technical-bench-frozen":
        raise RuntimeError(f"Bench manifest is not frozen: {m.get('status')!r}")
    return m, sha256_text(raw)


def fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def verify_model_identity(m: dict[str, Any]) -> dict[str, Any]:
    expected_tag = m["model"]["tag"]
    expected_id = normalize_digest(m["model"]["observed_model_id"])
    tags = fetch_json(TAGS_URL)
    models = tags.get("models", [])
    match = next((x for x in models if x.get("name") == expected_tag), None)
    if match is None:
        raise RuntimeError(f"Locked model {expected_tag!r} not found.")
    digest = normalize_digest(str(match.get("digest", "")))
    if digest and not digest.startswith(expected_id):
        raise RuntimeError(
            f"Model digest mismatch: expected prefix {expected_id}, observed {digest}"
        )
    return {
        "name": match.get("name"),
        "digest": str(match.get("digest", "")),
        "normalized_digest": digest,
        "size": match.get("size"),
    }


def validate_schema_object(obj: Any, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["top_level_not_object"]

    required = list(schema["required"])
    allowed = set(schema["properties"].keys())
    actual = set(obj.keys())

    missing = [k for k in required if k not in obj]
    extra = sorted(actual - allowed)
    if missing:
        errors.append("missing_keys:" + ",".join(missing))
    if extra:
        errors.append("extra_keys:" + ",".join(extra))

    for key, spec in schema["properties"].items():
        if key not in obj:
            continue
        value = obj[key]
        expected_type = spec.get("type")
        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"{key}:not_string")
            continue
        if expected_type == "integer" and (
            not isinstance(value, int) or isinstance(value, bool)
        ):
            errors.append(f"{key}:not_integer")
            continue
        if "enum" in spec and value not in spec["enum"]:
            errors.append(f"{key}:enum_violation:{value!r}")
        if isinstance(value, int) and not isinstance(value, bool):
            if "minimum" in spec and value < spec["minimum"]:
                errors.append(f"{key}:below_minimum")
            if "maximum" in spec and value > spec["maximum"]:
                errors.append(f"{key}:above_maximum")
    return errors


def call_model(
    m: dict[str, Any], prompt: str, seed: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    sampling = m["sampling"]
    messages = [
        {
            "role": "system",
            "content": (
                "You are completing an unrelated synthetic routing-card task. "
                "Return only the structured object required by the supplied schema."
            ),
        },
        {"role": "user", "content": prompt},
    ]
    payload = {
        "model": m["model"]["tag"],
        "stream": False,
        "think": bool(sampling["think"]),
        "format": m["schema"],
        "options": {
            "temperature": sampling["temperature"],
            "top_p": sampling["top_p"],
            "num_predict": sampling["num_predict"],
            "num_ctx": sampling["num_ctx"],
            "seed": seed,
        },
        "messages": messages,
    }
    request = urllib.request.Request(
        CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        raw_body = json.loads(response.read().decode("utf-8"))
    return payload, raw_body


def main() -> None:
    m, manifest_sha = load_manifest()

    forbidden_fragments = [
        "K17",
        "temperature",
        "vibration",
        "shutdown",
        "correction",
        "hypothesis",
        "preserve",
        "revise",
        "self-sealing",
        "survivable",
    ]
    corpus = json.dumps(m["dummy_prompts"], ensure_ascii=False).lower()
    hits = [x for x in forbidden_fragments if x.lower() in corpus]
    if hits:
        raise RuntimeError(f"Contamination audit failed; forbidden terms found: {hits}")

    expected_runs = len(m["dummy_prompts"]) * len(m["sampling"]["seeds"])
    print("MINISTRAL_JSON_SCHEMA_BENCH_001")
    print(f"Manifest SHA256: {manifest_sha}")
    print(f"Locked model: {m['model']['tag']}")
    print(f"Planned calls: {expected_runs}")
    print("Contamination audit PASS")

    model_identity = verify_model_identity(m)
    print(f"Model preflight PASS: {model_identity}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"ministral_json_schema_bench_001_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"ministral_json_schema_bench_001_{stamp}_summary.json"

    rows: list[dict[str, Any]] = []
    run_index = 0
    with out_path.open("w", encoding="utf-8") as out:
        for prompt_index, prompt in enumerate(m["dummy_prompts"], start=1):
            for seed in m["sampling"]["seeds"]:
                run_index += 1
                print(
                    f"[{run_index:02d}/{expected_runs}] "
                    f"prompt={prompt_index} seed={seed}"
                )
                row: dict[str, Any] = {
                    "bench_id": m["bench_id"],
                    "manifest_sha256": manifest_sha,
                    "prompt_index": prompt_index,
                    "seed": seed,
                    "prompt_sha256": sha256_text(prompt),
                    "request": None,
                    "raw_response": None,
                    "parsed": None,
                    "parse_error": None,
                    "schema_errors": [],
                    "conforming": False,
                }
                try:
                    payload, raw_body = call_model(m, prompt, seed)
                    row["request"] = payload
                    row["raw_response"] = raw_body
                    content = str(
                        raw_body.get("message", {}).get("content", "")
                    ).strip()
                    try:
                        parsed = json.loads(content)
                        row["parsed"] = parsed
                    except json.JSONDecodeError as exc:
                        row["parse_error"] = f"json_decode_error:{exc}"
                        parsed = None

                    if parsed is not None:
                        row["schema_errors"] = validate_schema_object(
                            parsed, m["schema"]
                        )
                        row["conforming"] = len(row["schema_errors"]) == 0
                except Exception as exc:
                    row["parse_error"] = f"call_error:{type(exc).__name__}:{exc}"

                rows.append(row)
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()

    n_conforming = sum(bool(x["conforming"]) for x in rows)
    n_parseable = sum(x["parsed"] is not None for x in rows)
    summary = {
        "bench_id": m["bench_id"],
        "manifest_sha256": manifest_sha,
        "model_identity": model_identity,
        "n_total": len(rows),
        "n_parseable": n_parseable,
        "n_conforming": n_conforming,
        "pass_rule": m["pass_rule"],
        "bench_pass": n_conforming == len(rows),
        "failures": [
            {
                "prompt_index": x["prompt_index"],
                "seed": x["seed"],
                "parse_error": x["parse_error"],
                "schema_errors": x["schema_errors"],
            }
            for x in rows
            if not x["conforming"]
        ],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("")
    print(f"Raw results: {out_path}")
    print(f"Summary:     {summary_path}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if summary["bench_pass"]:
        print("")
        print("SCHEMA BENCH PASS — strict JSON Schema is eligible for RVT-INTERP-003.")
    else:
        print("")
        print("SCHEMA BENCH FAIL — do not use strict JSON Schema for RVT-INTERP-003 yet.")


if __name__ == "__main__":
    main()
