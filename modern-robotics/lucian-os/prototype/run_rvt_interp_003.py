"""RVT-INTERP-003 — consequences-of-correction experiment.

From modern-robotics/lucian-os:
    py prototype/run_rvt_interp_003.py --dry-run

Actual model execution is refused until the manifest status is changed from
preregistered-freeze-candidate to preregistered-frozen after the dry-run audit
and prompt hashes are reviewed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PROJECT_ROOT / "manifests" / "rvt_interp_003_cases.json"
RESULTS_DIR = PROJECT_ROOT / "results"
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434").rstrip("/")
CHAT_URL = f"{OLLAMA_BASE}/api/chat"
TAGS_URL = f"{OLLAMA_BASE}/api/tags"

CONDITIONS = [
    "NEUTRAL_CONTROL",
    "CORRECTION_SURVIVABLE",
    "CORRECTION_COSTLY",
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_json(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw), sha256_text(raw)


def normalize_digest(value: str) -> str:
    value = value.strip().lower()
    if value.startswith("sha256:"):
        value = value.split(":", 1)[1]
    return value


def build_messages(m: dict[str, Any], condition: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": m["system_prompt"]},
    ]
    messages.extend(m["shared_prefix"])
    messages.append({"role": "user", "content": m["consequence_1"][condition]})
    messages.extend(m["shared_middle"])
    messages.append({"role": "user", "content": m["consequence_2"][condition]})
    messages.append({"role": "user", "content": m["terminal_prompt"]})
    return messages


def word_count_messages(messages: list[dict[str, str]]) -> int:
    return sum(len(x["content"].split()) for x in messages)


def validate_structure(m: dict[str, Any]) -> None:
    assert m["experiment_id"] == "RVT_INTERP_003"
    assert m["status"] in {"preregistered-freeze-candidate", "preregistered-frozen"}
    seeds = m["sampling"]["seeds"]
    orders = m["condition_order_by_seed_index"]
    assert len(seeds) == 12
    assert len(orders) == len(seeds)
    expected = set(CONDITIONS)
    for order in orders:
        assert len(order) == 3
        assert set(order) == expected
    assert m["run_count"] == len(seeds) * 3


def audit_bench_prerequisite(m: dict[str, Any]) -> dict[str, Any]:
    spec = m["interface_prerequisite"]
    path = PROJECT_ROOT / spec["summary_path"]
    if not path.exists():
        return {"passed": False, "detail": f"missing:{path}"}
    summary = json.loads(path.read_text(encoding="utf-8"))
    passed = (
        summary.get("bench_id") == spec["bench_id"]
        and summary.get("manifest_sha256") == spec["manifest_sha256"]
        and summary.get("bench_pass") is spec["required_bench_pass"]
        and summary.get("n_conforming") == spec["required_n_conforming"]
    )
    return {
        "passed": bool(passed),
        "detail": {
            "bench_id": summary.get("bench_id"),
            "manifest_sha256": summary.get("manifest_sha256"),
            "bench_pass": summary.get("bench_pass"),
            "n_conforming": summary.get("n_conforming"),
        },
    }


def audit_manifest(m: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: Any = "") -> None:
        checks.append({"name": name, "passed": bool(ok), "detail": detail})

    bench = audit_bench_prerequisite(m)
    check("schema_bench_prerequisite", bench["passed"], bench["detail"])

    # Six possible order permutations should each occur twice.
    order_counts = Counter(tuple(x) for x in m["condition_order_by_seed_index"])
    check(
        "balanced_condition_orders",
        len(order_counts) == 6 and set(order_counts.values()) == {2},
        {">".join(k): v for k, v in order_counts.items()},
    )

    # Every condition must have the same chat-role sequence and message count.
    built = {c: build_messages(m, c) for c in CONDITIONS}
    role_sequences = {
        c: [x["role"] for x in msgs] for c, msgs in built.items()
    }
    check(
        "role_sequence_equal",
        len({tuple(v) for v in role_sequences.values()}) == 1,
        role_sequences,
    )

    # All shared messages must be byte-identical by construction; only the two
    # consequence messages may differ. Verify the differing indices exactly.
    reference = built["NEUTRAL_CONTROL"]
    allowed_diff_indices = {
        1 + len(m["shared_prefix"]),
        2 + len(m["shared_prefix"]) + len(m["shared_middle"]),
    }
    diff_detail: dict[str, list[int]] = {}
    diff_ok = True
    for condition in ("CORRECTION_SURVIVABLE", "CORRECTION_COSTLY"):
        msgs = built[condition]
        diffs = [
            i
            for i, (a, b) in enumerate(zip(reference, msgs))
            if a != b
        ]
        diff_detail[condition] = diffs
        diff_ok = diff_ok and set(diffs) == allowed_diff_indices
    check("only_two_consequence_messages_vary", diff_ok, diff_detail)

    # Lexical directive/truth-value audit applies only to condition-specific text.
    forbidden = [
        x.lower() for x in m["forbidden_condition_specific_terms"]
    ] + [
        x.lower() for x in m["forbidden_condition_specific_truth_terms"]
    ]
    lexical_hits: dict[str, list[str]] = {}
    for condition in CONDITIONS:
        text = (
            m["consequence_1"][condition] + " " + m["consequence_2"][condition]
        ).lower()
        lexical_hits[condition] = [x for x in forbidden if x in text]
    check(
        "condition_specific_lexical_audit",
        all(not hits for hits in lexical_hits.values()),
        lexical_hits,
    )

    # Internal condition labels must never occur in model-visible messages.
    label_hits: dict[str, list[str]] = {}
    for condition, msgs in built.items():
        corpus = "\n".join(x["content"] for x in msgs)
        label_hits[condition] = [x for x in CONDITIONS if x in corpus]
    check(
        "condition_labels_hidden",
        all(not hits for hits in label_hits.values()),
        label_hits,
    )

    # Review word-count imbalance explicitly rather than silently accepting it.
    word_counts = {c: word_count_messages(msgs) for c, msgs in built.items()}
    spread = max(word_counts.values()) - min(word_counts.values())
    check(
        "prompt_word_count_spread_le_8",
        spread <= 8,
        {"word_counts": word_counts, "spread": spread},
    )

    # Strict schema should have exact required/property equality and no extras.
    schema = m["response_schema"]
    props = set(schema["properties"])
    required = set(schema["required"])
    check(
        "response_schema_exact_required_keys",
        props == required and schema.get("additionalProperties") is False,
        {"properties": sorted(props), "required": sorted(required)},
    )

    return {
        "passed": all(x["passed"] for x in checks),
        "checks": checks,
    }


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
        if spec.get("type") == "string" and not isinstance(value, str):
            errors.append(f"{key}:not_string")
            continue
        if spec.get("type") == "integer" and (
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
    m: dict[str, Any], messages: list[dict[str, str]], seed: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    sampling = m["sampling"]
    payload = {
        "model": m["model"]["tag"],
        "stream": False,
        "think": bool(sampling["think"]),
        "format": m["response_schema"],
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


def summarize(m: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_seed: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)

    for row in rows:
        grouped[row["condition"]].append(row)
        by_seed[int(row["seed"])][row["condition"]] = row

    summary: dict[str, Any] = {"conditions": {}, "paired_endpoint_contrasts": {}}

    revision_map = m["primary_outcomes"]["original_hypothesis_status_scoring"]

    for condition, items in grouped.items():
        conforming = [x for x in items if x["conforming"]]
        parsed = [x["parsed"] for x in conforming]
        revision_scores = [
            revision_map[x["original_hypothesis_status"]] for x in parsed
        ]
        temperature_exit = [
            0 if x["next_diagnostic_priority"] == "TEMPERATURE" else 1
            for x in parsed
        ]
        summary["conditions"][condition] = {
            "n_total": len(items),
            "n_parseable": sum(x["parsed"] is not None for x in items),
            "n_conforming": len(conforming),
            "next_diagnostic_priority": dict(
                Counter(x["next_diagnostic_priority"] for x in parsed)
            ),
            "original_hypothesis_status": dict(
                Counter(x["original_hypothesis_status"] for x in parsed)
            ),
            "best_supported_explanation": dict(
                Counter(x["best_supported_explanation"] for x in parsed)
            ),
            "does_new_evidence_count_against_it": dict(
                Counter(x["does_new_evidence_count_against_it"] for x in parsed)
            ),
            "mean_revision_score": (
                sum(revision_scores) / len(revision_scores)
                if revision_scores else None
            ),
            "temperature_exit_rate": (
                sum(temperature_exit) / len(temperature_exit)
                if temperature_exit else None
            ),
        }

    def endpoint_values(field: str) -> list[tuple[int, int]]:
        pairs: list[tuple[int, int]] = []
        for seed in m["sampling"]["seeds"]:
            block = by_seed[int(seed)]
            s = block.get("CORRECTION_SURVIVABLE")
            c = block.get("CORRECTION_COSTLY")
            if not s or not c or not s["conforming"] or not c["conforming"]:
                continue
            ps = s["parsed"]
            pc = c["parsed"]
            if field == "revision":
                pairs.append(
                    (
                        revision_map[ps["original_hypothesis_status"]],
                        revision_map[pc["original_hypothesis_status"]],
                    )
                )
            elif field == "temperature_exit":
                pairs.append(
                    (
                        0 if ps["next_diagnostic_priority"] == "TEMPERATURE" else 1,
                        0 if pc["next_diagnostic_priority"] == "TEMPERATURE" else 1,
                    )
                )
        return pairs

    for field in ("revision", "temperature_exit"):
        pairs = endpoint_values(field)
        diffs = [a - b for a, b in pairs]
        summary["paired_endpoint_contrasts"][field] = {
            "n_complete_pairs": len(pairs),
            "survivable_minus_costly": {
                "positive": sum(x > 0 for x in diffs),
                "tie": sum(x == 0 for x in diffs),
                "negative": sum(x < 0 for x in diffs),
                "mean_difference": (
                    sum(diffs) / len(diffs) if diffs else None
                ),
            },
        }

    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    m, manifest_sha = load_json(MANIFEST_PATH)
    validate_structure(m)
    audit = audit_manifest(m)

    print("RVT-INTERP-003 — Consequences of Correction")
    print(f"Manifest: {MANIFEST_PATH.name} v{m['version']}")
    print(f"Status: {m['status']}")
    print(f"Manifest SHA256: {manifest_sha}")
    print(f"Locked model: {m['model']['tag']}")
    print(f"Planned runs: {m['run_count']}")
    print("")
    print("Freeze audit:")
    for item in audit["checks"]:
        state = "PASS" if item["passed"] else "FAIL"
        detail = f" — {item['detail']}" if item["detail"] not in ("", None) else ""
        print(f"  [{state}] {item['name']}{detail}")

    print("")
    print("Candidate schedule:")
    for i, (seed, order) in enumerate(
        zip(m["sampling"]["seeds"], m["condition_order_by_seed_index"]),
        start=1,
    ):
        print(f"  block {i:02d} seed={seed}: {' -> '.join(order)}")

    print("")
    print("Prompt hashes:")
    for condition in CONDITIONS:
        messages = build_messages(m, condition)
        print(
            f"  {condition}: "
            f"{sha256_text(canonical_json(messages))} "
            f"(words={word_count_messages(messages)})"
        )
    print(
        "  RESPONSE_SCHEMA: "
        + sha256_text(canonical_json(m["response_schema"]))
    )

    if not audit["passed"]:
        raise RuntimeError("Freeze audit failed. Do not execute.")

    if args.dry_run:
        print("")
        print("FREEZE AUDIT PASS — no model calls were made.")
        if m["status"] == "preregistered-freeze-candidate":
            print("EXECUTION REMAINS LOCKED — manifest is still a freeze candidate.")
        else:
            print("Manifest is preregistered-frozen.")
        return

    if m["status"] != "preregistered-frozen":
        raise RuntimeError(
            "Actual execution refused: manifest is not preregistered-frozen."
        )

    model_identity = verify_model_identity(m)
    print("")
    print(f"Model preflight PASS: {model_identity}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"rvt_interp_003_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"rvt_interp_003_{stamp}_summary.json"

    rows: list[dict[str, Any]] = []
    run_index = 0
    with out_path.open("w", encoding="utf-8") as out:
        for seed, order in zip(
            m["sampling"]["seeds"],
            m["condition_order_by_seed_index"],
        ):
            for condition in order:
                run_index += 1
                print(
                    f"[{run_index:02d}/{m['run_count']}] "
                    f"seed={seed} condition={condition}"
                )
                row: dict[str, Any] = {
                    "experiment_id": m["experiment_id"],
                    "manifest_version": m["version"],
                    "manifest_sha256": manifest_sha,
                    "seed": seed,
                    "condition": condition,
                    "prompt_sha256": sha256_text(
                        canonical_json(build_messages(m, condition))
                    ),
                    "request": None,
                    "raw_response": None,
                    "parsed": None,
                    "parse_error": None,
                    "schema_errors": [],
                    "conforming": False,
                }
                try:
                    payload, raw_body = call_model(
                        m, build_messages(m, condition), int(seed)
                    )
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
                            parsed, m["response_schema"]
                        )
                        row["conforming"] = len(row["schema_errors"]) == 0
                except Exception as exc:
                    row["parse_error"] = (
                        f"call_error:{type(exc).__name__}:{exc}"
                    )

                rows.append(row)
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()

    summary = {
        "experiment_id": m["experiment_id"],
        "manifest_version": m["version"],
        "manifest_sha256": manifest_sha,
        "model_identity": model_identity,
        "freeze_audit": audit,
        "prompt_hashes": {
            c: sha256_text(canonical_json(build_messages(m, c)))
            for c in CONDITIONS
        },
        "response_schema_sha256": sha256_text(
            canonical_json(m["response_schema"])
        ),
        "automatic_summary": summarize(m, rows),
        "directional_prediction": m["directional_prediction"],
        "interpretation_ceiling": m["interpretation_ceiling"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("")
    print(f"Raw results: {out_path}")
    print(f"Summary:     {summary_path}")
    print(json.dumps(summary["automatic_summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
