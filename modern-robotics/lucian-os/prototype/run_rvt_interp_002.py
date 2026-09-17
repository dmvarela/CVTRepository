"""RVT-INTERP-002 — flattened-history lexical / semantic priming ablation.

From modern-robotics/lucian-os:
    py prototype/run_rvt_interp_002.py --dry-run

The first committed manifest is a freeze candidate. --dry-run performs the
parent-equivalence audit and prints the exact schedule and prompt hashes without
calling Ollama. Actual model execution is refused until the manifest status is
changed, before any outputs are observed, to `preregistered-frozen`.
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
MANIFEST_PATH = PROJECT_ROOT / "manifests" / "rvt_interp_002_cases.json"
RESULTS_DIR = PROJECT_ROOT / "results"
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434").rstrip("/")
CHAT_URL = f"{OLLAMA_BASE}/api/chat"
TAGS_URL = f"{OLLAMA_BASE}/api/tags"

PRIMARY_FIELDS = [
    "original_hypothesis_status",
    "does_new_evidence_count_against_it",
    "best_supported_explanation",
    "terminal_evidence_role",
]


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw), sha256_text(raw)


def parent_path(m: dict[str, Any]) -> Path:
    return PROJECT_ROOT / m["parent_manifest_path"]


def normalize_digest(value: str) -> str:
    value = value.strip().lower()
    if value.startswith("sha256:"):
        value = value.split(":", 1)[1]
    return value


def validate_structure(m: dict[str, Any]) -> None:
    assert m["experiment_id"] == "RVT_INTERP_002"
    assert m["status"] in {"preregistered-freeze-candidate", "preregistered-frozen"}
    seeds = m["sampling"]["seeds"]
    orders = m["condition_order_by_seed_index"]
    annotation_orders = m["annotation_order_by_seed_index"]
    assert len(seeds) == 10
    assert len(orders) == len(seeds)
    assert len(annotation_orders) == len(seeds)
    expected_conditions = {
        "NEUTRAL_CONTROL",
        "CORRECTION_SURVIVABLE",
        "SELF_SEALING",
    }
    for order in orders:
        assert len(order) == 3 and set(order) == expected_conditions
    assert all(x in {"A_B", "B_A"} for x in annotation_orders)
    assert m["run_count"] == len(seeds) * 3


def audit_against_parent(m: dict[str, Any], parent: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(ok), "detail": detail})

    check("parent_experiment_id", parent.get("experiment_id") == "RVT_INTERP_001")
    check("model_tag_equal", m["model"]["tag"] == parent["model"]["tag"])
    check(
        "model_id_prefix_equal",
        m["model"]["observed_model_id"] == parent["model"]["observed_model_id"],
    )
    check("sampling_equal", m["sampling"] == parent["sampling"])
    check(
        "condition_order_equal",
        m["condition_order_by_seed_index"] == parent["condition_order_by_seed_index"],
    )

    expected_initial = parent["shared_prefix"][0]["content"]
    check("initial_statement_verbatim", m["initial_statement"] == expected_initial)

    expected_observations = [
        parent["shared_prefix"][2]["content"],
        parent["shared_prefix"][4]["content"],
        parent["shared_prefix"][6]["content"],
        parent["shared_middle"][1]["content"],
    ]
    check(
        "runs_1_to_4_verbatim",
        m["factual_observations"] == expected_observations,
    )

    annotation_ok = True
    annotation_details: list[str] = []
    for condition in (
        "NEUTRAL_CONTROL",
        "CORRECTION_SURVIVABLE",
        "SELF_SEALING",
    ):
        a_ok = m["annotations"][condition]["A"] == parent["condition_history_1"][condition]
        b_ok = m["annotations"][condition]["B"] == parent["condition_history_2"][condition]
        annotation_ok = annotation_ok and a_ok and b_ok
        annotation_details.append(f"{condition}:A={a_ok},B={b_ok}")
    check("annotations_verbatim", annotation_ok, "; ".join(annotation_details))

    terminal_evidence = m["terminal_evidence_text"]
    parent_terminal = parent["terminal_prompt"]
    check(
        "terminal_evidence_exact_prefix",
        parent_terminal.startswith(terminal_evidence),
    )

    expected_system = parent["system_prompt"].replace(
        "Earlier dialogue is historical context",
        "Earlier material is historical context",
        1,
    )
    check(
        "system_only_dialogue_to_material_change",
        m["system_prompt"] == expected_system,
    )

    parent_instruction = parent_terminal[len(terminal_evidence):].strip()
    expected_terminal_instruction = parent_instruction.replace(
        "Earlier requests about whether to preserve or revise H_T",
        "Earlier annotations about whether to preserve or revise H_T",
        1,
    )
    check(
        "terminal_only_requests_to_annotations_change",
        m["terminal_instruction"] == expected_terminal_instruction,
    )

    expected_annotation_orders = [
        "A_B" if i % 2 == 1 else "B_A" for i in range(1, 11)
    ]
    check(
        "annotation_order_rule",
        m["annotation_order_by_seed_index"] == expected_annotation_orders,
    )

    prompt_shape_ok = True
    for condition in (
        "NEUTRAL_CONTROL",
        "CORRECTION_SURVIVABLE",
        "SELF_SEALING",
    ):
        for annotation_order in ("A_B", "B_A"):
            messages = build_messages(m, condition, annotation_order)
            prompt_shape_ok = prompt_shape_ok and len(messages) == 3
            prompt_shape_ok = prompt_shape_ok and all(
                msg["role"] != "assistant" for msg in messages
            )
    check(
        "flat_prompt_has_no_assistant_turns",
        prompt_shape_ok,
        "Expected exactly system + flat dossier user + terminal user messages.",
    )

    return {
        "passed": all(x["passed"] for x in checks),
        "checks": checks,
    }


def build_dossier(m: dict[str, Any], condition: str, annotation_order: str) -> str:
    annotations = m["annotations"][condition]
    keys = ["A", "B"] if annotation_order == "A_B" else ["B", "A"]
    lines = [
        m["flat_dossier_wrapper"],
        "",
        "INITIAL WORKING STATEMENT:",
        m["initial_statement"],
        "",
        "FACTUAL OBSERVATIONS:",
    ]
    lines.extend(m["factual_observations"])
    lines.extend(
        [
            "",
            "HISTORICAL ANNOTATIONS (source and temporal ordering unavailable):",
            f"Annotation 1: {annotations[keys[0]]}",
            f"Annotation 2: {annotations[keys[1]]}",
        ]
    )
    return "\n".join(lines)


def build_messages(
    m: dict[str, Any], condition: str, annotation_order: str
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": m["system_prompt"]},
        {"role": "user", "content": build_dossier(m, condition, annotation_order)},
        {
            "role": "user",
            "content": m["terminal_evidence_text"] + " " + m["terminal_instruction"],
        },
    ]


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
        available = [x.get("name") for x in models]
        raise RuntimeError(
            f"Locked model {expected_tag!r} not found. Available models: {available}"
        )
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


def call_model(
    m: dict[str, Any], messages: list[dict[str, str]], seed: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    sampling = m["sampling"]
    payload = {
        "model": m["model"]["tag"],
        "stream": False,
        "think": bool(sampling["think"]),
        "format": sampling["format"],
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


def parse_model_json(raw_body: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    content = str(raw_body.get("message", {}).get("content", "")).strip()
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        return None, f"json_decode_error:{exc}"
    if not isinstance(parsed, dict):
        return None, "top_level_not_object"
    return parsed, None


def allowed_primary(m: dict[str, Any], field: str) -> set[str]:
    spec = m["primary_fields"][field]
    if isinstance(spec, dict):
        return set(spec.keys())
    return set(spec)


def extract_primary(m: dict[str, Any], parsed: dict[str, Any] | None) -> dict[str, Any]:
    out: dict[str, Any] = {
        "parse_valid": isinstance(parsed, dict),
        "fields": {},
        "normalized_confidence": None,
        "normalization_source": None,
    }
    if not isinstance(parsed, dict):
        for field in PRIMARY_FIELDS:
            out["fields"][field] = {
                "value": None,
                "conforming": False,
                "reason": "no_parseable_object",
            }
        return out

    for field in PRIMARY_FIELDS:
        value = parsed.get(field)
        conforming = value in allowed_primary(m, field)
        out["fields"][field] = {
            "value": value,
            "conforming": conforming,
            "reason": None if conforming else "missing_or_nonallowed_value",
        }

    confidence = parsed.get("confidence_0_to_100")
    if isinstance(confidence, int) and 0 <= confidence <= 100:
        out["normalized_confidence"] = confidence
        out["normalization_source"] = "confidence_0_to_100"
    else:
        alias = parsed.get("confidence")
        if isinstance(alias, int) and 0 <= alias <= 100:
            out["normalized_confidence"] = alias
            out["normalization_source"] = "confidence_alias"
    return out


def summarize(m: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_seed: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        grouped[row["condition"]].append(row)
        by_seed[int(row["seed"])][row["condition"]] = row

    summary: dict[str, Any] = {"conditions": {}, "paired_contrasts": {}}
    for condition, items in grouped.items():
        c: dict[str, Any] = {
            "n_total": len(items),
            "n_parse_valid": sum(
                bool(x.get("primary_extraction", {}).get("parse_valid")) for x in items
            ),
        }
        for field in PRIMARY_FIELDS:
            values = [
                x["primary_extraction"]["fields"][field]["value"]
                for x in items
                if x["primary_extraction"]["fields"][field]["conforming"]
            ]
            c[field] = {
                "n_conforming": len(values),
                "counts": dict(Counter(values)),
            }
            spec = m["primary_fields"][field]
            if isinstance(spec, dict):
                scores = [spec[v] for v in values]
                c[field]["mean_score"] = sum(scores) / len(scores) if scores else None
        aliases = Counter(
            x["primary_extraction"].get("normalization_source") for x in items
        )
        c["confidence_interface"] = dict(aliases)
        summary["conditions"][condition] = c

    for field in (
        "original_hypothesis_status",
        "does_new_evidence_count_against_it",
    ):
        score_map = m["primary_fields"][field]
        diffs: list[int] = []
        neutral_between: list[bool] = []
        for seed in m["sampling"]["seeds"]:
            triplet = by_seed.get(seed, {})
            if set(triplet) != {
                "CORRECTION_SURVIVABLE",
                "SELF_SEALING",
                "NEUTRAL_CONTROL",
            }:
                continue
            values: dict[str, int] = {}
            for condition, row in triplet.items():
                f = row["primary_extraction"]["fields"][field]
                if f["conforming"]:
                    values[condition] = score_map[f["value"]]
            if len(values) == 3:
                s = values["CORRECTION_SURVIVABLE"]
                n = values["NEUTRAL_CONTROL"]
                ss = values["SELF_SEALING"]
                diffs.append(s - ss)
                neutral_between.append(min(s, ss) <= n <= max(s, ss))
        summary["paired_contrasts"][field] = {
            "n_complete_triplets": len(diffs),
            "survivable_minus_self_sealing": {
                "positive": sum(d > 0 for d in diffs),
                "tie": sum(d == 0 for d in diffs),
                "negative": sum(d < 0 for d in diffs),
                "mean_difference": sum(diffs) / len(diffs) if diffs else None,
            },
            "neutral_between_endpoints": {
                "yes": sum(neutral_between),
                "no": len(neutral_between) - sum(neutral_between),
            },
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run freeze audit and print hashes/schedule without calling Ollama.",
    )
    args = parser.parse_args()

    manifest, manifest_sha = load_json(MANIFEST_PATH)
    validate_structure(manifest)
    parent, parent_sha = load_json(parent_path(manifest))
    audit = audit_against_parent(manifest, parent)

    print("RVT-INTERP-002 — Flattened-History Lexical / Semantic Priming Ablation")
    print(f"Manifest: {MANIFEST_PATH.name} v{manifest['version']}")
    print(f"Status: {manifest['status']}")
    print(f"Manifest SHA256: {manifest_sha}")
    print(f"Parent manifest SHA256: {parent_sha}")
    print(f"Locked model: {manifest['model']['tag']}")
    print(f"Planned runs: {manifest['run_count']}")
    print("\nFreeze audit:")
    for check in audit["checks"]:
        label = "PASS" if check["passed"] else "FAIL"
        detail = f" — {check['detail']}" if check.get("detail") else ""
        print(f"  [{label}] {check['name']}{detail}")
    if not audit["passed"]:
        print("\nFREEZE AUDIT FAILED — do not execute.")
        return 2

    prompt_hashes: dict[str, str] = {}
    print("\nFrozen candidate schedule and prompt hashes:")
    for i, (seed, order, annotation_order) in enumerate(
        zip(
            manifest["sampling"]["seeds"],
            manifest["condition_order_by_seed_index"],
            manifest["annotation_order_by_seed_index"],
        ),
        start=1,
    ):
        print(
            f"  block {i:02d} seed={seed} annotations={annotation_order}: "
            + " -> ".join(order)
        )
        for condition in order:
            messages = build_messages(manifest, condition, annotation_order)
            key = f"{condition}:{annotation_order}"
            prompt_hashes[key] = sha256_text(canonical_json(messages))
    for key in sorted(prompt_hashes):
        print(f"Prompt hash [{key}]: {prompt_hashes[key]}")

    if args.dry_run:
        print("\nFREEZE AUDIT PASS — no model calls were made.")
        if manifest["status"] != "preregistered-frozen":
            print(
                "EXECUTION REMAINS LOCKED — manifest is still "
                "preregistered-freeze-candidate."
            )
        return 0

    if manifest["status"] != "preregistered-frozen":
        print(
            "EXECUTION REFUSED — run the dry-run audit first, then freeze the "
            "manifest in a new pre-output commit."
        )
        return 3

    try:
        identity = verify_model_identity(manifest)
    except (urllib.error.URLError, RuntimeError) as exc:
        print(f"MODEL PREFLIGHT FAILED: {exc}")
        return 4

    print(f"\nModel preflight PASS: {identity}")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results_path = RESULTS_DIR / f"rvt_interp_002_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"rvt_interp_002_{stamp}_summary.json"

    rows: list[dict[str, Any]] = []
    run_index = 0
    with results_path.open("w", encoding="utf-8") as out:
        for block_index, (seed, order, annotation_order) in enumerate(
            zip(
                manifest["sampling"]["seeds"],
                manifest["condition_order_by_seed_index"],
                manifest["annotation_order_by_seed_index"],
            ),
            start=1,
        ):
            for condition in order:
                run_index += 1
                messages = build_messages(manifest, condition, annotation_order)
                prompt_sha = sha256_text(canonical_json(messages))
                row: dict[str, Any] = {
                    "experiment_id": manifest["experiment_id"],
                    "manifest_version": manifest["version"],
                    "manifest_sha256": manifest_sha,
                    "parent_manifest_sha256": parent_sha,
                    "run_index": run_index,
                    "block_index": block_index,
                    "seed": seed,
                    "condition": condition,
                    "annotation_order": annotation_order,
                    "model": manifest["model"],
                    "prompt_sha256": prompt_sha,
                    "messages": messages,
                    "started_at_utc": datetime.now(timezone.utc).isoformat(),
                }
                print(
                    f"[{run_index:02d}/{manifest['run_count']}] seed={seed} "
                    f"condition={condition} annotations={annotation_order}"
                )
                try:
                    payload, raw_body = call_model(manifest, messages, seed)
                    parsed, parse_error = parse_model_json(raw_body)
                    extraction = extract_primary(manifest, parsed)
                    row.update(
                        {
                            "request_payload": payload,
                            "raw_response": raw_body,
                            "parsed_output": parsed,
                            "parse_error": parse_error,
                            "primary_extraction": extraction,
                            "metrics": {
                                "prompt_eval_count": raw_body.get("prompt_eval_count"),
                                "eval_count": raw_body.get("eval_count"),
                                "total_duration": raw_body.get("total_duration"),
                                "done_reason": raw_body.get("done_reason"),
                            },
                        }
                    )
                except Exception as exc:
                    row.update(
                        {
                            "request_error": f"{type(exc).__name__}: {exc}",
                            "parsed_output": None,
                            "primary_extraction": extract_primary(manifest, None),
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
        "parent_manifest_sha256": parent_sha,
        "model_identity": identity,
        "freeze_audit": audit,
        "prompt_hashes": prompt_hashes,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "automatic_summary": summarize(manifest, rows),
        "interpretation_ceiling": manifest["interpretation_ceiling"],
        "comparison_rule": manifest["comparison_rule"],
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
