# Lucian OS — Relationally Corrigible Viability Model v0.01

## Status

First formal candidate model, 2026-09-04.

This note compresses the current Lucian OS architecture into a small set of state variables and decision rules. It is not a validated theory of human cognition, aviation, robotics, or control. Its purpose is to generate falsifiable simulator behavior.

## Core object

At time `t`, Lucian OS maintains a decision state:

`Z_t = (X_hat_t, U_t, R_t, A_t, V_t, H_hat_t, sigma_H_t, C_t)`

where:

- `X_hat_t` = current estimated body/world state;
- `U_t` = uncertainty over that estimate;
- `R_t` = currently trusted relational constraints among sensors, body, world, estimator, planner, and actuator;
- `A_t` = current authority envelope;
- `V_t` = currently admissible viability-preserving trajectories;
- `H_hat_t` = estimated viability horizon;
- `sigma_H_t` = uncertainty in that horizon estimate;
- `C_t` = estimated time/cost required to detect, decide, act, and verify a correction.

The hidden physical world is not identical to `X_hat_t`. Telemetry updates the estimate but does not become truth by declaration.

## Relational correction

Critical relations may include:

- sensor -> telemetry;
- telemetry -> state estimate;
- state estimate -> expected dynamics;
- command -> actuator response;
- actuator response -> body motion;
- body motion -> world displacement;
- world state -> sensor response;
- human intent -> authority envelope;
- authority envelope -> admissible action.

A diagnostic anomaly is therefore represented as a violated expected relation, not automatically as a failed component.

Candidate diagnostic question:

> Which expected relation has stopped holding, and which surviving hypotheses remain compatible with the total evidence?

## Conservative viability horizon

The system should not reason from the point estimate `H_hat_t` alone.

Define a conservative horizon:

`H_lower_t = max(0, H_hat_t - k * sigma_H_t)`

where `k` is a chosen conservatism factor.

Define corrective slack:

`S_t = H_lower_t - C_t`

Interpretation:

- `S_t >> 0`: substantial time/dynamic margin remains after accounting for uncertainty and correction latency;
- `S_t > 0`: some corrective margin remains;
- `S_t <= 0`: explanatory delay risks consuming the remaining correction window.

This is a prototype abstraction. In real systems the horizon may be vector-valued, state-dependent, nonlinear, or non-temporal.

## Viability set

Let:

`V_t = {pi : pi is physically reachable, authorized, sufficiently warranted, and viability-preserving under current constraints}`

This deliberately separates:

- physical capability;
- authority;
- epistemic warrant;
- competence;
- timing;
- recoverability.

If `V_t` is empty for the original objective, the correct result is `INFEASIBLE`, not fabricated completion.

## Decision regimes

Let the regime be:

`rho_t in {HOLD, RECONSTRUCT, STABILIZE_AND_DISCRIMINATE, PRESERVE, INFEASIBLE}`

### HOLD

Use when:

- current state remains viable;
- useful intervention is not yet warranted/effective;
- waiting is expected to improve action value or information;
- waiting does not consume corrective slack too quickly.

Candidate condition:

`expected_information_gain_rate > expected_margin_loss_rate`

subject to `S_t > 0`.

HOLD is active monitoring, not disengagement.

### RECONSTRUCT

Use when:

- `S_t` is large;
- several viable paths remain;
- deeper diagnosis can be afforded.

Behavior:

- generate competing hypotheses;
- triangulate across independent relations;
- perform safe epistemic actions;
- preserve unresolved alternatives.

### STABILIZE_AND_DISCRIMINATE

Use when:

- the horizon is contracting;
- the hypothesis space matters to action;
- one or a few bounded high-information probes still fit inside `S_t`.

Behavior:

- preserve current stability;
- suppress irrelevant analysis;
- run only discriminating probes whose latency fits the remaining margin.

### PRESERVE

Use when:

- `S_t <= 0`, or diagnostic depth itself would consume critical margin;
- at least one high-confidence preserving action remains.

Behavior:

- stop pursuing explanatory completeness;
- choose the safest validated preserving action;
- prefer reversibility, recoverability, and retained observability.

Principle:

> As time collapses, preserve viability before explanatory completeness.

And:

> Compress search, not truth.

### INFEASIBLE

Use when:

`V_t = empty set`

for the original objective.

This is not `UNKNOWN`.

- `UNKNOWN`: insufficient warrant to decide.
- `INFEASIBLE`: sufficient warrant that no admissible path satisfies the original objective.

The system should truthfully switch to a secondary preservation objective rather than invent a winning route.

## HOLD and commitment timing

A further candidate variable is commitment margin:

`M_t = H_lower_t - T_commit_t`

where `T_commit_t` is the estimated time needed to detect the trigger, decide, act, and verify.

Waiting is viable only while it preserves future action.

Candidate rule:

> HOLD while what waiting buys exceeds what waiting consumes.

Thus patience is not delay. It is calibrated non-intervention while the option to act remains viable.

## Epistemic action

When uncertainty is consequential and a safe authorized probe can discriminate among surviving hypotheses:

`uncertainty -> epistemic action -> telemetry -> state update -> regime/action update`

The probe is selected for information, not immediate task completion.

If no safe probe fits within remaining corrective slack, the regime should compress toward `PRESERVE` rather than manufacture certainty.

## FTLτA interpretation

### F

Authority prunes the possible action space. A shorter horizon does not manufacture permission.

### T

Telemetry, inference, and reality remain distinct. Changed evidence must be capable of changing warrant, reachability, regime, or action.

### L

Prefer paths that preserve constituents, recoverability, observability, and correction capacity where the task permits.

### A

Regime selection should depend on actual current relations and evidence rather than performed agreement or nominal-script replay.

### τ

The topology of viable action changes through time even without new learning. Paths can appear, disappear, or lose recoverability as the horizon contracts.

## Safety candidate

> A safe trajectory preserves the possibility of correction for as long as reality permits.

This implies that a path can reach the requested destination and still be unsafe if it consumes all correction capacity unnecessarily.

## First deterministic regime test

The companion prototype should distinguish at least these scenarios:

1. stationary/low-pressure context -> `HOLD`;
2. action not yet effective but becoming so -> `HOLD`;
3. anomaly with ample margin -> `RECONSTRUCT`;
4. anomaly with contracting margin -> `STABILIZE_AND_DISCRIMINATE`;
5. critical margin -> `PRESERVE`;
6. no viable path -> `INFEASIBLE`.

The thresholds in v0.01 are deliberately crude. Passing these toy cases does not validate the architecture; failing them is diagnostic.

## Next experimental bridge

- MouseSim 003: relational fault isolation (`body` vs `sensor` vs `world`).
- MouseSim 004: same uncertainty under different horizons, including HOLD-too-long and horizon-misestimation cases.

The long-term test is whether the same kernel can apply these distinctions across different simulated embodiments without special-case rewriting.
