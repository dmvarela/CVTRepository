# Binding Relation Router — Research Program

## Status

Exploratory Lucian OS research program.

This program begins from a convergence across existing Lucian OS branches rather than from a claim that a general controller has already been solved.

Relevant upstream work includes:

- `docs/PROBLEM_SOLVING_ARCHITECTURE_v0.01.md`
- `docs/LUCIAN_OS_ARCHITECTURE_v0.03_CAPABILITY_COMPOSITION.md`
- `docs/INTENT_NATIVE_COMPUTING_AND_INTELLIGENCE_ALLOCATION_v0.01.md`
- `docs/MORPHOLOGY_ALLOCATION_AND_SCHEDULING_v0.01.md`
- `experiments/CP_002_READ_ONLY_HOST_PROBE.md`
- `experiments/RELATIONAL_SEARCH_004.md`
- `research/structural-traversal/`

## Program question

> **Given an intended outcome that is not currently reachable, can Lucian OS diagnose which relation is actually binding and route to the appropriate next operation without treating every failure as a need for more general reasoning?**

The first-order distinction is:

```text
missing != unknown != blocked != contradicted != insufficient != infeasible
```

These states can demand different responses.

Examples:

```text
evidence UNKNOWN        -> MEASURE / RETRIEVE / TEST
representation BLOCKED -> TRAVERSE
authority UNKNOWN      -> ASK / HOLD
authority FAIL         -> REFUSE
capability ABSENT      -> RECONFIGURE / RECRUIT
competence INSUFFICIENT-> ESCALATE INTELLIGENCE
resources TIGHT        -> SCHEDULE / SIMPLIFY
viability CLOSED       -> PRESERVE / REPORT INFEASIBILITY
no useful search path  -> ABSTAIN
no binding limitation  -> ACT
```

## Candidate architecture

```text
HUMAN INTENT
    -> FRAME
    -> ABSTRACT REQUIREMENTS
    -> CURRENT OPERATIONAL STATE
    -> DETECT RELEVANT RELATION STATES
    -> IDENTIFY BINDING RELATION
    -> ROUTE APPROPRIATE RESPONSE
    -> VERIFY
    -> RETURN
    -> UPDATE
```

The router is not intended to replace the existing Lucian subsystems. It selects among them.

Candidate responders include:

```text
structural traversal
measurement / retrieval / probing
intelligence escalation
affordance discovery / morphology composition
authority request / refusal
resource scheduling
preservation / rerouting
abstention
action
```

## Non-compensatory boundary

The program inherits the Lucian OS project constitution.

In particular:

```text
more competence cannot manufacture authority
more reasoning cannot manufacture evidence
more tokens cannot manufacture a missing actuator
more urgency cannot manufacture viability
an attractive representation cannot override contradictory target constraints
```

The router should therefore diagnose relation state before optimizing response cost.

## Relation to Structural Traversal

Structural Traversal remains a separate research program.

`TRAVERSE` is one possible response when representation is the binding limitation. It is not the general controller.

## Relation to Relational Search

`RELATIONAL_SEARCH_004` supplies an important pattern:

```text
relation detection
!=
standing aggregation
```

and:

```text
FAIL != UNKNOWN
```

The Binding Relation Router generalizes the routing question across problem-solving dimensions, but this generalization is only a research hypothesis until tested.

## Promotion criteria

No part of this program should be promoted into the Lucian OS core merely because a synthetic fixture passes.

Promotion requires evidence that the routing abstraction:

1. distinguishes materially different blocker classes;
2. chooses different appropriate responders rather than defaulting to generic reasoning;
3. preserves `UNKNOWN`, explicit `FAIL`, and `INFEASIBLE` distinctly;
4. respects authority, truth, privacy, safety, and viability as hard constraints;
5. survives held-out tasks and mixed-blocker cases;
6. remains useful when relation detection is noisy rather than pre-labeled;
7. can consume operational evidence from real embodiment/proprioception layers;
8. preserves provenance and Return after correction.

## Current experimental state

```text
BRR-001 — Binding relation discrimination
  status: PASS — fixture / outer-routing plumbing only
  supplied relation states
  -> 12/12 binding and response routing
  -> generic reason-harder baseline 1/12

BRR-002 — Raw relation detection
  status: PASS — internal/procedural fixture only; weak discrimination
  raw natural-language cases
  -> 14/14 exact relation vectors
  -> 14/14 binding relation
  -> 14/14 direct response
  -> 14/14 deterministic routed response
  -> 0 kernel recoveries
```

BRR-002 therefore validates the interface on clean single-blocker cases but does not yet demonstrate that explicit relation-vector decomposition improves final decisions over direct reasoning. Preserve the perfect score as evidence that the fixture was too legible rather than silently making the same test harder after seeing the result.

## Current experiment sequence

```text
BRR-001 — Binding relation discrimination
  same superficial failure
  -> different binding relation
  -> different required response

BRR-002 — Raw relation detection
  raw held-out description
  -> inferred relation vector
  -> deterministic non-compensatory outer routing

BRR-002B — Adversarial relation detection
  near-identical surface cases
  -> UNKNOWN vs FAIL / ABSENT vs UNKNOWN / TIGHT vs INFEASIBLE
  -> test whether explicit relation decomposition earns its keep

BRR-003 — Mixed blockers and value of information
  several active limitations
  -> choose which one to resolve first

BRR-004 — Cross-subsystem integration
  route into actual Lucian OS prototype responders
  -> verify outcome / Return
```

## Research discipline

- Synthetic routing fixtures validate plumbing and distinctions, not general intelligence.
- Do not tune rules solely to make a held-out fixture pass after seeing its labels.
- Preserve first-run failures and unexpectedly easy passes.
- Separate relation detection from downstream routing where possible.
- Prefer auditable deterministic outer rules for non-compensatory constraints.
- Keep simulation-only or read-only boundaries until authority and verification are independently adequate.

## Working formulation

> **Do not ask first how much more intelligence the task needs. Ask which relation is preventing the intended outcome from becoming reachable.**

Then address that relation and return to reality.