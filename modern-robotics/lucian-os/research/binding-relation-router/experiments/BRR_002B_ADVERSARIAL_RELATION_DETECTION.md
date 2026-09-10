# BRR-002B — Adversarial Relation Detection

## Status

Preregistered internal/procedural experiment. Same-assistant authorship is a known limitation.

Simulation only. No external action is executed.

## Question

> **When two problem descriptions are nearly surface-identical but differ in one relation-defining fact, can a detector preserve the distinction and route the case correctly?**

BRR-002 showed that the raw-language -> relation-vector -> deterministic-router interface is coherent on clean single-blocker cases, but direct response and relation-vector routing were both perfect. The fixture was therefore too easy to discriminate the value of explicit relation decomposition.

BRR-002B makes the detection boundary sharper by using near-twin pairs.

## Frozen design principle

Each pair should hold surface form, task type, and most facts approximately constant while changing one fact that changes the relation state.

Target contrasts:

```text
authority UNKNOWN       vs FAIL
evidence UNKNOWN        vs CONTRADICTED
capability UNKNOWN      vs ABSENT
competence UNKNOWN      vs INSUFFICIENT
resources TIGHT         vs INFEASIBLE
representation BLOCKED  vs competence INSUFFICIENT
search path UNKNOWN     vs ABSENT
viability UNCERTAIN     vs CLOSED
```

The detector should not infer a negative fact from missing information, and it should not soften an explicit blocker into uncertainty.

## Conditions

### A — DIRECT_RESPONSE

Given only the raw problem description, choose one response class from the fixed response vocabulary.

### B — RELATION_VECTOR

Given only the same raw problem description, first emit the explicit relation state vector, then identify the binding relation. A deterministic outer router maps the vector to the response class.

The comparison is exploratory because the same assistant supplies both conditions in the reference pass. It is not a claim of independent-model evidence.

## Relation vocabulary

```text
evidence:        PASS | UNKNOWN | CONTRADICTED
representation:  PASS | BLOCKED
competence:      SUFFICIENT | UNKNOWN | INSUFFICIENT
capability:      AVAILABLE | UNKNOWN | ABSENT
authority:       PASS | UNKNOWN | FAIL
resources:       SUFFICIENT | TIGHT | INFEASIBLE
viability:       OPEN | UNCERTAIN | CLOSED
search_path:     AVAILABLE | UNKNOWN | ABSENT
```

## Response vocabulary

```text
ACT
MEASURE_OR_RETRIEVE
REVISE
TRAVERSE
PROBE_COMPETENCE
ESCALATE_INTELLIGENCE
DISCOVER_OR_CALIBRATE
RECONFIGURE_OR_RECRUIT
ASK_OR_HOLD
REFUSE
SCHEDULE_OR_SIMPLIFY
REPORT_INFEASIBLE
PRESERVE_OR_REPORT_INFEASIBLE
SEARCH_OR_HOLD
ABSTAIN
```

## Router contract

For this experiment, every case is constructed so that exactly one relation is intended to be decision-relevant. Mixed blockers are deferred to BRR-003.

Mapping:

```text
evidence UNKNOWN          -> MEASURE_OR_RETRIEVE
evidence CONTRADICTED     -> REVISE
representation BLOCKED    -> TRAVERSE
competence UNKNOWN        -> PROBE_COMPETENCE
competence INSUFFICIENT   -> ESCALATE_INTELLIGENCE
capability UNKNOWN        -> DISCOVER_OR_CALIBRATE
capability ABSENT         -> RECONFIGURE_OR_RECRUIT
authority UNKNOWN         -> ASK_OR_HOLD
authority FAIL            -> REFUSE
resources TIGHT           -> SCHEDULE_OR_SIMPLIFY
resources INFEASIBLE      -> REPORT_INFEASIBLE
viability UNCERTAIN       -> MEASURE_OR_RETRIEVE
viability CLOSED          -> PRESERVE_OR_REPORT_INFEASIBLE
search_path UNKNOWN       -> SEARCH_OR_HOLD
search_path ABSENT        -> ABSTAIN
all non-blocking          -> ACT
```

The `viability UNCERTAIN` mapping is deliberately conservative in v0.01: obtain decision-relevant timing/trajectory evidence before treating the window as closed.

## Primary outcomes

Score separately:

1. active-relation state accuracy;
2. exact relation-vector accuracy;
3. binding-relation accuracy;
4. direct-response accuracy;
5. routed-response accuracy;
6. FAIL/UNKNOWN discrimination;
7. kernel recovery cases, where the vector supports the correct route despite a wrong direct response;
8. kernel degradation cases, where a wrong vector causes a wrong route;
9. false escalation;
10. false action;
11. false refusal;
12. pair consistency.

## Error classes

```text
UNKNOWN_AS_FAIL
FAIL_AS_UNKNOWN
UNKNOWN_AS_ABSENT
ABSENT_AS_UNKNOWN
UNKNOWN_AS_INSUFFICIENT
INSUFFICIENT_AS_UNKNOWN
TIGHT_AS_INFEASIBLE
INFEASIBLE_AS_TIGHT
REPRESENTATION_AS_COMPETENCE
COMPETENCE_AS_REPRESENTATION
UNKNOWN_SEARCH_AS_ABSENT
ABSENT_SEARCH_AS_UNKNOWN
UNCERTAIN_VIABILITY_AS_CLOSED
CLOSED_VIABILITY_AS_UNCERTAIN
```

## Research discipline

- Raw cases contain opaque IDs only.
- No expected relation or response labels belong in the generator-side packet.
- Freeze reference outputs before creating the evaluator key.
- Preserve first-pass errors.
- Do not rewrite a pair after seeing the score.
- A perfect same-assistant result should be interpreted as weak discriminating evidence, not as proof.
- Stronger evidence requires an independent host/model/session and eventually ecological mixed-blocker tasks.

## Falsifier of interest

The relation-vector architecture takes a hit if explicit decomposition does not improve error localization or route reliability on near-twin cases, or if it simply converts difficult cases into conservative `UNKNOWN` states.

## Working line

> **One small relational fact can change the correct remedy even when the surface problem barely changes.**
