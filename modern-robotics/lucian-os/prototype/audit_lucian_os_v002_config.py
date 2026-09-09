"""Independent static audit for Lucian OS v0.2 configuration and judge contracts.

No Ollama call. No external action.
Run from modern-robotics/lucian-os:
    py prototype/audit_lucian_os_v002_config.py

A PASS here means the inspected static contracts are internally consistent enough
for the current prototype. It does NOT certify semantic correctness of model
reasoning.
"""

from __future__ import annotations

import json
from pathlib import Path

from lucian_os_v002 import V002_IDENTITY, independent_warrant_gate
from relational_search_engine import validate_search_state


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IDENTITY_DIR = PROJECT_ROOT / "identity"
MANIFEST_DIR = PROJECT_ROOT / "manifests"

PATHS = {
    "identity_v001": IDENTITY_DIR / "lucian_identity_v001.json",
    "identity_v002": V002_IDENTITY,
    "operative_rules": IDENTITY_DIR / "operative_rules_v001.json",
    "structured_relations": IDENTITY_DIR / "structured_relations_v001.json",
    "temporal_state": IDENTITY_DIR / "temporal_relational_state_v001.json",
    "windows_manifest": MANIFEST_DIR / "windows_dev_host.json",
    "qwen_competence": MANIFEST_DIR / "qwen3_5_2b_competence_v001.json",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a top-level object")
    return value


def _search_state() -> dict:
    return {
        "candidate_relations": ["candidate A"],
        "competing_relations": ["candidate B"],
        "established": ["fact 1"],
        "not_established": ["stronger claim"],
        "missing_information": [],
        "warrant_status": "SUFFICIENT",
        "posture": "LAND",
        "provisional_landing": "unsupported semantic claim",
        "required_capability": "reason_about_task",
        "proposed_next_step": "Keep the claim provisional.",
        "return_localization": None,
    }


def main() -> None:
    docs = {name: load_json(path) for name, path in PATHS.items()}
    hard_failures: list[str] = []
    warnings: list[str] = []

    # Identity / operative-rule alignment.
    identity = docs["identity_v002"]
    invariant_ids = [str(item.get("id")) for item in identity.get("invariants", [])]
    if len(invariant_ids) != len(set(invariant_ids)):
        hard_failures.append("v0.02 identity contains duplicate invariant IDs")

    rule_ids = [
        str(item.get("invariant_id"))
        for item in docs["operative_rules"].get("rules", [])
    ]
    missing_rules = sorted(set(invariant_ids) - set(rule_ids))
    orphan_rules = sorted(set(rule_ids) - set(invariant_ids))
    if missing_rules:
        hard_failures.append(f"v0.02 invariants missing operative rules: {missing_rules}")
    if orphan_rules:
        hard_failures.append(f"operative rules refer to absent v0.02 invariants: {orphan_rules}")

    if identity.get("identity_id") != "lucian-v0.02":
        hard_failures.append("V002_IDENTITY does not identify lucian-v0.02")

    # Manifest consistency.
    manifest = docs["windows_manifest"]
    caps = {
        str(item.get("name")): item
        for item in manifest.get("capabilities", [])
        if item.get("name")
    }
    if len(caps) != len(manifest.get("capabilities", [])):
        hard_failures.append("windows manifest contains missing or duplicate capability names")

    authority = manifest.get("authority_defaults", {})
    permitted = set(authority.get("permitted", []))
    prohibited = set(authority.get("prohibited", []))
    overlap = sorted(permitted & prohibited)
    if overlap:
        hard_failures.append(f"capabilities both permitted and prohibited: {overlap}")

    undeclared_permitted = sorted(permitted - set(caps))
    if undeclared_permitted:
        hard_failures.append(f"permitted capabilities not declared in manifest: {undeclared_permitted}")

    disabled_permitted = sorted(
        name for name in permitted if name in caps and not bool(caps[name].get("enabled", False))
    )
    if disabled_permitted:
        hard_failures.append(f"permitted capabilities are disabled: {disabled_permitted}")

    # Model competence file must refer to a declared model, but remains only a prior.
    competence_model = str(docs["qwen_competence"].get("model", ""))
    manifest_models = {
        str(item.get("name")) for item in manifest.get("available_models", []) if item.get("name")
    }
    if competence_model not in manifest_models:
        hard_failures.append(
            f"competence manifest model {competence_model!r} not declared by embodiment"
        )

    task_classes = docs["qwen_competence"].get("task_classes", {})
    for critical_class in ("contrary_evidence_revision", "correction_continuity"):
        status = str(task_classes.get(critical_class, {}).get("status", ""))
        if status == "not_validated":
            warnings.append(
                f"Qwen competence remains not_validated for {critical_class}; do not use it as a judge"
            )

    # Legacy structured-relations schema audit.
    structured = docs["structured_relations"]
    declared_fields = set(structured.get("fields", {}))
    referenced_runtime_fields = {
        "authority_status",
        "proposed_posture",
        "verification_scope",
        "verification_status",
        "horizon_status",
        "horizon_value_seconds",
        "pressure_present",
        "preference_evidence_status",
        "contrary_evidence_present",
        "conclusion_status",
        "better_contrary_evidence",
        "continuity_target",
    }
    undeclared_relation_fields = sorted(referenced_runtime_fields - declared_fields)
    if undeclared_relation_fields:
        warnings.append(
            "structured_relations_v001 is not a self-contained executable schema; "
            f"referenced-but-undeclared fields include {undeclared_relation_fields}"
        )

    # Judge limitation must be explicit and preserved: structural validity is not semantic validity.
    unsupported = _search_state()
    structural = validate_search_state(unsupported)
    if not structural.get("valid", False):
        hard_failures.append(
            "expected well-formed unsupported fixture to pass structural validation; validator contract changed"
        )
    else:
        warnings.append(
            "structural validator correctly remains non-semantic: a well-formed unsupported claim is structurally valid"
        )

    warrant = independent_warrant_gate(search_state=unsupported)
    if warrant.get("allowed_to_land", True):
        hard_failures.append("host can still self-certify LAND without independent verification")

    # Historical identity remains present but must not be the selected runtime source.
    if PATHS["identity_v001"] == V002_IDENTITY:
        hard_failures.append("v0.2 identity path accidentally points to v0.01")

    print("Lucian OS v0.2 JSON + judge audit")
    print("=" * 72)
    for name, path in PATHS.items():
        print(f"READ {name}: {path.relative_to(PROJECT_ROOT)}")

    if warnings:
        print("\nWARNINGS")
        for warning in warnings:
            print(f"- {warning}")

    if hard_failures:
        print("\nHARD FAILURES")
        for failure in hard_failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("\nSTATIC SAFETY/CONFIG AUDIT: PASS")
    print("SEMANTIC CORRECTNESS: NOT CERTIFIED")


if __name__ == "__main__":
    main()
