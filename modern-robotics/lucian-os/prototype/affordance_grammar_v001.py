"""ECM-003 — candidate minimal affordance grammar harness.

Simulation only. This script:
- loads label-free substrates described by relation families;
- validates the candidate grammar;
- compiles the grammar into the flat affordance form expected by the current
  morphology composer;
- reuses the existing ECM module registry and task profiles;
- tests label invariance, primitive-affordance ablation, authority separation,
  and category relevance.

Run from modern-robotics/lucian-os:

    py prototype/affordance_grammar_v001.py
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from morphology_composer import compose


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = PROJECT_ROOT / "manifests" / "affordance_grammar_demo.json"
ECM_PATH = PROJECT_ROOT / "manifests" / "elastic_demo_hosts.json"

RELATION_FAMILIES = (
    "sense",
    "present",
    "compute",
    "store",
    "communicate",
    "act",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def substrate_index(grammar: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in grammar.get("substrates", [])}


def validate_substrate(substrate: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if "type" in substrate:
        errors.append("device type labels are forbidden in ECM-003 substrates")

    affordances = substrate.get("affordances")
    if not isinstance(affordances, dict):
        return errors + ["affordances must be an object keyed by relation family"]

    unknown = set(affordances) - set(RELATION_FAMILIES)
    missing = set(RELATION_FAMILIES) - set(affordances)
    if unknown:
        errors.append(f"unknown relation families: {sorted(unknown)}")
    if missing:
        errors.append(f"missing relation families: {sorted(missing)}")

    for family in RELATION_FAMILIES:
        values = affordances.get(family, [])
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
            errors.append(f"{family} must be a list of strings")

    if not isinstance(substrate.get("resources", {}), dict):
        errors.append("resources must be an object")
    if not isinstance(substrate.get("authority", []), list):
        errors.append("authority must be a list")

    return errors


def compile_substrate(substrate: dict[str, Any]) -> dict[str, Any]:
    """Compile relation families into the current flat ECM host interface.

    This is deliberately a lossy compatibility bridge for v0.01. The composer
    should never receive a device category or infer capabilities from the id.
    """
    errors = validate_substrate(substrate)
    if errors:
        raise ValueError(f"Invalid substrate {substrate.get('id')!r}: {'; '.join(errors)}")

    flat: set[str] = set()
    for family in RELATION_FAMILIES:
        flat.update(str(x) for x in substrate["affordances"].get(family, []))

    return {
        "id": substrate.get("id"),
        "resources": copy.deepcopy(substrate.get("resources", {})),
        "affordances": sorted(flat),
        "authority": list(substrate.get("authority", [])),
        "resting_modules": list(substrate.get("resting_modules", [])),
    }


def morphology_fingerprint(result: dict[str, Any]) -> dict[str, Any]:
    chosen = result.get("chosen_morphology", {})
    return {
        "disposition": result.get("disposition"),
        "modules": chosen.get("modules", []),
        "provided_functions": chosen.get("provided_functions", []),
        "required_authority": chosen.get("required_authority", []),
        "unmet_demands": result.get("unmet_demands", []),
    }


def run_case(
    ecm: dict[str, Any],
    grammar: dict[str, Any],
    substrate_id: str,
    task_name: str,
) -> dict[str, Any]:
    substrates = substrate_index(grammar)
    substrate = copy.deepcopy(substrates[substrate_id])
    host = compile_substrate(substrate)
    task = copy.deepcopy(ecm["task_profiles"][task_name])
    return compose(ecm, host, task_name, task)


def main() -> int:
    grammar = load_json(GRAMMAR_PATH)
    ecm = load_json(ECM_PATH)
    substrates = substrate_index(grammar)

    report: dict[str, Any] = {
        "experiment": "ECM-003",
        "mode": "SIMULATION_ONLY",
        "grammar": list(RELATION_FAMILIES),
        "positive_cases": [],
        "metamorphic_tests": [],
        "negative_controls": [],
        "category_ablations": [],
    }

    all_pass = True

    # 1. Positive cross-embodiment cases.
    for case in grammar.get("test_cases", []):
        result = run_case(ecm, grammar, case["substrate"], case["task"])
        passed = result["disposition"] == case["expected"]
        all_pass = all_pass and passed
        report["positive_cases"].append(
            {
                "substrate": case["substrate"],
                "task": case["task"],
                "expected": case["expected"],
                "actual": result["disposition"],
                "modules": result["chosen_morphology"]["modules"],
                "passed": passed,
            }
        )

    # 2. Label/id invariance: rename substrate-f while preserving everything else.
    base_substrate = copy.deepcopy(substrates["substrate-f"])
    renamed = copy.deepcopy(base_substrate)
    renamed["id"] = "purple-box-17"

    task_name = "pick_up_object"
    task = copy.deepcopy(ecm["task_profiles"][task_name])
    base_result = compose(ecm, compile_substrate(base_substrate), task_name, task)
    renamed_result = compose(ecm, compile_substrate(renamed), task_name, copy.deepcopy(task))
    invariant = morphology_fingerprint(base_result) == morphology_fingerprint(renamed_result)
    all_pass = all_pass and invariant
    report["metamorphic_tests"].append(
        {
            "name": "rename_without_affordance_change",
            "passed": invariant,
            "base": morphology_fingerprint(base_result),
            "renamed": morphology_fingerprint(renamed_result),
        }
    )

    # 3. Primitive-affordance negative control: keep generic host, remove manipulator.
    ablated = copy.deepcopy(base_substrate)
    ablated["affordances"]["act"] = [
        x for x in ablated["affordances"]["act"] if x != "manipulator"
    ]
    ablated_result = compose(ecm, compile_substrate(ablated), task_name, copy.deepcopy(task))
    primitive_control = ablated_result["disposition"] == "NO_COMPLETE_ADMISSIBLE_MORPHOLOGY"
    all_pass = all_pass and primitive_control
    report["negative_controls"].append(
        {
            "name": "remove_required_manipulator",
            "passed": primitive_control,
            "result": morphology_fingerprint(ablated_result),
        }
    )

    # 4. Authority separation: keep physical cleaning affordances, remove permission.
    cleaning = copy.deepcopy(substrates["substrate-c"])
    cleaning["authority"] = [
        x for x in cleaning.get("authority", []) if x != "physical_actuation"
    ]
    clean_task = copy.deepcopy(ecm["task_profiles"]["clean_floor"])
    authority_result = compose(
        ecm,
        compile_substrate(cleaning),
        "clean_floor",
        clean_task,
    )
    authority_control = authority_result["disposition"] == "NO_COMPLETE_ADMISSIBLE_MORPHOLOGY"
    all_pass = all_pass and authority_control
    report["negative_controls"].append(
        {
            "name": "capability_without_authority",
            "passed": authority_control,
            "result": morphology_fingerprint(authority_result),
        }
    )

    # 5. Category relevance checks. Each category is ablated from a task that
    # currently depends on at least one primitive placed in that family.
    category_tests = {
        "sense": ("substrate-f", "pick_up_object"),
        "present": ("substrate-b", "show_explanation"),
        "compute": ("substrate-f", "pick_up_object"),
        "store": ("substrate-e", "organize_files"),
        "communicate": ("substrate-a", "speak_with_user"),
        "act": ("substrate-c", "clean_floor"),
    }

    for family, (substrate_id, category_task_name) in category_tests.items():
        original = copy.deepcopy(substrates[substrate_id])
        baseline_task = copy.deepcopy(ecm["task_profiles"][category_task_name])
        baseline = compose(
            ecm,
            compile_substrate(original),
            category_task_name,
            copy.deepcopy(baseline_task),
        )

        variant = copy.deepcopy(original)
        variant["affordances"][family] = []
        changed = compose(
            ecm,
            compile_substrate(variant),
            category_task_name,
            copy.deepcopy(baseline_task),
        )

        informative = (
            baseline["disposition"] == "VIABLE_MORPHOLOGY"
            and changed["disposition"] == "NO_COMPLETE_ADMISSIBLE_MORPHOLOGY"
        )
        all_pass = all_pass and informative
        report["category_ablations"].append(
            {
                "family": family,
                "substrate": substrate_id,
                "task": category_task_name,
                "baseline": baseline["disposition"],
                "after_ablation": changed["disposition"],
                "passed": informative,
            }
        )

    report["overall"] = "PASS" if all_pass else "REVIEW_REQUIRED"
    report["interpretation"] = (
        "PASS means the candidate grammar is expressive enough for the current demo set "
        "and each relation family is exercised by at least one discriminating test. It "
        "does not prove global minimality or real-device portability."
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
