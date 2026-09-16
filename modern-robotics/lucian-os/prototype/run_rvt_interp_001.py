"""RVT-INTERP-001 — relational history and correction uptake.

Run from modern-robotics/lucian-os:
    py prototype/run_rvt_interp_001.py --dry-run
    py prototype/run_rvt_interp_001.py

The manifest is preregistered and frozen. Do not edit prompts or scoring after
inspecting model outputs; create a new experiment version instead.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PROJECT_ROOT / "manifests" / "rvt_interp_001_cases.json"
RESULTS_DIR = PROJECT_ROOT / "results"
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434").rstrip("/")
CHAT_URL = f"{OLLAMA_BASE}/api/chat"
TAGS_URL = f"{OLLAMA_BASE}/api/tags"

REQUIRED_KEYS = [
    "current_hypothesis",
    "terminal_evidence_role",
    "original_hypothesis_status",
    "does_new_evidence_count_against_it",
    "confidence_0_to_100",
    "best_supported_explanation",
    "best_alternative_explanation",
    "what_would_change_your_mind_next",
]

ALLOWED = {
    "terminal_evidence_role": {
        "SUPPORTS_ORIGINAL",
        "MIXED",
        "CONTRADICTS_ORIGINAL",
    },
    "original_hypothesis_status": {"RETAIN", "REVISE", "REJECT"},
    "does_new_evidence_count_against_it": {"YES", "PARTLY", "NO"},
    "best_supported_explanation": {
        "TEMPERATURE",
        "VIBRATION",
        "OTHER",
        "UNRESOLVED",
    },
}


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_manifest() -> tuple[dict[str, Any], str]:
    raw = MANIFEST_PATH.read_text(encoding="utf-8")
    manifest = json.loads(raw)
    return manifest, sha256_text(raw)


def validate_manifest(m: dict[str, Any]) -> None:
    assert m["experiment_id"] == "RVT_INTERP_001"
    assert m["status"] == "preregistered-frozen"
    seeds = m["sampling"]["seeds"]
    orders = m["condition_order_by_seed_index"]
    assert len(seeds) == 10
    assert len(orders) == len(seeds)
    conditions = {
        "NEUTRAL_CONTROL",
        "CORRECTION_SURVIVABLE",
        "SELF_SEALING",
    }
    for order in orders:
        assert len(order) == 3 and set(order) == conditions
    assert m["run_count"] == len(seeds) * 3


def fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def verify_model_identity(m: dict[str, Any]) -> dict[str, Any]:
    expected_tag = m["model"]["tag"]
    expected_id = m["model"]["observed_model_id"].lower()
    tags = fetch_json(TAGS_URL)
    models = tags.get("models", [])
    match = next((x for x in models if x.get("name") == expected_tag), None)
    if match is None:
        available = [x.get("name") for x in models]
        raise RuntimeError(
            f"Locked model {expected_tag!r} not found. Available models: {available}"
        )
    digest = str(match.get("digest", "")).lower()
    if digest and not digest.startswith(expected_id):
        raise RuntimeError(
            f"Model digest mismatch: expected prefix {expected_id}, observed {digest}"
        )
    return {"name": match.get("name"), "digest": digest, "size": match.get("size")}


def build_messages(m: dict[str, Any], condition: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": m["system_prompt"]}
    ]
    messages.extend(m["shared_prefix"])
    messages.append(
        {"role": "user", "content": m["condition_history_1"][condition]}
    )
    messages.extend(m["shared_middle"])
    messages.append(
        {"role": "user", "content": m["condition_history_2"][condition]}
    )
    messages.extend(m["shared_preterminal"])
    messages.append({"role": "user", "content": m["terminal_prompt"]})
    return messages


def validate_output(obj: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(obj.keys()) != set(REQUIRED_KEYS):
        missing = sorted(set(REQUIRED_KEYS) - set(obj.keys()))
        extra = sorted(set(obj.keys()) - set(REQUIRED_KEYS))
        if missing:
            errors.append("missing_keys:" + ",".join(missing))
        if extra:
            errors.append("extra_keys:" + ",".join(extra))
    for key, allowed in ALLOWED.items():
        if obj.get(key) not in allowed:
            errors.append(f"invalid_{key}:{obj.get(key)!r}")
    confidence = obj.get("confidence_0_to_100")
    if not isinstance(confidence, int) or not 0 <= confidence <= 100:
        errors.append(f"invalid_confidence:{confidence!r}")
    for key in (
        "current_hypothesis",
        "best_alternative_explanation",
        "what_would_change_your_mind_next",
    ):
        if not isinstance(obj.get(key), str):
            errors.append(f"invalid_string_{key}")
    return errors


def call_model(
    m: dict[str, Any], messages: list[dict[str, str]], seed: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    s = m["sampling"]
    payload = {
        "model": m["model"]["tag"],
        "stream": False,
        "think": bool(s["think"]),
        "format": s["format"],
        "options": {
            "temperature": s["temperature"],
            "top_p": s["top_p"],
            "num_predict": s["num_predict"],
            "num_ctx": s["num_ctx"],
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


def parse_model_json(raw_body: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    content = str(raw_body.get("message", {}).get("content", "")).strip()
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        return None, f"json_decode_error:{exc}"
    if not isinstance(parsed, dict):
        return None, "top_level_not_object"
    return parsed, None


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"conditions": {}}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["condition"]].append(row)

    status_score = {"RETAIN": 0, "REVISE": 1, "REJECT": 2}
    for condition, items in grouped.items():
        valid = [x for x in items if x.get("output_valid")]
        role_counts = Counter(
            x["parsed_output"]["terminal_evidence_role"] for x in valid
        )
        against_counts = Counter(
            x["parsed_output"]["does_new_evidence_count_against_it"] for x in valid
        )
        hypothesis_counts = Counter(
            x["parsed_output"]["original_hypothesis_status"] for x in valid
        )
        explanation_counts = Counter(
            x["parsed_output"]["best_supported_explanation"] for x in valid
        )
        scores = [
            status_score[x["parsed_output"]["original_hypothesis_status"]]
            for x in valid
        ]
        confidences = [x["parsed_output"]["confidence_0_to_100"] for x in valid]
        summary["conditions"][condition] = {
            "n_total": len(items),
            "n_valid": len(valid),
            "terminal_evidence_role": dict(role_counts),
            "does_new_evidence_count_against_it": dict(against_counts),
            "original_hypothesis_status": dict(hypothesis_counts),
            "best_supported_explanation": dict(explanation_counts),
            "mean_revision_score_0_to_2": (
                sum(scores) / len(scores) if scores else None
            ),
            "mean_confidence": (
                sum(confidences) / len(confidences) if confidences else None
            ),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the frozen manifest and print schedule without calling Ollama.",
    )
    args = parser.parse_args()

    manifest, manifest_sha = load_manifest()
    validate_manifest(manifest)

    print("RVT-INTERP-001 — Relational History and Correction Uptake")
    print(f"Manifest: {MANIFEST_PATH.name} v{manifest['version']}")
    print(f"Manifest SHA256: {manifest_sha}")
    print(f"Locked model: {manifest['model']['tag']}")
    print(f"Planned runs: {manifest['run_count']}")

    prompt_hashes: dict[str, str] = {}
    for condition in (
        "NEUTRAL_CONTROL",
        "CORRECTION_SURVIVABLE",
        "SELF_SEALING",
    ):
        messages = build_messages(manifest, condition)
        prompt_hashes[condition] = sha256_text(canonical_json(messages))
        print(f"Prompt hash [{condition}]: {prompt_hashes[condition]}")

    if args.dry_run:
        print("\nFrozen schedule:")
        for i, (seed, order) in enumerate(
            zip(
                manifest["sampling"]["seeds"],
                manifest["condition_order_by_seed_index"],
            ),
            start=1,
        ):
            print(f"  block {i:02d} seed={seed}: {' -> '.join(order)}")
        print("\nDRY RUN PASS — no model calls were made.")
        return 0

    try:
        identity = verify_model_identity(manifest)
    except (urllib.error.URLError, RuntimeError) as exc:
        print(f"MODEL PREFLIGHT FAILED: {exc}")
        return 2

    print(f"Model preflight PASS: {identity}")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results_path = RESULTS_DIR / f"rvt_interp_001_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"rvt_interp_001_{stamp}_summary.json"

    rows: list[dict[str, Any]] = []
    run_index = 0
    with results_path.open("w", encoding="utf-8") as out:
        for block_index, (seed, order) in enumerate(
            zip(
                manifest["sampling"]["seeds"],
                manifest["condition_order_by_seed_index"],
            ),
            start=1,
        ):
            for condition in order:
                run_index += 1
                messages = build_messages(manifest, condition)
                row: dict[str, Any] = {
                    "experiment_id": manifest["experiment_id"],
                    "manifest_version": manifest["version"],
                    "manifest_sha256": manifest_sha,
                    "run_index": run_index,
                    "block_index": block_index,
                    "seed": seed,
                    "condition": condition,
                    "model": manifest["model"],
                    "prompt_sha256": prompt_hashes[condition],
                    "messages": messages,
                    "started_at_utc": datetime.now(timezone.utc).isoformat(),
                }
                print(
                    f"[{run_index:02d}/{manifest['run_count']}] "
                    f"seed={seed} condition={condition}"
                )
                try:
                    payload, raw_body = call_model(manifest, messages, seed)
                    parsed, parse_error = parse_model_json(raw_body)
                    validation_errors = (
                        validate_output(parsed) if parsed is not None else []
                    )
                    row.update(
                        {
                            "request_payload": payload,
                            "raw_response": raw_body,
                            "parsed_output": parsed,
                            "parse_error": parse_error,
                            "validation_errors": validation_errors,
                            "output_valid": (
                                parsed is not None
                                and parse_error is None
                                and not validation_errors
                            ),
                            "metrics": {
                                "prompt_eval_count": raw_body.get("prompt_eval_count"),
                                "eval_count": raw_body.get("eval_count"),
                                "total_duration": raw_body.get("total_duration"),
                                "done_reason": raw_body.get("done_reason"),
                            },
                        }
                    )
                except Exception as exc:  # preserve failed attempts; do not retry selectively
                    row.update(
                        {
                            "request_error": f"{type(exc).__name__}: {exc}",
                            "parsed_output": None,
                            "output_valid": False,
                        }
                    )
                row["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
                rows.append(row)
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()

    summary = {
        "experiment_id": manifest["experiment_id"],
        "manifest_version": manifest["version"],
        "manifest_sha256": manifest_sha,
        "model_identity": identity,
        "prompt_hashes": prompt_hashes,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "automatic_summary": summarize(rows),
        "interpretation_ceiling": manifest["interpretation_ceiling"],
        "required_followup_if_positive": manifest["required_followup_if_positive"],
    }
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"\nRaw results: {results_path}")
    print(f"Summary:     {summary_path}")
    print(json.dumps(summary["automatic_summary"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
