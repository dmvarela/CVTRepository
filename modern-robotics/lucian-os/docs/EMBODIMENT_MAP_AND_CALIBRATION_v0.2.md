# Lucian OS — Embodiment Map & Calibration v0.2

## Status

Frozen design hypothesis for the next Lucian OS development phase, 2026-09-03.

This note is intentionally more specific than the v0.1 capability manifest. It introduces the hypothesis that an embodiment should not be represented only as a list of capabilities. Lucian OS should maintain a provisional map of reachable state transitions and refine that map through bounded interaction with the embodiment.

The hypothesis is inspired by prior Lucian OS work plus independent literature on sensorimotor contingency learning, infant body-map development, developmental robotics, and visual robot self-modeling. Those literatures motivate the experiment; they do not prove this architecture.

## Core hypothesis

> A portable intelligence layer should begin with a minimal declared embodiment scaffold, then calibrate an empirical embodiment map by comparing bounded actions with observed consequences.

The device/driver provides a prior, not the final truth.

Formally:

`G_declared -> safe action -> observed consequence -> G_experienced -> G_operational`

where:

- `G_declared` is the manufacturer/adapter description of possible states and transitions;
- `G_experienced` records empirically observed action-consequence relations;
- `G_operational` is the currently trusted map used for planning.

## Why a map rather than a flat library

A capability library answers:

`What moves exist?`

A map answers:

`From the current state, what states are reachable, by which transitions, under what constraints?`

Represent the embodiment as a transition graph or other reachability structure:

`G_E = (S, E)`

where `S` denotes relevant states and `E` denotes candidate transitions.

Each transition should carry at least:

- action/command;
- preconditions;
- predicted state change;
- observed state change history;
- confidence/validation state;
- risk;
- cost/energy;
- reversibility;
- verification method;
- authority requirements;
- competence required to execute it.

The graph representation is a hypothesis. Continuous-control embodiments may require richer representations later.

## Calibration loop

Lucian OS should not perform unconstrained exploration.

Calibration is permitted only inside an explicit safe envelope.

Minimal loop:

1. identify embodiment;
2. load declared primitives and constraints;
3. establish a calibration authority envelope;
4. choose a permitted low-risk primitive action;
5. predict the expected sensory consequence;
6. execute or simulate the action;
7. observe the consequence;
8. compare prediction and observation;
9. update confidence in the transition;
10. preserve provenance;
11. repeat until the minimal operational map is sufficiently calibrated.

Compactly:

`action -> observation -> contingency estimate -> map update`

## Truth must bite

The declared map is not reality.

If the adapter says:

`command a -> state delta x`

but repeated observation shows:

`command a -> state delta y`

then T requires the operational map to change.

A warning in a log is insufficient.

The new evidence must have behavioral consequences:

- downgrade or remove the disputed transition;
- lower confidence;
- block plans that depend on the unsupported edge;
- request recalibration or escalation;
- preserve the discrepancy and provenance.

Thus:

> Truth has to bite by changing reachability.

## FTLτA over the map

FTLτA is not treated as decoration layered on top of planning. The current candidate interpretation is that it constrains path admissibility.

### F — Freedom / authority

Physical possibility does not create permission.

`possible edge != authorized edge`

Authority can remove transitions from the currently admissible map.

If an action is unauthorized, the disposition is `BLOCK`, not `ESCALATE`.

A stronger reasoner may expand competence; it may not expand authority merely by being stronger.

### T — Truth / warrant

The map must remain corrigible by observation, evidence, provenance, and verification.

`predicted edge != warranted edge`

A transition can move through states such as:

`declared -> candidate -> observed -> tested -> validated -> contested -> retracted`

### L — preservation / repair

When multiple admissible paths exist, Lucian OS should prefer paths that preserve viable relations, recoverability, and constituents where task constraints allow.

L must not override F or T.

### A — agency / authentic evaluation

