# BRR-001 — Binding Relation Discrimination

## Status

PASS — fixture / outer-routing plumbing only.

Simulation only. Relation states are supplied explicitly. This experiment does **not** test whether a model can infer the correct relation state from open-ended natural language.

## Question

> **When the same superficial symptom is present — “the intended task is not currently completing” — can an outer Lucian OS controller route different binding relations to different appropriate responders rather than defaulting to more general reasoning?**

## Upstream convergence

BRR-001 integrates distinctions already present across several Lucian OS branches:

```text
PROBLEM_SOLVING_ARCHITECTURE
  meta-level choice of how to solve the current problem

RELATIONAL_SEARCH_004
  relation detection != standing aggregation
  FAIL != UNKNOWN

STRUCTURAL_TRAVERSAL
  representation scarcity -> TRAVERSE

INTELLIGENCE_ALLOCATION
  competence shortfall -> escalate intelligence

CAPABILITY_COMPOSITION / ECM
  missing capability -> discover, compose, or recruit

COMPUTATIONAL_PROPRIOCEPTION
  unknown capability -> inspect / calibrate the actual host

MORPHOLOGY SCHEDULING
  resource pressure -> schedule / simplify

AUTHORITY MEMBRANE
  unknown authority -> ask / hold
  failed authority -> refuse

VIABILITY / RETURN
  closed trajectory -> preserve / report infeasibility
```

The integration hypothesis is narrower than a general theory of control:

> A single failure symptom can arise from materially different binding relations, and the next operation should depend on the relation state rather than on failure alone.

## Design

Twelve cases share the same top-level symptom but vary one active relation while keeping the others in a non-blocking state.

Dimensions exercised:

```text
evidence
representation
competence
capability
authority
resources
viability
search path
none / action-ready
```

Important state distinctions include:

```text
EVIDENCE_UNKNOWN != EVIDENCE_CONTRADICTED
AUTHORITY_UNKNOWN != AUTHORITY_FAIL
CAPABILITY_UNKNOWN != CAPABILITY_ABSENT
```

### Policy A — GENERIC_REASON_HARDER

Every non-completion symptom routes to:

```text
ESCALATE_INTELLIGENCE
```

This is intentionally naive and represents the failure mode in which additional general reasoning is treated as the default remedy for every blockage.

### Policy B — BINDING_RELATION_v0.01

The supplied relation vector is inspected and routed non-compensatorily.

Examples:

```text
EVIDENCE_UNKNOWN        -> MEASURE_OR_RETRIEVE
REPRESENTATION_BLOCKED  -> TRAVERSE
COMPETENCE_INSUFFICIENT -> ESCALATE_INTELLIGENCE
CAPABILITY_ABSENT       -> RECONFIGURE_OR_RECRUIT
AUTHORITY_UNKNOWN       -> ASK_OR_HOLD
AUTHORITY_FAIL          -> REFUSE
RESOURCES_TIGHT         -> SCHEDULE_OR_SIMPLIFY
VIABILITY_CLOSED        -> PRESERVE_OR_REPORT_INFEASIBLE
SEARCH_PATH_ABSENT      -> ABSTAIN
NONE                    -> ACT
EVIDENCE_CONTRADICTED   -> REVISE
CAPABILITY_UNKNOWN      -> DISCOVER_OR_CALIBRATE
```

## Procedural order

1. Research-program boundary created.
2. Generator-side packets committed without evaluator labels.
3. Deterministic router prototype added.
4. A project-root path bug was discovered before freezing output and corrected.
5. Corrected router executed successfully.
6. Router output frozen at commit `dbf0867c9204e23b53d085bdaa098d8d6fea3408`.
7. Evaluator key created only after frozen output existed.
8. Post-freeze evaluator added and applied.

The path correction is plumbing repair, not a result repair; no scored router output existed before the correction.

## Results

```text
cases                              12
binding relation accuracy          12 / 12 = 1.000
binding response accuracy          12 / 12 = 1.000
generic reason-harder accuracy      1 / 12 = 0.0833
distinct binding responses         12
```

The generic baseline succeeds only on `B03_COMPETENCE_INSUFFICIENT`, where stronger reasoning competence is in fact the appropriate response.

All explicit boundary checks pass:

```text
authority UNKNOWN -> ASK_OR_HOLD
authority FAIL -> REFUSE
evidence UNKNOWN -> MEASURE_OR_RETRIEVE
evidence CONTRADICTED -> REVISE
representation BLOCKED -> TRAVERSE
competence INSUFFICIENT -> ESCALATE_INTELLIGENCE
capability ABSENT -> RECONFIGURE_OR_RECRUIT
no binding limit -> ACT
```

## Interpretation

The result supports only a small architectural claim:

> **Given already-correct relation states, a deterministic outer router can preserve distinctions among materially different blockers and select different responder classes.**

It also demonstrates the intended failure of the generic baseline in the fixture:

> **Non-completion does not imply insufficient intelligence.**

The stronger candidate principle is:

> **Do not allocate a remedy before identifying the relation that is binding.**

## What BRR-001 does not show

It does **not** establish that:

- an LLM can infer the correct binding relation from arbitrary user requests;
- the relation vocabulary is complete;
- the precedence ordering is correct for mixed blockers;
- these response labels are globally optimal;
- routing improves real task completion;
- Lucian OS has a general problem-state controller;
- synthetic fixture accuracy predicts robotics or operating-system performance.

The fixture is deliberately easy at the detection layer because relation states are supplied explicitly. A 12/12 score is therefore primarily a plumbing/invariant result.

## Most important next test

BRR-002 should remove the supplied answer at the relation-detection layer.

Candidate structure:

```text
raw held-out problem packet
        ↓
RELATION DETECTOR
  emits explicit state vector
        ↓
DETERMINISTIC OUTER ROUTER
        ↓
response class
```

The critical comparison is not merely final route accuracy. Score separately:

```text
relation-state accuracy
FAIL vs UNKNOWN discrimination
binding-relation accuracy
final route accuracy
kernel recovery of host aggregation errors
false escalation rate
false action / false refusal rate
```

This keeps the architecture falsifiable: if relation detection is unreliable, deterministic routing cannot rescue bad inputs.

## Working result

> **The symptom “I cannot complete the task” is not itself a diagnosis. The next intelligent move depends on what relation is preventing reachability.**
