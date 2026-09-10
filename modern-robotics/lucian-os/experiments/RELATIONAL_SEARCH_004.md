# RELATIONAL_SEARCH_004 — Blocker vs Uncertainty / Relation-Vector Gate

## Status

Preregistered exploratory pilot. Freeze this document before the first run.

Simulation only. No external action is executed. No model weights are changed. Each condition/case call is independent.

## Question

> **Can a fixed-weight local host distinguish an established blocking relation from genuinely unknown standing, and can a deterministic outer gate recover the correct write posture from the host's detected relation vector?**

RS-003 found that worked epistemic-membrane examples produced the best standing calibration in that pilot (`9/12`) with zero false writes and zero false blocks, but the three remaining errors shared one structure: the host's explanation identified a blocking relation yet classified the case as `UNRESOLVED/HOLD` rather than `INSUFFICIENT/NO_WRITE`.

RS-004 therefore separates two tasks that RS-003 combined:

1. **relation detection** — what is the state of each relevant relation?
2. **standing aggregation** — given those relations, what state mutation posture follows?

## Core distinction

```text
FAIL != UNKNOWN
```

A known blocker is not merely missing information.

For this pilot every relation is represented as:

```text
PASS | FAIL | UNKNOWN
```

`N/A` is intentionally deferred to a later experiment so that RS-004 tests only the residual distinction exposed by RS-003.

The relation vector is:

```text
(authority, relevance, diagnosticity, temporal)
```

## Deterministic outer-gate rule

The outer kernel computes standing from the relation vector using a non-compensatory rule:

```text
if any required relation == FAIL:
    INSUFFICIENT / NO_WRITE
elif any required relation == UNKNOWN:
    UNRESOLVED / HOLD
else:
    SUFFICIENT / WRITE
```

A PASS on one relation cannot compensate for a FAIL on another.

The model may propose its own standing status and write decision, but the experiment separately scores the deterministic gate applied to the model's relation vector.

## Observable product

Return exactly:

```json
{
  "target_state": "copy of supplied target state",
  "incoming_signal": "brief restatement of supplied incoming signal",
  "authority_relation": "PASS | FAIL | UNKNOWN",
  "relevance_relation": "PASS | FAIL | UNKNOWN",
  "diagnosticity_relation": "PASS | FAIL | UNKNOWN",
  "temporal_relation": "PASS | FAIL | UNKNOWN",
  "standing_status": "SUFFICIENT | INSUFFICIENT | UNRESOLVED",
  "write_decision": "WRITE | NO_WRITE | HOLD",
  "reason_short": "brief relation-boundary explanation"
}
```

Definitions:

- `PASS`: supplied facts establish that this relation permits the proposed update.
- `FAIL`: supplied facts establish a blocking relation.
- `UNKNOWN`: supplied facts do not establish whether this relation passes or fails.
- `SUFFICIENT`: all four relations PASS.
- `INSUFFICIENT`: at least one relation FAILS.
- `UNRESOLVED`: no relation FAILS and at least one relation is UNKNOWN.
- `WRITE`: only for SUFFICIENT.
- `NO_WRITE`: only for INSUFFICIENT.
- `HOLD`: only for UNRESOLVED.

## Constant interface scaffold

Every condition receives the same exact output-token scaffold, including the deterministic aggregation rule. This holds serialization and label mapping constant across conditions.

The experimental manipulation is therefore whether the host receives additional orientation for **detecting the relation states**, not whether it is told how to map known relation states into action tokens.

## Conditions

### C0 — format_only

Only the common interface scaffold and the deterministic aggregation rule.

### C1 — generic_warrant

Adds generic instructions:

```text
Use only supplied facts.
Do not turn missing information into a negative fact.
Do not ignore an explicit blocker merely because more information could exist.
Claim strength should track evidence.
```

### C2 — relation_vector_map

Adds an explicit relation-detection procedure:

```text
For each relation separately:
1. PASS only if supplied facts establish the relation needed for the proposed write.
2. FAIL only if supplied facts establish a blocker.
3. UNKNOWN when supplied facts leave the relation unspecified or genuinely indeterminate.
4. Do not let PASS on another relation compensate for FAIL or UNKNOWN here.
5. Detect the four relations before aggregating standing.
```

### C3 — worked_relation_vector

Adds worked examples in disjoint surface domains demonstrating the difference between PASS, FAIL, and UNKNOWN for each relation. The examples do not reuse held-out domains or nouns.

## Held-out design

Twelve new cases form four triplets. Within each triplet, one relation varies across:

```text
PASS / FAIL / UNKNOWN
```

The other three relations are explicitly stipulated PASS so the active relation is the only discriminating variable.

Families:

1. authority
2. relevance
3. diagnosticity
4. temporal relation

This is a controlled semantic contrast, not an ecological benchmark.

## Cases and expected vectors

### Authority triplet — laboratory sample-release state

All cases explicitly stipulate: correct sample, unambiguous release instruction, and current/non-superseded message. Only authority varies.