Planning should reflect the actual current map and task envelope rather than merely mirroring an expected answer or replaying a stored route when current evidence contradicts it.

### τ — change through time

The map is dynamic:

`G_t -> G_(t+1)`

through action, learning, correction, authority changes, device changes, skill acquisition, unresolved questions, and return.

τ preserves history and enables re-entry without silently rewriting prior state.

## Skills as compressed topology

A skill is provisionally defined as:

> a validated reusable trajectory, controller, or policy that reliably traverses a region of embodiment possibility space under specified conditions.

A skill is not automatically a fixed discrete path; continuous-control systems may compress a region or policy rather than a literal sequence of edges.

Each validated skill should record:

- applicable state region;
- required primitives;
- authority requirements;
- validation conditions;
- known limits;
- failure conditions;
- verification method;
- source/provenance;
- version.

## Escalation as a gap in local navigability

Escalation is justified when:

- the destination is authorized;
- the embodiment appears physically capable;
- but no sufficiently competent local path/policy is available.

Then Lucian OS should escalate the missing reasoning, not raw motor ownership.

A bounded escalation packet should describe:

- current state;
- desired state;
- trusted local map;
- candidate/contested edges;
- attempted paths;
- remaining uncertainty;
- authority envelope;
- prohibited transitions;
- verification criteria.

The upstream reasoner returns a candidate route or policy.

That candidate remains provisional until locally checked and, where appropriate, empirically validated.

## Downward compilation

A successful upstream solution may become local competence only after validation.

Candidate lifecycle:

`novel problem -> upstream proposal -> bounded test -> repeated validation -> reusable local skill`

One success is not enough to create a permanent local policy.

## MouseSim 001

The first embodiment experiment will be a simulation-only robot mouse.

The mouse should not begin with a complete world/body map.

It receives only a minimal scaffold:

- a small set of permitted primitive action channels;
- sensory observations;
- safe operating bounds;
- no hidden access to the simulator's transition rules.

The experiment asks whether Lucian OS can infer stable sensorimotor contingencies and build a usable empirical map.

### Initial test sequence

1. **Primitive calibration** — determine which bounded actions reliably cause which state changes.
2. **Unexpected transition** — simulator behavior differs from the declared prior; T should update operational reachability.
3. **Unauthorized transition** — a physically possible move is outside authority; F should `BLOCK` rather than escalate.
4. **Competence gap** — destination is authorized and reachable but local planner cannot find a route; escalate the missing reasoning.
5. **Candidate skill** — an upstream-proposed route succeeds; retain as provisional.
6. **Skill validation** — repeat under defined conditions; only then promote to validated local competence.
7. **Continuity test** — restart the host and verify that learned map state, provenance, uncertainty, and unresolved edges survive without fabricated history.

## What would count against the hypothesis

The map formulation should be weakened or rejected if:

- meaningful embodiment competence cannot be represented without excessive special cases;
- continuous-control tasks make the map abstraction misleading rather than useful;
- calibration adds complexity without improving safety or portability;
- declared capabilities alone perform as well as empirical calibration under perturbation;
- F/T/L/A constraints do not produce distinct behavioral consequences;
- τ/history preservation does not improve recovery after host/device discontinuity.

Negative results must be preserved.

## Immediate implementation order

1. fix v0.1 router so `BLOCK`, `ESCALATE`, and `LOCAL` are distinct outcomes;
2. build `MouseSim 001` with hidden transition rules and observable consequences;
3. implement a minimal empirical transition table independent of Qwen;
4. let Qwen propose interpretations/plans but not directly mutate trusted map state;
5. add tests where declared and observed body behavior conflict;
6. only after the deterministic calibration loop works, test selective Qwen escalation.

## Guardrails

- No real physical actuation in v0.2.
- No autonomous deployment.
- No self-expansion of authority.
- No silent promotion of inferred transitions to validated skills.
- No claim that infant learning and robot learning are mechanistically identical.
- No claim that the map abstraction is universal until it survives substantially different embodiments.
