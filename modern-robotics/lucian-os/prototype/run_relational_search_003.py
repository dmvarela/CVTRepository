"""Run RELATIONAL_SEARCH_003 against the local Ollama host.

Simulation only. No external actions are executed and no model weights are changed.
Run from modern-robotics/lucian-os:
    py prototype/run_relational_search_003.py

RS-003 tests epistemic standing / write-access on new held-out surfaces.
Preserve the first complete run exactly.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lucian_router import MODEL, OLLAMA_URL, extract_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"

CONDITIONS = (
    "format_only",
    "generic_warrant",
    "epistemic_membrane_map",
    "worked_epistemic_membrane",
)

VALID_STANDING = {"SUFFICIENT", "INSUFFICIENT", "UNRESOLVED"}
VALID_WRITE = {"WRITE", "NO_WRITE", "HOLD"}

SYSTEM_PROMPT = """You are a development host inside a simulation-only reasoning experiment.
Judge whether one supplied incoming signal has standing to update one explicitly specified target state.
Use only the supplied facts. Do not invent authority, provenance, relevance, diagnosticity, or temporal relations.
Do not expose private hidden chain-of-thought.
Training material is orientation only and is not evidence about the held-out case.

Return JSON only with exactly these keys:
target_state, incoming_signal, standing_basis, blocking_factor,
standing_status, write_decision, reason_short

Definitions:
SUFFICIENT = supplied facts establish that the incoming signal has enough standing to update the specified target state as proposed.
INSUFFICIENT = supplied facts establish a blocking relation that prevents the proposed write.
UNRESOLVED = supplied facts do not establish whether standing is sufficient.
WRITE = only when standing_status is SUFFICIENT.
NO_WRITE = only when standing_status is INSUFFICIENT.
HOLD = only when standing_status is UNRESOLVED.

This task scores standing, not ultimate world truth. A signal may be observed without receiving write-access to the target state.
"""

INTERFACE = """INTERFACE SCAFFOLD — FORMAT ONLY
If standing_status is SUFFICIENT, write_decision must be the string \"WRITE\".
If standing_status is INSUFFICIENT, write_decision must be the string \"NO_WRITE\".
If standing_status is UNRESOLVED, write_decision must be the string \"HOLD\".