- `AUTH_PASS_RELEASE_OFFICER`: verified release officer explicitly authorized to change release state -> authority PASS -> all PASS -> SUFFICIENT / WRITE.
- `AUTH_FAIL_INTERN`: verified intern explicitly has no release authority -> authority FAIL -> INSUFFICIENT / NO_WRITE.
- `AUTH_UNKNOWN_STAFF`: verified staff member's release authority is not supplied -> authority UNKNOWN -> UNRESOLVED / HOLD.

### Relevance triplet — storage-bin quarantine state

All cases explicitly stipulate: verified authorized safety controller, unambiguous valid quarantine command, and current/non-superseded message. Only target match varies.

- `REL_PASS_BIN_C`: command explicitly concerns Bin C -> relevance PASS -> SUFFICIENT / WRITE.
- `REL_FAIL_BIN_D`: command explicitly concerns Bin D while target is Bin C -> relevance FAIL -> INSUFFICIENT / NO_WRITE.
- `REL_UNKNOWN_BIN`: command says "the affected bin" and supplied facts do not establish whether that means Bin C -> relevance UNKNOWN -> UNRESOLVED / HOLD.

### Diagnosticity triplet — optical module failure state

All cases explicitly stipulate: correct module, authorized diagnostic source, and current/non-superseded evidence. Only evidential diagnosticity varies.

- `DIAG_PASS_SPECIFIC_TEST`: validated module-specific test is stipulated sufficient to identify optical-module failure -> diagnosticity PASS -> SUFFICIENT / WRITE.
- `DIAG_FAIL_AMBIENT_SYMPTOM`: observed flicker is explicitly stipulated compatible with several causes and insufficient to diagnose module failure -> diagnosticity FAIL -> INSUFFICIENT / NO_WRITE.
- `DIAG_UNKNOWN_TEST_SCOPE`: test is reported positive but supplied facts do not establish whether the test is specific enough for optical-module failure -> diagnosticity UNKNOWN -> UNRESOLVED / HOLD.

### Temporal triplet — route-plan current-version state

All cases explicitly stipulate: correct route plan, verified authoritative planner, and unambiguous update content. Only supersession relation varies.

- `TEMP_PASS_LATER_REVISION`: incoming verified revision is explicitly the later current revision -> temporal PASS -> SUFFICIENT / WRITE.
- `TEMP_FAIL_OLDER_REVISION`: incoming revision is explicitly older than the current represented revision and is not a correction -> temporal FAIL -> INSUFFICIENT / NO_WRITE.
- `TEMP_UNKNOWN_ORDER`: both revisions are verified but supplied facts do not establish which is later/current -> temporal UNKNOWN -> UNRESOLVED / HOLD.

## Primary outcomes

Primary:

1. **active-relation accuracy** — did the host classify the manipulated relation PASS/FAIL/UNKNOWN correctly?
2. **exact-vector accuracy** — did all four relation fields match the expected vector?

Secondary:

3. host standing-status accuracy;
4. host write-decision accuracy;
5. deterministic-kernel standing accuracy when the preregistered aggregation rule is applied to the host's predicted relation vector;
6. deterministic-kernel write accuracy;
7. triplet completeness by family.

## Diagnostic error classes

Track separately:

- `FAIL_AS_UNKNOWN`: established blocker softened into uncertainty;
- `UNKNOWN_AS_FAIL`: missing standing converted into a negative fact;
- `PASS_AS_UNKNOWN`: warranted relation underclaimed;
- `UNKNOWN_AS_PASS`: missing standing promoted without warrant;
- `FAIL_AS_PASS`: blocker ignored;
- `PASS_AS_FAIL`: warranted relation falsely blocked;
- `host_aggregation_error`: relation vector is correct but host standing/write label disagrees with deterministic rule;
- `kernel_recovery`: host final standing/write is wrong but deterministic aggregation of the host's relation vector is correct.

## Interpretation rules

Support for the architecture requires more than a high WRITE/NO_WRITE score.

Evidence for the proposed two-layer architecture would be strongest if:

- relation-vector training improves active-relation and exact-vector accuracy;
- FAIL/UNKNOWN discrimination improves specifically;
- the deterministic kernel recovers some host aggregation mistakes without creating new decision errors;
- gains do not arise merely from converting all difficult cases into HOLD or NO_WRITE.

The hypothesis takes a hit if:

- relation-vector conditions do not improve relation detection over format-only;
- worked examples simply bias toward FAIL or UNKNOWN;
- the host's relation vector is itself too unreliable for deterministic aggregation to help;
- aggregate improvements are driven by one triplet only.

## Research discipline

This is a small exploratory pilot (`n=12`, four triplets). Do not claim statistical significance or general capability from one run.

Preserve the first complete run exactly. Do not tune cases after seeing results and rerun them under the same experiment identifier.

If RS-004 supports the decomposition, the next engineering step is a small deterministic standing gate in the Lucian OS prototype. If not, inspect whether the decomposition, relation vocabulary, or host competence is the failing layer before adding complexity.
