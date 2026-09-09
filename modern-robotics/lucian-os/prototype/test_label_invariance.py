"""ECM-002 — label-free embodiment / morphology invariance test.

Simulation only. This test checks whether descriptive host labels (id/type) are
non-load-bearing for morphology composition while genuine affordance and
authority changes remain load-bearing.

Run from modern-robotics/lucian-os:

    py prototype/test_label_invariance.py
"""

from __future__ import annotations

import copy
import json
from typing import Any

from morphology_composer import DEFAULT_DEMO, compose, find_host, find_task, load_demo


BASELINE_CASES = [
    ("old-radio-demo", "speak_with_user"),
    ("vacuum-demo", "clean_floor"),
    ("robot-demo", "pick_up_object"),
]


def signature(result: dict[str, Any]) -> dict[str, Any]:
    morphology = result["chosen_morphology"]
    return {
        "modules": morphology["modules"],
        "local_modules": morphology["local_modules"],
        "recruited_remote_modules": morphology["recruited_remote_modules"],
        "provided_functions": morphology["provided_functions"],
        "memory_cost_mb": morphology["memory_cost_mb"],
        "required_authority": morphology["required_authority"],
        "unmet_demands": result["unmet_demands"],
        "disposition": result["disposition"],
    }


def run_case(data: dict[str, Any], host: dict[str, Any], task_name: str) -> dict[str, Any]:
    task = find_task(data, task_name)
    return compose(data, host, task_name, task)


def assert_same(label: str, baseline: dict[str, Any], transformed: dict[str, Any]) -> tuple[bool, str]:
    left = signature(baseline)
    right = signature(transformed)
    ok = left == right
    detail = "unchanged" if ok else json.dumps({"baseline": left, "transformed": right}, indent=2)
    return ok, f"{label}: {'PASS' if ok else 'FAIL'} — {detail}"


def main() -> int:
    data = load_demo(DEFAULT_DEMO)
    reports: list[str] = []
    failures = 0

    for index, (host_id, task_name) in enumerate(BASELINE_CASES, start=1):
        baseline_host = find_host(data, host_id)
        baseline = run_case(data, baseline_host, task_name)

        renamed = copy.deepcopy(baseline_host)
        renamed["id"] = f"substrate-{index:03d}"
        renamed["type"] = "purple_box"
        renamed_result = run_case(data, renamed, task_name)
        ok, report = assert_same(f"{host_id}/{task_name} rename id+type", baseline, renamed_result)
        reports.append(report)
        failures += 0 if ok else 1

        typeless = copy.deepcopy(baseline_host)
        typeless["id"] = f"substrate-{index:03d}-typeless"
        typeless.pop("type", None)
        typeless_result = run_case(data, typeless, task_name)
        ok, report = assert_same(f"{host_id}/{task_name} remove type", baseline, typeless_result)
        reports.append(report)
        failures += 0 if ok else 1

    # Negative control 1: familiar label must not compensate for missing physical affordance.
    robot = find_host(data, "robot-demo")
    robot_without_manipulator = copy.deepcopy(robot)
    robot_without_manipulator["affordances"] = [
        x for x in robot_without_manipulator.get("affordances", []) if x != "manipulator"
    ]
    result_missing_manipulator = run_case(data, robot_without_manipulator, "pick_up_object")
    ok = result_missing_manipulator["disposition"] == "NO_COMPLETE_ADMISSIBLE_MORPHOLOGY"
    reports.append(
        "negative control / remove manipulator: "
        + ("PASS" if ok else "FAIL")
        + " — device label retained; missing affordance must still block composition"
    )
    failures += 0 if ok else 1

    # Negative control 2: physical capability must not manufacture authority.
    vacuum = find_host(data, "vacuum-demo")
    vacuum_without_authority = copy.deepcopy(vacuum)
    vacuum_without_authority["authority"] = [
        x for x in vacuum_without_authority.get("authority", []) if x != "physical_actuation"
    ]
    result_no_authority = run_case(data, vacuum_without_authority, "clean_floor")
    ok = result_no_authority["disposition"] == "NO_COMPLETE_ADMISSIBLE_MORPHOLOGY"
    reports.append(
        "negative control / remove physical authority: "
        + ("PASS" if ok else "FAIL")
        + " — physical affordances remain; authority loss must block admissible composition"
    )
    failures += 0 if ok else 1

    print("ECM-002 — Label-Free Embodiment / Morphological Invariance")
    print("=" * 68)
    for report in reports:
        print(report)

    print("-" * 68)
    if failures:
        print(f"RESULT: FAIL ({failures} failed checks)")
        return 1

    print("RESULT: PASS — descriptive device labels are non-load-bearing in tested cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
