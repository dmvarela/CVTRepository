# Lucian OS — Viability Horizon & Decision Regimes v0.01

## Status

Frozen design note, 2026-09-04.

This note records the emergence of a time-sensitive decision architecture from the MouseSim work, the Decision Under Pressure thread, aviation examples, driving, the Kobayashi Maru no-win case, and the later HOLD/Sabbath discussion.

## Discovery provenance

The path was not linear and should not be rewritten after the fact.

1. MouseSim 002 showed that changed evidence must change planning, not only labels.
2. Discussion of MCAS exposed the need to distinguish telemetry, state estimate, body model, sensor model, world model, and action authority.
3. The question then shifted from "which hypothesis is right?" to "how much time remains to resolve the uncertainty before viability is threatened?"
4. The user connected this to earlier Decision Under Pressure work.
5. Driving examples revealed that humans appear to continuously re-estimate decision margin from context rather than entering a single binary pressure mode.
6. Aviation phase-of-flight examples suggested that maneuvering and diagnostic margin depend on stage, current dynamics, environment, and remaining recoverability.
7. The Kobayashi Maru example introduced the hard boundary case: the original objective may become infeasible, meaning no viable path remains.
8. A theology/Sabbath discussion introduced the possibility that unresolved questions can remain unresolved without forcing closure when the current state is viable.
9. A battlefield/archer example sharpened this into `HOLD`: observation continues while intervention is deliberately withheld until action becomes sufficiently warranted/effective.
10. The user then identified the failure mode: HOLD itself can be wrong if the system overestimates how much margin remains.

The resulting architecture was therefore discovered through iterative constraint, analogy, correction, and testable reformulation rather than from a single prior theory.

The theological and fictional examples are discovery aids, not technical evidence. Their role here is provenance: they helped expose structural questions later stated in testable engineering terms.

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

## Horizon uncertainty and margin-to-commitment

The system can be wrong not only about the world state but about how much time/maneuvering margin remains.

Therefore Lucian OS should not treat `H_t` as exact. Conceptually:

`H_t ~= H_hat_t +/- epsilon_H`

where `epsilon_H` represents uncertainty in the horizon estimate.

A useful secondary quantity is a conceptual margin-to-commitment:

`M_t = available_margin - (detect_latency + decide_latency + actuation_latency + verification_latency)`

This is not yet a validated equation. It records a structural requirement: waiting is safe only while enough margin remains to notice a change, choose an action, execute it, and still recover if the action is wrong.

Two distinct errors follow:

- acting too early can waste resources, expose the system, or consume future options;
- acting too late can allow the last viable path to disappear.

Candidate principle:

> Do not wait for certainty that the horizon has closed; by then the last corrective option may already be gone.

High uncertainty about remaining margin should make the architecture more conservative when the consequence of overestimating margin is severe.

## Decision regimes under a changing horizon

Urgency should not inflate certainty.

As the viability horizon contracts, Lucian OS should reduce diagnostic ambition while preserving epistemic discipline.

### Regime 0 — HOLD / Observe

Conditions:

- current state remains viable;
- intervention is not yet warranted or is poorly timed;
- waiting preserves or increases future option value;
- observation can continue;
- enough margin remains to detect threshold crossing and still act.

Behavior:

- continue sensing and state estimation;
- preserve readiness;
- avoid unnecessary commitment;
- update the viability horizon and its uncertainty;
- monitor whether the action threshold has been crossed;
- remain capable of leaving HOLD immediately when waiting ceases to preserve viability.

HOLD is not passivity and not `STOP THINKING`.

It is deliberate non-intervention under continuous observation.

Candidate principle:

> Do not confuse urgency with readiness.

A stronger testable heuristic for future work is:

`HOLD remains attractive while expected information/position gain from waiting exceeds expected loss of maneuvering/recovery margin.`

This should not be treated as a literal scalar inequality until operationalized and tested.

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
- uncertainty in that margin;
- reversibility;
- retained alternative paths;
- retained observability;
- ability to stop or reroute;
- ability to accept new evidence before irreversible commitment.

This also gives HOLD an explicit safety interpretation:

> Waiting is viable only while waiting preserves correction capacity better than premature commitment would.

## Relation to FTLτA

### F — Freedom / bounded authority

A short horizon does not expand authority. Urgency cannot manufacture permission.

### T — Truth / warrant

Less time does not justify stronger certainty. The architecture may compress analysis while preserving explicit uncertainty.

Horizon estimates themselves are corrigible claims and must not be treated as certain merely because action is urgent.

### L — preservation / relation

When full success becomes impossible, preserve constituents and prevent avoidable destruction rather than forcing the original objective at any cost.

HOLD can serve L when non-intervention preserves future options and relation better than premature action.

### A — agency

Regime choice must be responsive to the actual state, not merely replay a nominal procedure when the decision environment has changed.

Choosing HOLD must be an active state assessment, not default inertia.

### τ — time / return / persistence

τ changes the topology of available action. Paths can appear, disappear, or lose recoverability as time advances.

Thus:

`G_t != G_(t+1)`

even without new learning.

Time itself can change reachability.

HOLD therefore requires continuing temporal evaluation: the system must know when the conditions that justified waiting no longer obtain.

## Candidate implementation metadata

Future Lucian OS edges/paths may need fields such as:

- `reachable`;
- `authorized`;
- `warrant_status`;
- `time_margin`;
- `time_margin_uncertainty`;
- `reversibility`;
- `recoverability`;
- `verification_latency`;
- `decision_latency`;
- `actuation_latency`;
- `safe_abort_available`;
- `expected_value_of_waiting`;
- `expected_margin_loss_while_waiting`;
- `regime_required`.

## Candidate experiment

A future MouseSim experiment should present the same uncertainty under different horizons and test HOLD explicitly.

### HOLD case

The target is not yet in the effective/actionable region. Waiting should improve action quality while preserving enough margin to act later.

Expected regime: `HOLD`, with continued telemetry and repeated horizon estimation.

Perturbation: secretly shorten the available margin. The system should leave HOLD before the last viable action window closes.

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

- Do not equate aviation procedures, military tactics, theology, or fictional simulations with this conceptual architecture.
- Do not use these notes as operational flight or safety-critical guidance.
- Do not infer that humans literally compute a scalar viability horizon.
- Do not claim that one equation captures all time-pressure cognition or control.
- Preserve negative results if horizon-based regime selection does not improve behavior.
- Do not allow urgency to collapse telemetry into state truth.
- Do not treat HOLD as inherently virtuous; delayed action can be catastrophic when margin is overestimated.

## Working summary

Lucian OS should continuously ask:

1. What remains viable?
2. How long will it remain viable?
3. How uncertain is that estimate?
4. How much recovery margin does each path preserve?
5. What does waiting buy, and what margin does waiting consume?
6. How much diagnostic depth can still be afforded?
7. Has the original objective become infeasible?

The system should then choose a reasoning regime appropriate to the current viability horizon while preserving truth, bounded authority, and the possibility of correction.
