# Lucian OS — Problem Solving Architecture v0.01

## Status

Frozen conceptual architecture note, 2026-09-04.

This note records an emerging interpretation of Lucian OS as a general problem-solving architecture rather than only a robot-control, fault-diagnosis, or pressure-response system.

It is a candidate architecture, not a validated general theory of intelligence.

## Discovery provenance

The insight emerged after a sequence of concrete experiments and analogies rather than from a prior claim that Lucian OS was a universal problem solver.

1. MouseSim 001 tested empirical action-consequence learning.
2. MouseSim 002 showed that changed evidence must alter warrant and planning.
3. MouseSim 003 showed that causal attribution should depend on patterns of relations and that underdetermined evidence must remain `UNKNOWN`.
4. The relational viability model introduced time-sensitive reasoning regimes such as `HOLD`, `RECONSTRUCT`, `STABILIZE_AND_DISCRIMINATE`, `PRESERVE`, and `INFEASIBLE`.
5. Driving, aviation, Sabbath/HOLD, Kobayashi Maru, and time-to-effect examples sharpened the role of temporal margin, commitment, delayed effects, and honest infeasibility.
6. The resulting realization was that these mechanisms jointly describe not merely control under pressure but a broader structure for solving problems under uncertainty.

The claim therefore comes after the experimental structure, not before it.

## Core proposition

Problem solving is not adequately represented as:

`problem -> compute answer`

A more realistic Lucian OS candidate is:

`FRAME -> INFER -> TEST -> UPDATE -> CHOOSE REGIME -> ACT/HOLD -> RETURN`

with the loop repeated as reality supplies new evidence.

The system is solving two problems at once:

1. the object-level problem: what should be believed or done?
2. the meta-level problem: how should this problem be solved from the current state, with the current uncertainty, authority, tools, time, and recoverability?

Candidate formulation:

> An intelligent problem solver must adapt not only its answer, but its method of inquiry and commitment as the problem state changes.

## Need for a solution does not manufacture a solution

A central epistemic constraint is:

> Need for a solution does not manufacture a solution.

The system must distinguish at least:

- `KNOWN_ENOUGH_TO_ACT`
- `UNKNOWN`
- `INFEASIBLE`

These are not interchangeable.

- `KNOWN_ENOUGH_TO_ACT` means available warrant is sufficient for the required action under the current risk and authority envelope.
- `UNKNOWN` means evidence does not yet warrant a unique conclusion or action.
- `INFEASIBLE` means there is sufficient warrant that no admissible path satisfies the original objective.

Urgency may change how much inquiry can be afforded, but it must not convert `UNKNOWN` into false certainty or `INFEASIBLE` into fabricated completion.

## Problem-solving state

A candidate problem-solving state at time `t` is:

`P_t = (Q_t, X_hat_t, U_t, H_t, A_t, V_t, R_t, C_t, O_t)`

where:

- `Q_t` = current problem framing or question;
- `X_hat_t` = current estimated state of body/world/task;
- `U_t` = uncertainty over that estimate;
- `H_t` = currently live hypotheses/explanations;
- `A_t` = authority envelope;
- `V_t` = currently admissible viability-preserving trajectories;
- `R_t` = trusted and contested relational constraints;
- `C_t` = correction/intervention latency including time-to-effect;
- `O_t` = available observation, probe, tool, and action options.

The state is dynamic. New telemetry, time passage, failed probes, or changed constraints may alter any of these terms.

## Core loop

### 1. FRAME

Determine what problem is actually being solved.

Questions include:

- What changed?
- Which objective is primary?
- Which constraints are binding?
- Is the observed symptom the problem, or evidence of a deeper relational failure?

Framing is revisable. A later contradiction may show that the original problem statement was wrong.

### 2. INFER

Generate explanations or candidate state hypotheses without treating completion as fact.

Examples:

- world constraint;
- sensor/observation failure;
- body/actuator failure;
- external disturbance;
- task infeasibility;
- insufficient evidence.

The hypothesis set should remain plural when the evidence is underdetermined.

### 3. TEST

When consequential uncertainty remains and an authorized safe probe exists, select an epistemic action that discriminates among surviving hypotheses.

The relevant question is not merely:

`What can I measure?`

but:

`Which available observation or action most changes the decision-relevant uncertainty before the viability horizon closes?`

### 4. UPDATE

Telemetry and other evidence update:

- hypothesis warrant;
- trusted/contested relations;
- reachability;
- horizon estimates;
- available tools/actions;
- the problem framing itself.

Truth must be capable of changing downstream behavior.

### 5. CHOOSE REGIME

The system selects how much problem solving can still be afforded.

Current candidate reasoning regimes:

- `RECONSTRUCT` — ample margin for broad hypothesis generation and triangulation;
- `STABILIZE_AND_DISCRIMINATE` — contracting margin; preserve state and use only bounded high-value probes;
- `PRESERVE` — explanatory depth would consume critical corrective margin;
- `INFEASIBLE` — no admissible path satisfies the original objective.

`HOLD` is currently better interpreted as a commitment posture rather than purely a reasoning regime. This distinction remains unresolved and should be tested rather than hidden.

### 6. ACT / HOLD

Commitment is separate from inference.

Possible postures include:

- `HOLD` — active observation while intentionally withholding intervention;
- `EXECUTE` — commit to an authorized, sufficiently warranted action;
- `ABORT/REROUTE` — leave a trajectory whose correction capacity is degrading;
- `PRESERVE` — prioritize survivability/recoverability over explanatory completeness;
- `REFUSE` — no authorized action exists;
- `INFEASIBLE` — original objective cannot be satisfied.

