# Lucian OS — Viability Horizon & Decision Regimes v0.01

## Status

Frozen design note, 2026-09-04.

This note records the emergence of a time-sensitive decision architecture from the MouseSim work, the Decision Under Pressure thread, aviation examples, driving, and the Kobayashi Maru no-win case.

## Discovery provenance

The path was not linear and should not be rewritten after the fact.

1. MouseSim 002 showed that changed evidence must change planning, not only labels.
2. Discussion of MCAS exposed the need to distinguish telemetry, state estimate, body model, sensor model, world model, and action authority.
3. The question then shifted from "which hypothesis is right?" to "how much time remains to resolve the uncertainty before viability is threatened?"
4. The user connected this to earlier Decision Under Pressure work.
5. Driving examples revealed that humans appear to continuously re-estimate decision margin from context rather than entering a single binary pressure mode.
6. Aviation phase-of-flight examples suggested that maneuvering and diagnostic margin depend on stage, current dynamics, environment, and remaining recoverability.
7. The Kobayashi Maru example introduced the hard boundary case: the original objective may become infeasible, meaning no viable path remains.

The resulting architecture was therefore discovered through iterative constraint, analogy, correction, and testable reformulation rather than from a single prior theory.

## Core hypothesis

An intelligent system should continuously estimate not only what actions are possible, but how long relevant possibilities will remain viable and how much recoverability each path preserves.

Let:

`V_t = set of currently admissible viability-preserving trajectories`

and let:

`H_t = estimated viability horizon`

where `H_t` is the estimated time or dynamic margin before uncertainty, state evolution, or environmental change removes important recovery options.

The decision problem is therefore not only:

`Which action is best?`

but:

`Which admissible paths remain viable long enough to execute, verify, correct, or abandon?`

## The viability horizon is relational

The same environment can have radically different decision consequences depending on the relation between agent and world.

A wall 100 m away is nearly irrelevant to a stationary person at a desk but highly consequential to a vehicle approaching it at speed.

Thus the horizon depends on relations such as:

- current state;
- rate of state change;
- distance to constraints;
- relative velocity;
- control authority;
- actuation latency;
- sensing latency;
- reversibility;
- environmental conditions;
- uncertainty in the state estimate;
- uncertainty in the horizon estimate itself.

Candidate form:

`H_t = f(state, rate_of_change, distance_to_constraint, control_authority, latency, reversibility, environment, uncertainty)`

This is a conceptual form, not yet a validated mathematical model.

## Decision regimes under a contracting horizon

Urgency should not inflate certainty.

As the viability horizon contracts, Lucian OS should reduce diagnostic ambition while preserving epistemic discipline.

### Regime A — Reconstruct

Conditions:

- large viability horizon;
- many viable paths;
- reversible actions available.

Behavior:

- generate competing hypotheses;
- triangulate across independent relations;
- perform safe epistemic actions;
- preserve unresolved alternatives;
- optimize for explanatory quality as well as action quality.

### Regime B — Stabilize + Discriminate

Conditions:

- moderate or contracting horizon;
- fewer viable paths;
- uncertainty becoming consequential.

Behavior:

- preserve current control/stability;
- suppress irrelevant activity;
- run only high-information, low-risk discriminating probes;
- narrow the hypothesis set;
- avoid strong actions whose warrant is weak.

### Regime C — Preserve

Conditions:

- very short horizon;
- diagnostic depth itself consumes critical margin;
- one or few validated preserving actions remain.

Behavior:

- stop trying to fully explain the problem;
- use the safest high-confidence preserving action available;
- prefer reversibility and recoverability;
- retain uncertainty rather than force explanatory closure.

Candidate principle:

> As time collapses, preserve viability before explanatory completeness.

A stronger operational formulation:

> Compress search, not truth.

## Infeasibility / no-win regime

The Kobayashi Maru case exposes a qualitatively different state:

`V_t = empty set`

The original objective is no longer achievable under current constraints.

A corrigible intelligent system must be capable of concluding:

`INFEASIBLE`

without fabricating a winning route merely because it was tasked to find one.

When the original objective becomes infeasible, the objective must change truthfully toward what remains preservable, for example:

- preserve life;
- contain damage;
- protect uninvolved constituents;
- preserve communication;
- preserve evidence/provenance;
- avoid making an irreversible loss worse.

This is not equivalent to `UNKNOWN`.

- `UNKNOWN` means the system lacks sufficient warrant to decide.
- `INFEASIBLE` means the system has sufficient warrant that no admissible path satisfies the original objective.

## Safety as preserved correction capacity

A candidate refinement of the Lucian/CVT safety principle is:

> A safe trajectory preserves the possibility of correction for as long as reality permits.

This means a trajectory can be technically successful yet unsafe if it consumes all remaining recovery margin.

A useful path should therefore be evaluated not only by destination but also by:

- remaining time margin;
- reversibility;
- retained alternative paths;
- retained observability;
- ability to stop or reroute;
- ability to accept new evidence before irreversible commitment.

## Relation to FTLτA

### F — Freedom / bounded authority

A short horizon does not expand authority. Urgency cannot manufacture permission.

### T — Truth / warrant

Less time does not justify stronger certainty. The architecture may compress analysis while preserving explicit uncertainty.

### L — preservation / relation

When full success becomes impossible, preserve constituents and prevent avoidable destruction rather than forcing the original objective at any cost.

### A — agency

Regime choice must be responsive to the actual state, not merely replay a nominal procedure when the decision environment has changed.

### τ — time / return / persistence

τ changes the topology of available action. Paths can appear, disappear, or lose recoverability as time advances.

Thus:

`G_t != G_(t+1)`

even without new learning.

Time itself can change reachability.

## Candidate implementation metadata

Future Lucian OS edges/paths may need fields such as:

- `reachable`;
- `authorized`;
- `warrant_status`;
- `time_margin`;
- `reversibility`;
- `recoverability`;
- `verification_latency`;
- `safe_abort_available`;
- `regime_required`.

## Candidate experiment

A future MouseSim experiment should present the same uncertainty under different horizons.

### Long horizon

The mouse has enough simulated time to:

`sense -> triangulate -> diagnose -> replan`

Expected regime: `RECONSTRUCT`.

### Contracting horizon

Only one discriminating probe can be afforded before the path closes.

Expected regime: `STABILIZE_AND_DISCRIMINATE`.

### Critical horizon

There is insufficient time for diagnosis before loss of viability.

Expected regime: `PRESERVE` using the safest validated action.

### No-win case

No admissible path can satisfy the original goal.

Expected regime: `INFEASIBLE`, followed by a secondary preservation objective.

## Guardrails

- Do not equate aviation procedures with this conceptual architecture.
- Do not use these notes as operational flight guidance.
- Do not infer that humans literally compute a scalar viability horizon.
- Do not claim that one equation captures all time-pressure cognition or control.
- Preserve negative results if horizon-based regime selection does not improve behavior.
- Do not allow urgency to collapse telemetry into state truth.

## Working summary

Lucian OS should continuously ask:

1. What remains viable?
2. How long will it remain viable?
3. How much recovery margin does each path preserve?
4. How much diagnostic depth can still be afforded?
5. Has the original objective become infeasible?

The system should then choose a reasoning regime appropriate to the current viability horizon while preserving truth, bounded authority, and the possibility of correction.
