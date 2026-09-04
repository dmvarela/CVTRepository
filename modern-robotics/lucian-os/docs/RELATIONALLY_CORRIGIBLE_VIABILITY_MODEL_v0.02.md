# Lucian OS — Relationally Corrigible Viability Model v0.02

## Status

Second formal candidate model, 2026-09-04.

v0.02 preserves the v0.01 regime structure but makes intervention latency explicit and corrects a flaw in the original HOLD criterion.

This remains a simulation hypothesis, not a validated control law or a model of human physiology, aviation, or cognition.

## Discovery provenance

The immediate trigger was a cross-domain observation: interventions often have a delay between command and effect. The conversation used insulin timing as a biological analogy, alongside braking, aircraft control response, and projectile travel time. The analogy did not serve as evidence for the architecture; it exposed a missing variable in the model.

The technical candidate is therefore:

> command time is not effect time.

A viability model must reserve enough horizon not merely to choose an action, but for that action to begin changing the trajectory and, where required, to verify the result.

## Core timing decomposition

v0.01 used one aggregate correction latency `C_t`.

v0.02 decomposes it:

`C_t = T_detect + T_decide + T_initiate + T_effect + T_verify`

with:

- `T_detect` = time to detect or recognize the relevant state;
- `T_decide` = time to select an action/regime;
- `T_initiate` = command or actuation-start latency;
- `T_effect` = delay before the intervention begins materially changing the trajectory;
- `T_verify` = time required to observe whether the intended effect occurred.

Define:

`T_to_effect = T_detect + T_decide + T_initiate + T_effect`

and:

`T_cycle = T_to_effect + T_verify`

The distinction matters because an action can be correct but too slow to affect the state before the viability horizon closes.

## Conservative horizon and corrective slack

As before:

`H_lower_t = max(0, H_hat_t - k * sigma_H_t)`

v0.02 uses:

`S_t = H_lower_t - T_cycle`

Interpretation:

- `S_t > 0`: some conservative margin remains after reserving a full correction cycle;
- `S_t <= 0`: the system should not spend that margin pursuing explanatory completeness if a preserving action is available.

This gives a direct test for time-to-effect:

Two cases may share the same `H_hat_t` and `sigma_H_t` but select different regimes solely because `T_effect` differs.

## HOLD correction

v0.01 contained the candidate condition:

`expected_information_gain_rate > expected_margin_loss_rate`

This was too loose because those quantities were not guaranteed to have compatible units. v0.02 removes that comparison.

Instead, HOLD is evaluated over an explicit next-review interval.

Let:

`Delta_wait = next_review_interval * margin_loss_rate`

and:

`S_after_wait = S_t - Delta_wait`

Then HOLD is permitted only if:

- the current state remains viable;
- useful intervention is not yet effective/warranted;
- waiting is expected to improve future action value;
- `S_after_wait > hold_reserve`.

Candidate rule:

> HOLD only while the next planned review still preserves a required corrective reserve.

This turns HOLD from indefinite patience into active, revisable non-intervention.

## Adversarial tests added in v0.02

### 1. Same horizon, different time-to-effect

Case A:

- same horizon estimate;
- same horizon uncertainty;
- short effect latency.

Expected: `STABILIZE_AND_DISCRIMINATE`.

Case B:

- identical except for long effect latency.

Expected: `PRESERVE`.

Purpose: prove that `T_effect` changes downstream behavior rather than appearing only in logs.

### 2. Same horizon estimate, different uncertainty

Case A:

- point estimate unchanged;
- low uncertainty.

Expected: `RECONSTRUCT`.

Case B:

- same point estimate;
- high uncertainty.

Expected: `PRESERVE`.

Purpose: prove that uncertainty about the margin itself constrains diagnostic ambition.

### 3. HOLD reserve consumed before next review

The current state is viable and waiting would normally improve action value, but the planned review interval consumes too much corrective slack.

Expected: reject HOLD and move to the safest validated preserving action.

Purpose: test the proposition that patience is calibrated non-intervention, not delay.

## Current regime set

v0.02 retains:

- `HOLD`
- `RECONSTRUCT`
- `STABILIZE_AND_DISCRIMINATE`
- `PRESERVE`
- `INFEASIBLE`

Known limitation: this regime set does not yet cleanly separate ordinary `EXECUTE/COMMIT` timing from reasoning mode. The archer example exposes that omission. A later version may need two axes: a reasoning regime and a commitment posture.

This limitation is preserved deliberately rather than hidden by overloading `PRESERVE` or `HOLD` with meanings they do not have.

## Emerging principle

> Viability depends not only on whether an action is available, but whether its effect can arrive before the relevant correction window closes.

Equivalent operational question:

> Given the dynamics already in motion, what state will be reached by the time my action can actually matter?

## Next experimental bridge

1. MouseSim 003 — relational fault isolation (`body`, `sensor`, `world`).
2. MouseSim 004 — combine fault hypotheses with contracting viability horizons and explicit time-to-effect.
3. Later: separate reasoning regime from commitment posture (`HOLD`, `COMMIT/EXECUTE`, possibly `ABORT`).

## Guardrails

- The insulin example is a discovery analogy, not a medical control model.
- The aviation and driving examples are structural analogies, not operational guidance.
- Thresholds remain intentionally crude and falsifiable.
- Passing the deterministic matrix validates only code behavior against our stated toy expectations.
- Negative results and regime ambiguities should be retained as evidence for model revision.
