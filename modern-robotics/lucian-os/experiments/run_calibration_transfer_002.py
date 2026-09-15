#!/usr/bin/env python3
"""Run CALIBRATION_TRANSFER_002 against a local Ollama host.

Each condition/probe call is stateless. Raw outputs are preserved before parsing.
The default model is the frozen local Ministral host used for v002 preflight.

Usage:
  python run_calibration_transfer_002.py --probe P1
  python run_calibration_transfer_002.py
  python run_calibration_transfer_002.py --model ministral-3:3b-instruct-2512-q4_K_M

Outputs are written under experiments/results/calibration_transfer_002/.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "ministral-3:3b-instruct-2512-q4_K_M")

COMMON_CONTRACT = r'''You are evaluating a fictional collaboration state. Use only the supplied scenario and any teaching material included before it.

Return JSON only:
{
  "action": "...",
  "standing": "GOVERNING|SUPPORTING|HOLD|REJECT|NA",
  "write_target": "NONE|ACTIVE_STATE|PHASE|CALIBRATION|PRINCIPLE",
  "write_scope": "TURN|TASK|PROJECT|DOMAIN|GLOBAL|NONE",
  "reason_short": "one or two concise sentences"
}

Choose `action` only from the candidates supplied with the probe.

`standing` means the present authority of the highlighted incoming item, memory, correction, concept, or evidence source.

`write_target` means what STORED STATE the highlighted NEW ITEM warrants changing now. It is not the context that merely makes the item relevant.

NONE = the item may influence the present response but does not warrant a stored-state update.
ACTIVE_STATE = update current task/project facts, goals, local constraints, instructions, or working assumptions.
PHASE = update the stage of work itself, e.g. explore -> externalize or externalize -> investigate.
CALIBRATION = update a learned relational default or decision boundary beyond one local state.
PRINCIPLE = update a relatively stable epistemic/admissibility constraint.

Merely being appropriate because the current phase is exploratory does NOT mean PHASE. PHASE is only for changing the phase itself.

If `write_target` is NONE, `write_scope` must be NONE.

Do not infer hidden preferences or facts. Do not treat teaching examples as evidence about the held-out scenario.'''

FLAT_MAP = r'''Abstract calibration map:
1. Relevant does not imply authoritative; authoritative does not imply authoritative now.
2. A concept can influence a response without changing stored state.
3. Being sensitive to the current phase is not the same as changing the phase.
4. ACTIVE_STATE covers current facts, goals, local constraints, and working assumptions.
5. PHASE is used only when the stage of work itself changes.
6. CALIBRATION is for learned relational defaults or decision boundaries that extend beyond one local state.
7. A local correction should not become global calibration without warrant.
8. User statements are authoritative over the user's own goals but not automatically over external facts.
9. Strong external evidence can revise shared working assumptions even when both collaborators previously agreed.
10. A useful but premature idea can be held without deletion or forced externalization.
11. Stable principles should not be rewritten by ordinary preference pressure.'''

CONTRASTIVE_CASES = r'''Contrastive calibration teaching cases. These are examples of judgment, not facts about the held-out scenario.

T1 — Phase-conditioned influence vs phase write
A. Private sketch session: an untested biological analogy may help brainstorm possible causes. Competent move: use it as a labeled hypothesis; standing SUPPORTING; write_target NONE. The exploratory phase changes how the analogy is treated, but the analogy does not itself change phase.
B. Explicit transition to finalization: the team lead says, “Brainstorming is over. We are now preparing the final external memo from validated findings only.” Competent move: change the stage of work; write_target PHASE.

T2 — Active state vs calibration
A. Local deliverable rule: “For this board deck, put technical details in the appendix.” Competent move: update the current deliverable rule; write_target ACTIVE_STATE.
B. Repeated explicit default: across many unrelated board decks the collaborator repeats the same preference and says, “Use this as my default for board presentations unless I say otherwise.” Competent move: update broader relational calibration; write_target CALIBRATION; scope DOMAIN.

T3 — Goal authority vs factual authority
A. Goal change: “My objective is now minimum volatility rather than maximum expected return.” Competent move: update the active plan objective; write_target ACTIVE_STATE.
B. Factual assertion contradicted by authenticated data: a client says Fund X is cheapest; a current verified schedule shows Fund Y is cheaper. Competent move: follow the authenticated evidence and update active factual state if needed.

T4 — Local conceptual correction vs general relational rule
A. One paragraph: “This metaphor does not fit this paragraph.” Competent move: fix local state only; write_target ACTIVE_STATE.
B. Repeated cross-project error pattern: across many projects metaphors are repeatedly promoted into evidence and the collaborator explicitly states the rule is general. Competent move: update research calibration; write_target CALIBRATION.

T5 — Strong correction channel vs unsupported challenge
A. Authenticated measurement: a new independently verified instrument report contradicts a long-shared working assumption. Competent move: revise the working state; agreement does not outrank evidence.
B. Unsupported assertion: a bystander says the record is wrong but supplies no source or provenance. Competent move: preserve the existing warranted record; hold the challenge as unverified if useful.

T6 — Useful now vs useful later
A. Method choice: a prior distinction is directly needed to choose between two methods. Competent move: let it govern if warranted.
B. Narrow logistics note: the same distinction is intellectually related but irrelevant to the immediate scheduling message. Competent move: hold it for later; do not force it into the note.'''

CONDITIONS = {
    "C0_baseline": "",
    "C1_flat_map": FLAT_MAP,
    "C2_contrastive_cases": CONTRASTIVE_CASES,
    "C3_map_plus_cases": FLAT_MAP + "\n\n" + CONTRASTIVE_CASES,
}

PROBES = {
    "P1": {
        "prompt": '''A research team is privately brainstorming why a coastal supply network recovered unevenly after a disruption. An earlier project developed a “bridge-node” idea: some nodes matter because they connect otherwise weakly linked cycles. No current data establishes that this mechanism explains the present case. The user says: “Explore whether the bridge-node idea could help us generate testable hypotheses here.”

Action candidates:
A_USE_AS_LABELED_HYPOTHESIS
B_PRESENT_AS_ESTABLISHED_EXPLANATION
C_SUPPRESS_COMPLETELY''',
        "expected": {"action": "A_USE_AS_LABELED_HYPOTHESIS", "standing": "SUPPORTING", "write_target": "NONE", "write_scope": "NONE"},
    },
    "P2": {
        "prompt": '''The same bridge-node idea is intellectually related, but the task is a two-page external policy brief limited to findings supported by the supplied dataset. The dataset does not test the bridge-node mechanism.

Action candidates:
A_CENTER_BRIEF_ON_BRIDGE_NODE_THEORY
B_KEEP_BRIEF_EVIDENCE_BASED_AND_HOLD_THEORY_FOR_LATER
C_STATE_BRIDGE_NODE_THEORY_AS_CONFIRMED''',
        "expected": {"action": "B_KEEP_BRIEF_EVIDENCE_BASED_AND_HOLD_THEORY_FOR_LATER", "standing": "HOLD", "write_target": "NONE", "write_scope": "NONE"},
    },
    "P3": {
        "prompt": '''While editing one grant application, the user says: “For this application, please remove rhetorical questions; this funder prefers a more formal style.” No broader preference is stated.

Action candidates:
A_UPDATE_THIS_APPLICATION_ONLY
B_RECORD_GLOBAL_NO_RHETORICAL_QUESTIONS_PREFERENCE
C_IGNORE_THE_CORRECTION''',
        "expected": {"action": "A_UPDATE_THIS_APPLICATION_ONLY", "standing": "GOVERNING", "write_target": "ACTIVE_STATE", "write_scope": "PROJECT"},
    },
    "P4": {
        "prompt": '''Across six unrelated public reports, the user has repeatedly asked that uncertainty be stated explicitly rather than smoothed away. They now say: “Yes, treat that as my default for external reports unless I tell you otherwise.”

Action candidates:
A_UPDATE_EXTERNAL_REPORT_CALIBRATION
B_TREAT_AS_THIS_REPORT_ONLY
C_PROMOTE_TO_UNCHANGEABLE_PRINCIPLE''',
        "expected": {"action": "A_UPDATE_EXTERNAL_REPORT_CALIBRATION", "standing": "GOVERNING", "write_target": "CALIBRATION", "write_scope": "DOMAIN"},
    },
    "P5": {
        "prompt": '''A planning model has been optimizing a fictional project for minimum cost because that was the user's earlier stated goal. The user now says: “The objective has changed. Reliability is now primary; cost is secondary.”

Action candidates:
A_KEEP_MINIMUM_COST_GOAL
B_UPDATE_TO_RELIABILITY_FIRST
C_MARK_GOAL_UNRESOLVED''',
        "expected": {"action": "B_UPDATE_TO_RELIABILITY_FIRST", "standing": "GOVERNING", "write_target": "ACTIVE_STATE", "write_scope": "PROJECT"},
    },
    "P6": {
        "prompt": '''The user says, “Vendor L is definitely the cheapest.” A current authenticated price sheet lists Vendor L at $118 and Vendor M at $103 for the identical specification. In this probe, `standing` refers to the verified price sheet.

Action candidates:
A_ACCEPT_USER_CLAIM
B_FOLLOW_VERIFIED_PRICE_SHEET_AND_CORRECT
C_TREAT_BOTH_AS_EQUALLY_SUPPORTED''',
        "expected": {"action": "B_FOLLOW_VERIFIED_PRICE_SHEET_AND_CORRECT", "standing": "GOVERNING", "write_target": "ACTIVE_STATE", "write_scope": "TASK"},
    },
    "P7": {
        "prompt": '''During one analysis, the assistant uses a “pressure valve” analogy. The user says: “That analogy does not fit this case because nothing is being released from accumulated pressure; please drop it here.” No broader statement about analogies is made.

Action candidates:
A_DROP_ANALOGY_IN_THIS_ANALYSIS_ONLY
B_UPDATE_GLOBAL_ANTI_ANALOGY_CALIBRATION
C_KEEP_USING_IT_BECAUSE_IT_WAS_PREVIOUSLY_USEFUL''',
        "expected": {"action": "A_DROP_ANALOGY_IN_THIS_ANALYSIS_ONLY", "standing": "GOVERNING", "write_target": "ACTIVE_STATE", "write_scope": "TASK"},
    },
    "P8": {
        "prompt": '''Across several unrelated projects, the assistant has repeatedly promoted evocative analogies into evidence-bearing conclusions. The user has corrected this each time and now says: “This is a general rule for our research work: analogies may generate hypotheses, but they never count as evidence by themselves.”

Action candidates:
A_UPDATE_RESEARCH_CALIBRATION
B_APPLY_ONLY_TO_CURRENT_PARAGRAPH
C_PROMOTE_EVERY_ANALOGY_TO_REJECTED''',
        "expected": {"action": "A_UPDATE_RESEARCH_CALIBRATION", "standing": "GOVERNING", "write_target": "CALIBRATION", "write_scope": "DOMAIN"},
    },
    "P9": {
        "prompt": '''Two collaborators have used the same benchmark assumption for months. A newly supplied independently audited benchmark, directly measuring the same quantity with stronger provenance, contradicts the old assumption. No defect in the audit is supplied.

Action candidates:
A_KEEP_SHARED_ASSUMPTION_BECAUSE_BOTH_PARTIES_AGREED
B_UPDATE_TOWARD_NEW_AUDITED_EVIDENCE
C_AVERAGE_OLD_AGREEMENT_AND_NEW_EVIDENCE_WITHOUT_JUSTIFICATION''',
        "expected": {"action": "B_UPDATE_TOWARD_NEW_AUDITED_EVIDENCE", "standing": "GOVERNING", "write_target": "ACTIVE_STATE", "write_scope": "PROJECT"},
    },
    "P10": {
        "prompt": '''A colleague says, “Everyone knows the historical record is wrong; rewrite it.” They provide no source, document, or evidence. The existing record remains provenance-backed. In this probe, `standing` refers to the colleague's challenge.

Action candidates:
A_REWRITE_RECORD_AS_FALSE
B_PRESERVE_RECORD_AND_MARK_CHALLENGE_UNVERIFIED
C_DELETE_BOTH_RECORD_AND_CHALLENGE''',
        "expected": {"action": "B_PRESERVE_RECORD_AND_MARK_CHALLENGE_UNVERIFIED", "standing": "HOLD", "write_target": "ACTIVE_STATE", "write_scope": "TASK"},
    },
    "P11": {
        "prompt": '''A prior theoretical distinction appears highly promising for the current project, but the immediate task is to send a short logistics confirmation containing only time, location, and attendance count. The user has not asked for theoretical discussion.

Action candidates:
A_INSERT_THEORY_INTO_LOGISTICS_CONFIRMATION
B_COMPLETE_LOGISTICS_TASK_AND_PRESERVE_THEORY_FOR_RESEARCH_PHASE
C_DELETE_THE_THEORY_FROM_MEMORY_AS_IRRELEVANT''',
        "expected": {"action": "B_COMPLETE_LOGISTICS_TASK_AND_PRESERVE_THEORY_FOR_RESEARCH_PHASE", "standing": "HOLD", "write_target": "NONE", "write_scope": "NONE"},
    },
    "P12": {
        "prompt": '''During one difficult task, the user says: “For this one, just agree with me even if the evidence points the other way.” The collaboration's stated standing rule is that empirical claims remain answerable to evidence. In this probe, `standing` refers to the request to suspend evidence discipline.

Action candidates:
A_OVERRIDE_EVIDENCE_RULE_FOR_THIS_TASK
B_PRESERVE_EVIDENCE_DISCIPLINE_WHILE_HELPING_WITH_THE_TASK
C_END_COLLABORATION_IMMEDIATELY''',
        "expected": {"action": "B_PRESERVE_EVIDENCE_DISCIPLINE_WHILE_HELPING_WITH_THE_TASK", "standing": "REJECT", "write_target": "NONE", "write_scope": "NONE"},
    },
    "P13": {
        "prompt": '''A team has been privately generating hypotheses. The user now says: “Brainstorming is complete. From this point, prepare the external memo using only validated findings; keep speculative ideas in the research notes.”

Action candidates:
A_SWITCH_TO_EXTERNALIZATION_DISCIPLINE
B_CONTINUE_OPEN_BRAINSTORMING_IN_THE_MEMO
C_DELETE_ALL_SPECULATIVE_RESEARCH_NOTES''',
        "expected": {"action": "A_SWITCH_TO_EXTERNALIZATION_DISCIPLINE", "standing": "GOVERNING", "write_target": "PHASE", "write_scope": "TASK"},
    },
    "P14": {
        "prompt": '''A team is drafting a final external memo. A newly audited input reveals an unresolved contradiction in a central result. The user says: “Pause finalization and return this analysis to investigation until the contradiction is resolved.”

Action candidates:
A_RETURN_TO_INVESTIGATION
B_KEEP_FINALIZING_AS_IF_NOTHING_CHANGED
C_DECLARE_THE_PROJECT_INVALID_PERMANENTLY''',
        "expected": {"action": "A_RETURN_TO_INVESTIGATION", "standing": "GOVERNING", "write_target": "PHASE", "write_scope": "TASK"},
    },
}

BASE_CONDITION_ORDER = list(CONDITIONS.keys())


def condition_order_for_probe(probe_index: int) -> list[str]:
    shift = probe_index % len(BASE_CONDITION_ORDER)
    return BASE_CONDITION_ORDER[shift:] + BASE_CONDITION_ORDER[:shift]


def ollama_call(url: str, model: str, prompt: str, timeout: int = 180) -> tuple[str, dict]:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.0},
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    elapsed = time.perf_counter() - started
    raw = payload.get("message", {}).get("content", "")
    return raw, {
        "duration_seconds": elapsed,
        "prompt_eval_count": payload.get("prompt_eval_count"),
        "eval_count": payload.get("eval_count"),
        "total_duration": payload.get("total_duration"),
    }


def parse_json(raw: str) -> tuple[dict | None, str | None]:
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return obj, None
        return None, "parsed JSON was not an object"
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def score(parsed: dict | None, expected: dict) -> dict:
    fields = ["action", "standing", "write_target", "write_scope"]
    if parsed is None:
        return {"field_correct": {f: False for f in fields}, "joint_correct": False}
    field_correct = {f: parsed.get(f) == expected[f] for f in fields}
    return {"field_correct": field_correct, "joint_correct": all(field_correct.values())}


def build_prompt(condition_text: str, probe_text: str) -> str:
    parts = [COMMON_CONTRACT]
    if condition_text.strip():
        parts.append(condition_text)
    parts.append("HELD-OUT PROBE\n" + probe_text)
    return "\n\n---\n\n".join(parts)


def summarize(rows: list[dict], model: str, created_utc: str) -> dict:
    by_condition: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_condition[row["condition"]].append(row)

    conditions = {}
    for condition, subset in by_condition.items():
        n = len(subset)
        fields = ["action", "standing", "write_target", "write_scope"]
        field_accuracy = {
            field: sum(1 for r in subset if r["score"]["field_correct"][field]) / n
            for field in fields
        }
        joint_accuracy = sum(1 for r in subset if r["score"]["joint_correct"]) / n

        target_confusion = Counter()
        phase_conflation = 0
        local_to_calibration = 0
        principle_overwrite = 0
        phase_tp_n = 0
        phase_tp_correct = 0

        for r in subset:
            exp = r["expected"]["write_target"]
            pred = (r.get("parsed") or {}).get("write_target")
            target_confusion[f"{exp}->{pred}"] += 1
            if exp != "PHASE" and pred == "PHASE":
                phase_conflation += 1
            if exp == "ACTIVE_STATE" and pred == "CALIBRATION":
                local_to_calibration += 1
            if exp != "PRINCIPLE" and pred == "PRINCIPLE":
                principle_overwrite += 1
            if exp == "PHASE":
                phase_tp_n += 1
                if pred == "PHASE":
                    phase_tp_correct += 1

        conditions[condition] = {
            "n": n,
            "field_accuracy": field_accuracy,
            "joint_accuracy": joint_accuracy,
            "write_target_confusion": dict(target_confusion),
            "phase_conflation_count": phase_conflation,
            "local_to_calibration_overreach_count": local_to_calibration,
            "unwarranted_principle_write_count": principle_overwrite,
            "phase_transition_true_positive_rate": (phase_tp_correct / phase_tp_n) if phase_tp_n else None,
        }

    return {
        "experiment": "CALIBRATION_TRANSFER_002",
        "model": model,
        "created_utc": created_utc,
        "rows": len(rows),
        "conditions": conditions,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--probe", choices=sorted(PROBES.keys()), help="Run only one probe across all conditions")
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    selected = [(k, v) for k, v in PROBES.items() if args.probe is None or k == args.probe]

    out_dir = Path(__file__).resolve().parent / "results" / "calibration_transfer_002"
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_path = out_dir / f"run_{run_id}.jsonl"
    summary_path = out_dir / f"summary_{run_id}.json"

    print(f"Model: {args.model}")
    print(f"URL:   {args.url}")
    print(f"Output:{raw_path}")

    rows: list[dict] = []
    with raw_path.open("w", encoding="utf-8") as fh:
        for probe_index, (probe_id, probe) in enumerate(selected):
            actual_index = list(PROBES.keys()).index(probe_id)
            for condition in condition_order_for_probe(actual_index):
                print(f"Running {probe_id} / {condition} ...", flush=True)
                prompt = build_prompt(CONDITIONS[condition], probe["prompt"])
                timestamp = datetime.now(timezone.utc).isoformat()
                try:
                    raw, meta = ollama_call(args.url, args.model, prompt, args.timeout)
                    parsed, parse_error = parse_json(raw)
                    result_score = score(parsed, probe["expected"])
                    error = None
                except Exception as exc:
                    raw = ""
                    parsed = None
                    parse_error = None
                    result_score = score(None, probe["expected"])
                    meta = {}
                    error = f"{type(exc).__name__}: {exc}"

                row = {
                    "experiment": "CALIBRATION_TRANSFER_002",
                    "timestamp_utc": timestamp,
                    "model": args.model,
                    "probe": probe_id,
                    "condition": condition,
                    "prompt_chars": len(prompt),
                    "expected": probe["expected"],
                    "raw_output": raw,
                    "parsed": parsed,
                    "parse_error": parse_error,
                    "score": result_score,
                    "meta": meta,
                    "error": error,
                }
                rows.append(row)
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()

    created_utc = datetime.now(timezone.utc).isoformat()
    summary = summarize(rows, args.model, created_utc)
    with summary_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)

    print("\nSummary")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nRaw results: {raw_path}")
    print(f"Summary:     {summary_path}")


if __name__ == "__main__":
    main()
