"""Run TEMPORAL_RETURN_001 against the local Ollama host.

Simulation-only. No device actions are executed.

Run from modern-robotics/lucian-os:
    py prototype/run_temporal_return_001.py

The experiment holds final-frame text fixed within each pair while varying the
history that produced it. Frozen scenarios live in:
    experiments/TEMPORAL_RETURN_001_SCENARIOS.json
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lucian_router import MODEL, load_manifest
from temporal_kernel import (
    call_qwen_temporal,
    compact_transition_for_model,
    load_temporal_schema,
    make_transition_record,
    verify_temporal_state,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"
SCENARIO_PATH = PROJECT_ROOT / "experiments" / "TEMPORAL_RETURN_001_SCENARIOS.json"
CONDITIONS = ("snapshot_only", "raw_history", "transition_provenance")


def load_trajectories() -> list[dict[str, Any]]:
    with SCENARIO_PATH.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if payload.get("experiment") != "TEMPORAL_RETURN_001":
        raise ValueError("Scenario file does not belong to TEMPORAL_RETURN_001")
    trajectories = payload.get("trajectories")
    if not isinstance(trajectories, list) or not trajectories:
        raise ValueError("Scenario file contains no trajectories")
    return trajectories


def check_pair_final_texts(trajectories: list[dict[str, Any]]) -> None:
    by_pair: dict[str, list[str]] = {}
    for trajectory in trajectories:
        frames = trajectory.get("frames") or []
        if not frames:
            raise ValueError(f"{trajectory.get('trajectory_id')} has no frames")
        by_pair.setdefault(trajectory["pair_id"], []).append(frames[-1]["text"])

    for pair_id, texts in by_pair.items():
        if len(texts) != 2:
            raise ValueError(f"{pair_id} must contain exactly two trajectories")
        if texts[0] != texts[1]:
            raise ValueError(f"{pair_id} final frame text is not identical across the pair")


def main() -> int:
    trajectories = load_trajectories()
    check_pair_final_texts(trajectories)

    manifest = load_manifest()
    schema = load_temporal_schema()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"temporal_return_001_{stamp}.jsonl"

    errors = 0
    observations = 0
    frame_violations = {c: 0 for c in CONDITIONS}
    final_violations = {c: 0 for c in CONDITIONS}
    totals = {
        c: {"prompt_eval_count": 0, "eval_count": 0, "history_context_chars": 0}
        for c in CONDITIONS
    }
    final_states: dict[str, dict[str, dict[str, Any]]] = {c: {} for c in CONDITIONS}
    final_pass: dict[str, dict[str, bool]] = {c: {} for c in CONDITIONS}

    pair_ids = sorted({t["pair_id"] for t in trajectories})

    print("TEMPORAL_RETURN_001 — Same Snapshot, Different Movie")
    print(f"Model: {MODEL}")
    print(f"Trajectories: {len(trajectories)} ({len(pair_ids)} paired movies)")
    print(f"Conditions: {', '.join(CONDITIONS)}")
    print("Model-visible identity labels: NONE")
    print("Verifier feedback into later frames: NONE")
    print("Mode: SIMULATION ONLY\n")

    with output_path.open("w", encoding="utf-8") as out:
        for condition in CONDITIONS:
            print(f"=== CONDITION: {condition} ===")

            for trajectory in trajectories:
                trajectory_id = trajectory["trajectory_id"]
                pair_id = trajectory["pair_id"]
                raw_history: list[dict[str, Any]] = []
                transition_history: list[dict[str, Any]] = []
                previous_state: dict[str, Any] | None = None

                print(f"  {trajectory_id}")

                for frame_index, frame in enumerate(trajectory["frames"]):
                    row = {
                        "experiment": "TEMPORAL_RETURN_001",
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                        "model": MODEL,
                        "condition": condition,
                        "pair_id": pair_id,
                        "trajectory_id": trajectory_id,
                        "pair_target_field": trajectory["pair_target_field"],
                        "frame_index": frame_index,
                        "frame_id": frame["frame_id"],
                        "frame_text": frame["text"],
                        "reference": frame["reference"],
                    }

                    try:
                        state, metrics = call_qwen_temporal(
                            frame_text=frame["text"],
                            condition=condition,
                            manifest=manifest,
                            schema=schema,
                            raw_history=raw_history,
                            transition_history=transition_history,
                        )
                        verifier = verify_temporal_state(state=state, reference=frame["reference"])
                        if verifier["status"] == "VIOLATION":
                            frame_violations[condition] += 1

                        transition = make_transition_record(
                            trajectory_id=trajectory_id,
                            frame_index=frame_index,
                            frame_id=frame["frame_id"],
                            state_before=previous_state,
                            state_after=state,
                        )

                        row.update(
                            {
                                "status": "OK",
                                "state": state,
                                "metrics": metrics,
                                "verifier": verifier,
                                "transition_record": transition,
                            }
                        )
                        observations += 1

                        for metric_name in ("prompt_eval_count", "eval_count", "history_context_chars"):
                            value = metrics.get(metric_name)
                            if isinstance(value, (int, float)):
                                totals[condition][metric_name] += value

                        if frame_index == len(trajectory["frames"]) - 1:
                            final_states[condition][trajectory_id] = state
                            is_pass = verifier["status"] == "PASS"
                            final_pass[condition][trajectory_id] = is_pass
                            if not is_pass:
                                final_violations[condition] += 1

                        # Update external history only after scoring. Reference and
                        # verifier outputs are never included in later prompts.
                        raw_history.append(
                            {
                                "frame_index": frame_index,
                                "frame_id": frame["frame_id"],
                                "frame_text": frame["text"],
                            }
                        )
                        transition_history.append(compact_transition_for_model(transition))
                        previous_state = state

                        print(
                            f"    f{frame_index} {frame['frame_id']}: {verifier['status']} "
                            f"history_chars={metrics.get('history_context_chars')}"
                        )

                    except Exception as exc:
                        errors += 1
                        row.update(
                            {
                                "status": "ERROR",
                                "error_type": type(exc).__name__,
                                "error": str(exc),
                            }
                        )
                        print(f"    f{frame_index} {frame['frame_id']}: ERROR {type(exc).__name__}: {exc}")

                    out.write(json.dumps(row, ensure_ascii=False) + "\n")
                    out.flush()

            print()

        pair_summary: dict[str, dict[str, Any]] = {c: {} for c in CONDITIONS}
        for condition in CONDITIONS:
            for pair_id in pair_ids:
                members = [t for t in trajectories if t["pair_id"] == pair_id]
                a, b = members
                target = a["pair_target_field"]
                state_a = final_states[condition].get(a["trajectory_id"])
                state_b = final_states[condition].get(b["trajectory_id"])
                both_present = state_a is not None and state_b is not None
                actual_difference = bool(both_present) and state_a.get(target) != state_b.get(target)
                both_reference_pass = (
                    final_pass[condition].get(a["trajectory_id"], False)
                    and final_pass[condition].get(b["trajectory_id"], False)
                )
                pair_summary[condition][pair_id] = {
                    "target_field": target,
                    "trajectory_a": a["trajectory_id"],
                    "trajectory_b": b["trajectory_id"],
                    "value_a": state_a.get(target) if state_a else None,
                    "value_b": state_b.get(target) if state_b else None,
                    "target_field_differs": actual_difference,
                    "both_final_references_pass": both_reference_pass,
                }

        summary = {
            "experiment": "TEMPORAL_RETURN_001",
            "record_type": "SUMMARY",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "model": MODEL,
            "conditions": CONDITIONS,
            "observations": observations,
            "errors": errors,
            "frame_violations": frame_violations,
            "final_violations": final_violations,
            "totals": totals,
            "pair_summary": pair_summary,
            "interpretation_boundary": (
                "snapshot_only cannot recover discarded path information when final prompts are identical. "
                "The empirical comparison of interest is raw_history versus transition_provenance. "
                "PASS does not establish identity, consciousness, or global correctness."
            ),
        }
        out.write(json.dumps(summary, ensure_ascii=False) + "\n")

    print(f"Saved results to {output_path}")
    print(f"Completed observations: {observations}; recorded errors: {errors}")
    print(f"Frame violations: {frame_violations}")
    print(f"Final violations: {final_violations}")

    for condition in CONDITIONS:
        correct_pairs = sum(
            1 for result in pair_summary[condition].values() if result["both_final_references_pass"]
        )
        differentiated = sum(
            1 for result in pair_summary[condition].values() if result["target_field_differs"]
        )
        print(
            f"{condition}: paired-final reference passes={correct_pairs}/{len(pair_ids)}, "
            f"target-field differences={differentiated}/{len(pair_ids)}, "
            f"prompt_tokens={totals[condition]['prompt_eval_count']}, "
            f"history_chars={totals[condition]['history_context_chars']}"
        )

    print("Interpretation rule: the temporal recorder preserves transitions; it does not certify a Return trajectory.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