Exact token examples:
{\"standing_status\":\"SUFFICIENT\",\"write_decision\":\"WRITE\"}
{\"standing_status\":\"INSUFFICIENT\",\"write_decision\":\"NO_WRITE\"}
{\"standing_status\":\"UNRESOLVED\",\"write_decision\":\"HOLD\"}

These examples teach only output tokens, not how to judge standing.
"""

GENERIC_WARRANT = """ORIENTATION — GENERIC WARRANT
- Claim strength should track supplied evidence.
- Missing evidence is not contrary evidence.
- Strong evidence should not be ignored merely to remain cautious.
- New information matters according to what it actually establishes.
Do not infer extra facts.
"""

MEMBRANE_MAP = """ORIENTATION — EPISTEMIC MEMBRANE / STANDING MAP
For the held-out case:
1. Identify the target state that would be changed.
2. Identify the incoming signal.
3. Ask whether the signal bears on THIS target rather than a nearby state.
4. Ask whether the source has authority or competence over THIS kind of state when authority matters.
5. Ask whether the signal is direct/diagnostic enough for THIS proposed update.
6. Ask whether its temporal relation permits it to supersede the currently represented state.
7. Do not confuse arrival with standing: information may be observed without being allowed to rewrite the target.
8. If a blocking relation is established -> INSUFFICIENT / NO_WRITE.
9. If the required standing relations are established -> SUFFICIENT / WRITE.
10. If supplied facts do not establish standing either way -> UNRESOLVED / HOLD.
"""

WORKED = """ORIENTATION — WORKED EPISTEMIC-MEMBRANE EXAMPLES

Library-catalog authority example:
A patron proposes changing the canonical author field. The supplied policy says only the catalog editor may alter canonical metadata. The suggestion can be observed, but it has INSUFFICIENT standing to rewrite the author field -> NO_WRITE. If the verified catalog editor issues the same change under that policy, standing is SUFFICIENT -> WRITE.

Soil-plot relevance example:
A calibrated moisture reading from Plot B does not have standing to update Plot A's moisture state because it concerns the wrong target -> INSUFFICIENT / NO_WRITE. A valid calibrated reading explicitly from Plot A has SUFFICIENT standing for Plot A -> WRITE.

Manufacturing diagnosticity example:
An unusual squeal is compatible with several faults and by itself does not have standing to write motor_bearing=FAILED -> INSUFFICIENT / NO_WRITE. A stipulated validated bearing-specific bench test identifying bearing failure has SUFFICIENT standing -> WRITE.

Version-stream temporality example:
A later verified revision in the same authoritative version stream can supersede an earlier verified revision -> SUFFICIENT / WRITE. An older revision does not supersede a newer current revision merely because the older record is presented later to the model -> INSUFFICIENT / NO_WRITE.

Learn the standing relation, not the surface nouns.
"""


def material(condition: str) -> str:
    if condition == "format_only":
        return INTERFACE
    if condition == "generic_warrant":
        return INTERFACE + "\n\n" + GENERIC_WARRANT
    if condition == "epistemic_membrane_map":
        return INTERFACE + "\n\n" + MEMBRANE_MAP
    if condition == "worked_epistemic_membrane":
        return INTERFACE + "\n\n" + WORKED
    raise ValueError(condition)


def case(
    case_id: str,
    family: str,
    facts: str,
    target_state: str,
    incoming_signal: str,
    expected: str,
) -> dict[str, str]:
    return {
        "case_id": case_id,
        "family": family,
        "facts": facts,
        "target_state": target_state,
        "incoming_signal": incoming_signal,
        "expected": expected,
        "expected_write": {
            "SUFFICIENT": "WRITE",
            "INSUFFICIENT": "NO_WRITE",
            "UNRESOLVED": "HOLD",
        }[expected],
    }


CASES = [
    case(
        "AUTH_ASSISTANT_CANNOT_REBOOK",
        "authority",
        "The represented state says Studio 3 is reserved for Maya. The written booking policy says only the booking coordinator may change reservation holders. A student assistant, who is not the booking coordinator, sends a message saying to replace Maya with Leo.",
        "Studio 3 reservation holder = Leo",
        "Student assistant says replace Maya with Leo.",
        "INSUFFICIENT",
    ),
    case(
        "AUTH_COORDINATOR_CAN_REBOOK",
        "authority",
        "The represented state says Studio 3 is reserved for Maya. The written booking policy says the booking coordinator may change reservation holders. The verified booking coordinator sends an update replacing Maya with Leo.",
        "Studio 3 reservation holder = Leo",
        "Verified booking coordinator says replace Maya with Leo.",
        "SUFFICIENT",
    ),
    case(
        "REL_SENSOR_WRONG_ZONE",
        "relevance",
        "The represented state tracks the soil-moisture condition of Greenhouse Zone A. A calibrated moisture sensor reports DRY, but its verified sensor identifier belongs to Greenhouse Zone B. Nothing links this reading to Zone A.",
        "Greenhouse Zone A moisture condition = DRY",
        "Calibrated Zone B sensor reports DRY.",
        "INSUFFICIENT",
    ),
    case(
        "REL_SENSOR_MATCHED_ZONE",
        "relevance",
        "The represented state tracks the soil-moisture condition of Greenhouse Zone A. A calibrated moisture sensor reports DRY, and its verified sensor identifier belongs to Greenhouse Zone A. The prompt stipulates the reading is valid for the current Zone A condition.",
        "Greenhouse Zone A moisture condition = DRY",
        "Calibrated Zone A sensor reports DRY.",
        "SUFFICIENT",
    ),
    case(
        "DIAG_LEAF_SYMPTOM_ONLY",
        "diagnosticity",
        "Plant P develops yellow leaf spots. The supplied facts state that the same symptom can result from fungus X, nutrient deficiency, or heat stress. No discriminating test is supplied.",
        "Plant P infection status = FUNGUS_X_CONFIRMED",
        "Plant P has yellow leaf spots.",
        "INSUFFICIENT",
    ),
    case(
        "DIAG_SPECIFIC_ASSAY",
        "diagnosticity",
        "A validated laboratory assay stipulated to be specific for fungus X is run on Plant P. The assay is positive and the prompt stipulates the test and sample identity are valid.",
        "Plant P infection status = FUNGUS_X_CONFIRMED",
        "Validated fungus-X-specific assay on Plant P is positive.",
        "SUFFICIENT",
    ),
    case(
        "TEMP_OLDER_CALIBRATION_CANNOT_SUPERSEDE",
        "temporal",
        "The represented calibration coefficient is 1.05 from a verified laboratory calibration record timestamped 14:00. An equally authoritative verified record from the same calibration stream, timestamped 09:00, says the coefficient was 1.02. No evidence says the 09:00 record is a later correction of the 14:00 record.",
        "Calibration coefficient = 1.02",
        "Verified 09:00 calibration record says 1.02.",
        "INSUFFICIENT",
    ),
    case(
        "TEMP_LATER_CALIBRATION_SUPERSEDES",
        "temporal",
        "The represented calibration coefficient is 1.02 from a verified laboratory calibration record timestamped 09:00. An equally authoritative verified record from the same calibration stream, timestamped 14:00, says the coefficient is now 1.05. The prompt stipulates the 14:00 record is the later current revision.",
        "Calibration coefficient = 1.05",
        "Verified later 14:00 calibration record says 1.05.",
        "SUFFICIENT",
    ),
    case(
        "AR_CONTROLLER_WRONG_ARM",
        "authority_relevance",
        "A verified maintenance controller has authority to change maintenance-clearance states for robot arms. The represented target is robot arm R17. The controller issues a verified clearance revocation for robot arm R19. Nothing states that R19 and R17 share a clearance state.",
        "Robot arm R17 maintenance clearance = REVOKED",
        "Authorized controller revokes clearance for robot arm R19.",
        "INSUFFICIENT",
    ),
    case(
        "AR_CONTROLLER_MATCHED_ARM",
        "authority_relevance",
        "A verified maintenance controller has authority to change maintenance-clearance states for robot arms. The represented target is robot arm R17. The controller issues a verified clearance revocation for robot arm R17.",
        "Robot arm R17 maintenance clearance = REVOKED",
        "Authorized controller revokes clearance for robot arm R17.",
        "SUFFICIENT",
    ),
    case(
        "AT_LATER_VISITOR_POST_CANNOT_SUPERSEDE",
        "authority_temporal",
        "The represented opening time for Gallery North is 10:00 from the current verified curator schedule. Later, a visitor posts on a public forum that Gallery North opens at 11:00. Nothing establishes that the visitor can revise the curator schedule.",
        "Gallery North opening time = 11:00",
        "Later visitor forum post says 11:00.",
        "INSUFFICIENT",
    ),
    case(
        "AT_LATER_CURATOR_REVISION_SUPERSEDES",
        "authority_temporal",
        "The represented opening time for Gallery North is 10:00 from a verified curator schedule. Later, the verified curator publishes a revised current schedule saying Gallery North opens at 11:00. The prompt stipulates the revision supersedes the earlier schedule.",
        "Gallery North opening time = 11:00",
        "Later verified curator revision says 11:00.",
        "SUFFICIENT",
    ),
]


def call_host(prompt: str) -> tuple[str, dict[str, Any]]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 700, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
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
        raise RuntimeError(f"Could not reach Ollama at {OLLAMA_URL}: {exc}") from exc

    raw = str(body.get("message", {}).get("content", ""))
    return raw, {
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "total_duration": body.get("total_duration"),
        "done_reason": body.get("done_reason"),
    }


def rotated_conditions(index: int) -> list[str]:
    k = index % len(CONDITIONS)
    return list(CONDITIONS[k:] + CONDITIONS[:k])


def expected_write_for(status: str | None) -> str | None:
    return {
        "SUFFICIENT": "WRITE",
        "INSUFFICIENT": "NO_WRITE",
        "UNRESOLVED": "HOLD",
    }.get(status)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"relational_search_003_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"relational_search_003_{stamp}_summary.json"

    print("RELATIONAL_SEARCH_003 — Epistemic Membrane / Evidential Standing")
    print("Preregistered exploratory pilot; simulation only; no weights changed.")
    print(f"Model: {MODEL}")
    print(f"Calls: {len(CASES)} cases x {len(CONDITIONS)} conditions = {len(CASES) * len(CONDITIONS)}")
    print("Primary outcome: standing-status accuracy.")
    print("IMPORTANT: preserve the first complete run exactly.\n")

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    family_status: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))

    required_keys = {
        "target_state",
        "incoming_signal",
        "standing_basis",
        "blocking_factor",
        "standing_status",
        "write_decision",
        "reason_short",
    }

    for i, c in enumerate(CASES):
        for condition in rotated_conditions(i):
            prompt = (
                material(condition)
                + "\n\nHELD-OUT CASE\nFacts: " + c["facts"]
                + "\nTarget state: " + c["target_state"]
                + "\nIncoming signal: " + c["incoming_signal"]
                + "\nReturn the required JSON object only."
            )
            print(f"[{c['case_id']}] {condition} ...", flush=True)
            raw, metrics = call_host(prompt)

            parsed: dict[str, Any] | None = None
            parse_error: str | None = None
            valid_schema = False
            try:
                parsed = extract_json(raw)
                valid_schema = (
                    set(parsed.keys()) == required_keys
                    and parsed.get("standing_status") in VALID_STANDING
                    and parsed.get("write_decision") in VALID_WRITE
                )
            except Exception as exc:
                parse_error = repr(exc)

            status = parsed.get("standing_status") if isinstance(parsed, dict) else None
            write = parsed.get("write_decision") if isinstance(parsed, dict) else None

            status_correct = status == c["expected"]
            write_correct = write == c["expected_write"]
            joint_correct = status_correct and write_correct
            mapping_consistent = write == expected_write_for(status)

            false_write = c["expected"] == "INSUFFICIENT" and status == "SUFFICIENT"
            false_block = c["expected"] == "SUFFICIENT" and status == "INSUFFICIENT"
            unresolved_error = c["expected"] != "UNRESOLVED" and status == "UNRESOLVED"

            counts[condition]["calls"] += 1
            counts[condition]["status_correct"] += int(status_correct)
            counts[condition]["write_correct"] += int(write_correct)
            counts[condition]["joint_correct"] += int(joint_correct)
            counts[condition]["valid_schema"] += int(valid_schema)
            counts[condition]["mapping_consistent"] += int(mapping_consistent)
            counts[condition]["false_write"] += int(false_write)
            counts[condition]["false_block"] += int(false_block)
            counts[condition]["unresolved_error"] += int(unresolved_error)
            family_status[condition][c["family"]].append(status_correct)

            event = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "model": MODEL,
                "condition": condition,
                **c,
                "raw_output": raw,
                "parsed": parsed,
                "parse_error": parse_error,
                "valid_schema": valid_schema,
                "status_correct": status_correct,
                "write_correct": write_correct,
                "joint_correct": joint_correct,
                "mapping_consistent": mapping_consistent,
                "false_write": false_write,
                "false_block": false_block,
                "unresolved_error": unresolved_error,
                "metrics": metrics,
            }
            with output_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    summary: dict[str, Any] = {
        "experiment": "RELATIONAL_SEARCH_003",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "primary_outcome": "standing_status_accuracy",
        "result_file": str(output_path),
        "conditions": {},
    }

    for condition in CONDITIONS:
        c = counts[condition]
        pairs = sum(
            1
            for values in family_status[condition].values()
            if len(values) == 2 and all(values)
        )
        summary["conditions"][condition] = {
            "calls": c["calls"],
            "status_correct_primary": c["status_correct"],
            "status_pairs_correct": pairs,
            "status_pairs_total": 6,
            "false_write": c["false_write"],
            "false_block": c["false_block"],
            "unresolved_error": c["unresolved_error"],
            "valid_schema": c["valid_schema"],
            "mapping_consistent": c["mapping_consistent"],
            "write_correct": c["write_correct"],
            "joint_correct": c["joint_correct"],
        }

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nSUMMARY")
    for condition in CONDITIONS:
        s = summary["conditions"][condition]
        print(
            f"{condition:28s} standing={s['status_correct_primary']}/12 "
            f"pairs={s['status_pairs_correct']}/6 write={s['write_correct']}/12 "
            f"joint={s['joint_correct']}/12 false_write={s['false_write']} "
            f"false_block={s['false_block']} unresolved={s['unresolved_error']} "
            f"schema={s['valid_schema']}/12 mapping={s['mapping_consistent']}/12"
        )

    print(f"\nRaw first-run output: {output_path}")
    print(f"Summary: {summary_path}")
    print("Do not rerun before inspecting the first run.")


if __name__ == "__main__":
    main()
