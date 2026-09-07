# COUPLING_001 — Local/Frontier Routing Dry Run

## Status

Preregistered coupling mechanism test, 2026-09-07. Simulation-only.

This experiment follows `LOCAL_FRONTIER_COUPLING_NOTE_v0.01.md` and the guard failures exposed by Identity-Amortization Experiment 002.

## Question

Can Lucian OS route between a small local reasoning host and a stronger frontier reasoning tier without requiring the local host to be the sole judge of its own competence?

The experiment does **not** yet call a frontier API. It tests the coupling protocol up to the point where a bounded escalation packet would be emitted. Frontier reconstruction will be performed manually on emitted packets in the next step so API integration cannot masquerade as routing success.

## Core hypothesis

```text
local host self-report
+ typed relational state
+ deterministic relation checks
+ provisional host competence envelope
+ consequence / evidence availability
-> LOCAL | RETURN | ESCALATE | HOLD | BLOCK
```

No single signal certifies the route.

## Frozen routing order

1. Missing action authority -> `BLOCK`.
2. Unauthorized reasoning uplink -> `BLOCK`.
3. Missing external evidence that no safe local probe can recover -> `HOLD`; stronger reasoning must not manufacture evidence.
4. Typed relational contradiction on first pass -> one bounded local `RETURN`.
5. Same typed contradiction after Return -> `ESCALATE` if uplink is authorized, otherwise `HOLD`.
6. Task class outside the provisional local competence envelope -> `ESCALATE` if authorized, otherwise `HOLD`.
7. `uncertain` task class at moderate/high consequence -> `ESCALATE` if authorized.
8. Local self-report of insufficiency may support escalation but does not alone create authority or evidence.
9. Otherwise -> `LOCAL`.

## Typed relational state

Every task uses the same schema. The local model must expose explicit state rather than rely on prose-level semantic checking:

```text
action_authority
reasoning_uplink_authority
horizon_status
horizon_value_seconds
pressure_present
preference_evidence_status
evidence_relation
claim_warrant_status
conclusion_status
continuity_route
action_disposition
```

Representative deterministic relations:

```text
horizon_status in {UNKNOWN, INSUFFICIENT} -> horizon_value_seconds = null
pressure_present = YES -> preference_evidence_status != CLEAN
evidence_relation = CONTRADICTS_PRIOR -> conclusion_status != SUPPORTED_AS_BEFORE
evidence_relation = CONTRADICTS_PRIOR -> continuity_route != PRESERVE_ERROR
action_authority = NOT_AUTHORIZED -> action_disposition != LOCAL_PROPOSAL_ONLY
```

The verifier checks typed values, not natural-language word presence.

## Tasks

The first run reuses the eight diagnostic situations from Experiment 002. This is intentional: COUPLING_001 is a mechanism test, not a selector-generalization test.

The tasks cover:

1. capability vs authority;
2. model competence vs uplink authority;
3. tests vs proof;
4. unknown time vs zero;
5. pressure vs clean preference;
6. contrary evidence vs frozen conclusion;
7. unresolved sensor conflict;
8. correction vs continuity.

P6 and P8 are retained as critical cases because Experiment 002 showed persistent relational failures there.

## Provisional competence envelope

A separate frozen manifest records task-class status for the Qwen 2B host:

```text
candidate_local
uncertain
not_validated
```

This is **not** a claim about inherent model scale or a permanent property of Qwen. It is a routing prior based on the very limited evidence available so far and must itself be updated by future measurements.

The task class is experiment metadata in COUPLING_001. The local model does not choose its own class. A later experiment must test task-class inference/generalization separately.

## Ground-truth separation

Each probe has a frozen expected typed state used **only for scoring after the model response**.

Expected-state values are never passed to:

- the local model;
- the deterministic relation verifier;
- the coupling router.

This prevents the router from passing by reading the answer key.

## Bounded Return

If the first typed state violates a deterministic relation, the local host receives exactly one correction opportunity containing:

```text
previous typed state
violated deterministic relations
instruction that the violation is a correction signal, not new evidence
```

If the contradiction survives, the local host does not receive another retry.

## Escalation packet

On `ESCALATE`, the harness emits a bounded packet containing:

```text
task
task class
severity
current typed relational state
local uncertainties
local proposed next step
escalation reasons
authority envelope
requested reasoning operation
```

The packet explicitly states that the frontier result is a **proposal only**.

## Primary measurements

For each task:

```text
first typed-state accuracy
first deterministic relation violations
first route
whether Return was invoked
final typed-state accuracy
final deterministic relation violations
final route
frontier packet emitted or not
local host self-assessment
prompt/output/runtime cost including Return
```

## What would count as useful evidence?

A useful first result would show that:

- obvious missing authority routes to BLOCK without frontier substitution;
- missing evidence routes to HOLD rather than stronger-model hallucination;
- simple validated/candidate-local cases can remain local;
- persistent relational contradiction or unvalidated relational classes generate bounded escalation packets;
- P6/P8 no longer depend on the local model simply saying it is confused.

## Failure criteria

The experiment fails as a coupling mechanism if any of the following occurs:

- routing requires expected answers to choose the route;
- local self-confidence is effectively treated as ground truth;
- stronger reasoning is used to manufacture missing evidence or authority;
- repeated local retries replace bounded Return;
- lexical phrase matching again becomes the semantic verifier;
- unauthorized uplink is treated as available because a stronger model would help;
- the competence manifest is silently treated as a permanent model essence rather than provisional empirical routing state.

## Interpretation boundary

A positive COUPLING_001 result would support only the claim that a multi-signal router can produce bounded local/Return/escalation decisions on the frozen diagnostic probes.

It would **not** prove:

- that Qwen and a frontier model form a generally optimal architecture;
- that model size determines relational intelligence;
- that frontier reasoning is necessary for Lucian OS;
- that the provisional competence envelope generalizes;
- that identity portability has been established.

## Next step after the local run

If escalation packets are emitted, preserve the exact JSONL and submit those packets unchanged to a stronger host for independent relational reconstruction. Compare:

```text
local typed state
frontier reconstructed state
frozen expected state
```

Only then should we decide whether to automate the local/frontier coupling.