Candidate principle:

> Do not confuse urgency with readiness.

And:

> HOLD only while waiting preserves the option to act later.

### 7. RETURN

After action, observation, or deliberate non-action, return to reality.

The next loop begins from the actual consequences rather than from the prior plan.

This is the architectural meaning of:

> No single path certifies itself.

and:

> Reality is redundant.

The system should be able to leave a hypothesis, return by another evidentiary route, and revise if the routes diverge.

## Adaptive problem-solving depth

The same epistemic state may rationally produce different actions under different temporal envelopes.

Example:

`diagnosis = UNKNOWN`

with large corrective slack may yield:

`RECONSTRUCT -> several probes`

The same `UNKNOWN` with moderate slack may yield:

`STABILIZE_AND_DISCRIMINATE -> one high-value probe`

The same `UNKNOWN` with exhausted slack may yield:

`PRESERVE -> safest validated preserving action`

The uncertainty has not disappeared. The permissible depth of inquiry has changed.

Candidate principle:

> Compress search, not truth.

## Problem solving as management of commitment

A recurring structure across the current work is that intelligence involves managing when to commit.

The system must distinguish:

- when to infer;
- when to verify;
- when to ask reality through a probe;
- when to wait;
- when to commit;
- when to preserve rather than explain;
- when to admit that the original objective is infeasible.

Thus a candidate deeper formulation is:

> Problem solving is the disciplined management of uncertainty, action, and time until either a warranted solution emerges or the system truthfully recognizes that none remains available.

This definition explicitly permits unresolved states and honest failure.

## Relation to FTLτA

### F — bounded authority

Possible actions are not automatically permissible actions. Problem-solving competence cannot manufacture authority.

### T — truth / warrant

Claim strength must remain bounded by evidence. Missing evidence does not authorize causal completion. Changed evidence must be capable of changing the model and the action plan.

### L — preservation / relation

Where multiple paths satisfy the task, prefer those that preserve constituents, reversibility, observability, and correction capacity.

### A — agency

The system should independently evaluate the actual state and available evidence rather than merely replaying a script or mirroring an expected answer.

### τ — time / return / persistence

Questions may remain unresolved. Paths may appear or disappear as time advances. History and provenance should survive correction. Return is part of the solving process, not an afterthought.

## Relation to relational viability

Relational viability provides the object of diagnosis and safety evaluation.

The problem solver does not ask only:

`Which component failed?`

It asks:

`Which expected relation has stopped holding, and which candidate explanation best fits the surviving relational pattern?`

This permits forms of analytical redundancy where evidence is distributed across relationships rather than duplicated sensors.

## Relation to the viability horizon

Problem-solving depth is constrained by remaining correction margin.

A useful decision architecture therefore requires:

`state uncertainty + relation uncertainty + viable paths + horizon uncertainty + time-to-effect`

rather than merely a static problem description.

An otherwise correct intervention can fail if its effect arrives after the relevant window closes.

## Candidate architecture

A current high-level Lucian OS problem-solving loop is:

```text
OBSERVE
  -> FRAME
  -> ESTIMATE STATE + UNCERTAINTY
  -> GENERATE / PRESERVE HYPOTHESES
  -> CHECK RELATIONAL CONSISTENCY
  -> ESTIMATE VIABILITY HORIZON + TIME-TO-EFFECT
  -> SELECT REASONING REGIME
  -> SELECT COMMITMENT POSTURE
  -> ACT / PROBE / HOLD / REFUSE
  -> TELEMETRY
  -> UPDATE / CORRECT
  -> RETURN
```

This loop is deliberately model-agnostic and embodiment-agnostic at the conceptual level. Whether that abstraction survives more complex control systems remains an empirical question.

## Experimental implications

### MouseSim 004

Combine:

- `UNKNOWN` relational diagnosis;
- several available discriminating probes;
- different viability horizons;
- different probe latencies;
- different intervention time-to-effect.

Expected behavior:

- large horizon -> deeper reconstruction;
- contracting horizon -> choose one discriminating probe;
- critical horizon -> preserve without pretending uncertainty was resolved;
- infeasible case -> return `INFEASIBLE`;
- misestimated horizon -> preserve the failure and ask which additional relation could have corrected the estimate.

### Later tests

- separate reasoning regime from commitment posture;
- test whether the same kernel generalizes across different simulated embodiments;
- test whether false urgency causes premature commitment;
- test whether excessive patience causes loss of the last viable path;
- test whether changing evidence actually changes both diagnosis and action;
- preserve negative results where the abstraction fails.

## Guardrails

- Do not claim Lucian OS is a complete theory of intelligence.
- Do not claim current toy simulations validate general human, biological, aviation, or robotics behavior.
- Preserve `UNKNOWN` and `INFEASIBLE` as legitimate outputs.
- Do not allow time pressure to inflate epistemic certainty.
- Do not allow increased competence to expand authority automatically.
- Do not hide model failures by retuning thresholds after every adversarial case.
- Preserve discovery provenance, including accidental interpretations and later corrections.

## Working summary

Lucian OS is increasingly interpretable as a problem-solving architecture whose central task is not merely to produce answers, but to manage the evolving relation among evidence, uncertainty, authority, action, timing, and recoverability.

Its strongest current candidate principle is:

> Need for a solution does not manufacture a solution.

And its operational companion is:

> Solve the problem in the way the current reality still permits: investigate when margin allows, discriminate when margin contracts, preserve when explanation would arrive too late, and report infeasibility when no admissible solution exists.
