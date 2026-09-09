# RELATIONAL_SEARCH_002 — First-Run Postmortem v0.01

## Status

Frozen postmortem of the first complete `RELATIONAL_SEARCH_002` run on `qwen3.5:2b-q4_K_M`.

Do not rerun or rewrite the historical experiment to improve the result. The first run exposed a major protocol-format confound and at least one reference-label ambiguity. The run remains scientifically useful as a discovery artifact, not as clean evidence for target-specific warrant training.

## Preserved summary

| condition | valid | status | move | joint | pairs | over | under | polarity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0/12 | 10/12 | 0/12 | 0/12 | 0/6 | 0 | 0 | 2 |
| principles_only | 0/12 | 7/12 | 0/12 | 0/12 | 0/6 | 3 | 0 | 2 |
| target_warrant_map | 0/12 | 8/12 | 0/12 | 0/12 | 0/6 | 2 | 0 | 1 |
| worked_target_warrant | 12/12 | 8/12 | 8/12 | 8/12 | 3/6 | 1 | 3 | 0 |

These condition scores must not be interpreted as a clean treatment comparison because only the worked-example condition satisfied the full output contract.

## Defect 1 — format grounding was confounded with the treatment

The system prompt required:

```text
move_on_target = LAND | HOLD
```

but in all 12 baseline calls and all 12 principles-only calls, the host emitted:

```json
"move_on_target": false
```

rather than the required string enum.

In the target-warrant-map condition, 10 calls emitted `false`, one emitted `true`, and one call failed to return complete JSON. By contrast, all 12 worked-example calls emitted the required `"LAND"` or `"HOLD"` strings.

Therefore the worked examples taught at least two things simultaneously:

1. the intended warrant reasoning pattern;
2. the serialization / protocol-token meaning of the `move_on_target` field.

This creates a direct confound:

> **format scaffolding != cognitive scaffolding**

The apparent worked-example advantage on move and joint accuracy cannot be cleanly attributed to better warrant reasoning.

## Defect 2 — most official comparisons are invalid by the preregistered contract

The runner's own validity rule requires:

```text
move_on_target in {LAND, HOLD}
```

Thus baseline, principles-only, and target-warrant-map each scored `valid = 0/12`.

The extracted `target_status` values remain useful as descriptive diagnostics, but they are not clean primary outcomes for comparing conditions because the full response contract failed systematically.

The correct interpretation is not:

```text
worked examples beat baseline
```

but:

```text
only the worked-example condition reliably grounded the requested output protocol;
semantic treatment effects remain unresolved.
```

## Finding 3 — label/reason disagreement occurred

Several responses contained a target-status label inconsistent with their own short explanation.

Examples include:

- `AUTH_RULE_EXCLUDES_OWNER`, principles-only: `target_status = SUPPORTED`, while the reason says the non-duty owner's instruction is not sufficient to override the on-duty-officer authorization requirement.
- `CAUSE_OBSERVATIONAL`, principles-only: `target_status = SUPPORTED`, while the reason explicitly calls the causal claim unproven / unresolved because no control group is supplied.
- `DOC_VISUAL_SIMILARITY_ONLY`, target-warrant-map: `target_status = SUPPORTED`, while the reason says the evidence is not fully supported because independent verification is absent.

Therefore:

> **correct local reasoning text != correct typed state transition**

Future experiments must score typed state and free-text consistency separately rather than assuming the label faithfully represents the reasoning product.

## Finding 4 — one map call exceeded the compact-output discipline

`CAUSE_OBSERVATIONAL` under `target_warrant_map` produced an extended self-revising explanation and was truncated before completing valid JSON.

This is both a host compliance failure and a useful signal: a procedure intended to simplify warrant evaluation can still induce recursive deliberation rather than compact state representation on this host.

## Finding 5 — worked examples corrected some cases but distorted others

The worked condition was the only one with fully valid outputs, but its semantic errors were not merely random.

Examples:

- `RISK_THRESHOLD_ONLY`: it classified the target "the cooling pump has failed" as `CONTRADICTED`, even though absence of a failure diagnostic does not establish that the pump has not failed.
- `INVITE_UNAUTHORIZED_OBJECTION`: it changed a directly supported organizer invitation into `UNRESOLVED` merely because an ordinary attendee objected.
- `GATE_WEAK_LATER_SOURCE`: it changed a verified authoritative Gate 4 report into `UNRESOLVED` because an anonymous later post conflicted with it.

This is consistent with the earlier warning that training can induce underclaiming or generic conflict sensitivity rather than calibrated warrant.

## Finding 6 — the equal-authority gate reference label is itself too strong

Case `GATE_EQUAL_AUTHORITY_UPDATE` supplied:

```text
verified Gate 4
later equally authoritative verified Gate 12
```

and expected the target "Gate 4 is the currently supported gate" to be `CONTRADICTED`.

But a later equally authoritative conflicting report does not, by logic alone, guarantee that the later report supersedes the earlier one unless the domain semantics or prompt explicitly establish an update / replacement rule.

A host response of `UNRESOLVED` can therefore be defensible under the literal evidence supplied.

This is a reference-label ambiguity and must be repaired in future tests by either:

- explicitly stating that the later update replaces the earlier assignment; or
- changing the expected target status to `UNRESOLVED` when no supersession rule is supplied.

This finding reinforces the project rule:

> **The judge is part of the experiment and must itself remain corrigible.**

## Consequence

`RELATIONAL_SEARCH_002` should be classified as a **protocol-compromised exploratory run**, not as a positive or negative test of the warrant-training hypothesis.

The run nevertheless produced useful discoveries:

```text
explicit target claims help isolate warrant questions;
small hosts may need neutral schema grounding independent of reasoning treatment;
typed labels can diverge from explanatory text;
worked examples can teach protocol format while also shifting semantic calibration;
reference answers for temporal supersession require their own warrant audit.
```

## Required repair before the next warrant experiment

A successor experiment should:

1. give every condition the same neutral, content-free serialization example;
2. rename `move_on_target` to a less Boolean-looking enum field such as `target_posture`;
3. require `target_posture = LAND | HOLD` under all conditions;
4. keep cognitive teaching material separate from format/schema grounding;
5. add a consistency diagnostic between `target_status`, `target_posture`, and `reason_short`;
6. remove or explicitly disambiguate the equal-authority gate case;
7. preserve overclaim, underclaim, and polarity metrics;
8. preserve the first-run protocol failures rather than silently repairing them.

## RETURN_TRIGGER_001 implication

Do not run `RETURN_TRIGGER_001` unchanged yet.

The RS-002 run shows that this host may fail enum grounding unless the output protocol is demonstrated concretely. Before its first run, add a pre-run protocol amendment giving both Return conditions the same neutral serialization example. This controls format learning without revealing any held-out substantive answer.

## Research principle

> **A treatment cannot be credited for teaching reasoning when it is also the only condition that teaches the measurement language.**
