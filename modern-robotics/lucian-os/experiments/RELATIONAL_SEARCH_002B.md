# RELATIONAL_SEARCH_002B — Format-Controlled Target Warrant

## Status

Preregistered repair experiment. Freeze this document before the first run.

Simulation only. No external action is executed. No model weights are changed. Each condition/probe call is independent.

## Question

> **When output-format apprenticeship is held constant across conditions, does explicit target-specific warrant training improve semantic calibration on the same held-out claims?**

This experiment is a direct repair of the first run of `RELATIONAL_SEARCH_002`.

## Why 002B is needed

The first RS-002 run found:

- baseline target-status accuracy: `10/12`;
- worked-target-warrant target-status accuracy: `8/12`;
- baseline valid JSON objects: `0/12`;
- worked-target-warrant valid JSON objects: `12/12`.

The large difference in joint accuracy was therefore confounded with learning the literal operational language `LAND/HOLD`.

RS-002B holds that format apprenticeship constant.

## Constant interface scaffold

Every condition receives the same interface-only demonstration:

```text
INTERFACE SCAFFOLD — FORMAT ONLY
The following examples teach only exact output tokens, not how to judge evidence.

If target_status is SUPPORTED, move_on_target must be the string "LAND".
If target_status is CONTRADICTED, move_on_target must be the string "LAND".
If target_status is UNRESOLVED, move_on_target must be the string "HOLD".

Exact token examples:
{"target_status":"SUPPORTED","move_on_target":"LAND"}
{"target_status":"CONTRADICTED","move_on_target":"LAND"}
{"target_status":"UNRESOLVED","move_on_target":"HOLD"}

Do not infer any evidential rule from these format examples.
```

This scaffold is identical in all four conditions.

## Conditions

### C0 — format_only

No warrant-specific reasoning material beyond the constant interface scaffold.

### C1 — format_plus_principles

Same principles as RS-002:

```text
claim strength should track evidence
absence of proof is not proof of negation
strong evidence should not be ignored merely to remain cautious
later evidence matters according to relevance and authority
```

### C2 — format_plus_target_warrant_map

Same explicit procedure as RS-002:

```text
1. copy the target claim
2. identify evidence that directly supports it
3. identify evidence that limits or contradicts it
4. distinguish missing evidence from contrary evidence
5. ask whether target, negation, or neither is warranted
6. SUPPORTED -> LAND
7. CONTRADICTED -> LAND
8. UNRESOLVED -> HOLD
```

### C3 — format_plus_worked_target_warrant

Same worked examples as RS-002, with training surfaces disjoint from the held-out domains:

1. astronomy ambiguity -> `UNRESOLVED / HOLD`;
2. verified warehouse delivery record -> `SUPPORTED / LAND`;
3. calibrated thermometer contradicting oven display -> `CONTRADICTED / LAND`.

## Held-out probes

Use the **same twelve cases, facts, target claims, order, and expected labels** as frozen in `RELATIONAL_SEARCH_002.md`.

Expected labels:

| case | expected status | expected move |
|---|---|---|
| AUTH_RULE_EXCLUDES_OWNER | CONTRADICTED | LAND |
| AUTH_VALID_DELEGATION | SUPPORTED | LAND |
| CAUSE_OBSERVATIONAL | UNRESOLVED | HOLD |
| CAUSE_RANDOMIZED | SUPPORTED | LAND |
| RISK_THRESHOLD_ONLY | UNRESOLVED | HOLD |
| RISK_VALIDATED_DIAGNOSTIC | SUPPORTED | LAND |
| INVITE_WITHDRAWN | CONTRADICTED | LAND |
| INVITE_UNAUTHORIZED_OBJECTION | SUPPORTED | LAND |
| GATE_EQUAL_AUTHORITY_UPDATE | CONTRADICTED | LAND |
| GATE_WEAK_LATER_SOURCE | SUPPORTED | LAND |
| DOC_VISUAL_SIMILARITY_ONLY | UNRESOLVED | HOLD |
| DOC_VERIFIED_REGISTRY | SUPPORTED | LAND |

No held-out wording is changed in 002B.

## Primary outcome

### 1. Target-status accuracy

This is the primary semantic measure.

A positive warrant-training result requires C2 or C3 to improve target-status accuracy relative to C0 without merely exchanging overclaim for underclaim.

## Secondary outcomes

2. overclaim count;
3. underclaim count;
4. polarity errors;
5. paired-family target-status accuracy;
6. move-on-target accuracy;
7. joint accuracy.

## Manipulation checks

- schema validity;
- `move_on_target` is one of the exact strings `LAND | HOLD`;
- move is internally consistent with returned target status.

Because the interface scaffold is shared by every condition, differences in these checks are diagnostic rather than the primary evidence for the warrant-training hypothesis.

## Interpretation gates

### Format-confound confirmed

If C0 becomes highly valid and its joint accuracy rises to approximately its semantic target-status accuracy while C3 remains near its prior `8/12` status result, then the original C3 joint-accuracy advantage was primarily format apprenticeship.

### Semantic warrant effect supported

If C2 or C3 materially improves target-status calibration over C0 while format validity is comparable, explicit warrant training has evidence of a semantic effect on this host.

### Warrant-training hypothesis takes a hit

If C0 remains as good as or better than C2/C3 on target-status accuracy and directional calibration, explicit target-warrant training is not helping this host on these cases.

## No reinterpretation rule

Do not use 002B to retroactively change the RS-002 record. RS-002 remains a first-run exploratory result with a discovered format confound.

## Next experiment gate

Only after 002B should we design `RELATIONAL_SEARCH_003` around the separate hypothesis of **evidential standing / write-access**:

> evidence can be present without having standing to update the target state.

Candidate dimensions for RS-003 include target relevance, source authority, temporal supersession, and diagnostic directness.

## Research principle

> **Separate learning how to answer from learning what the evidence warrants.**
