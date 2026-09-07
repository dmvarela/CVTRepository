# Lucian OS Coupling Note v0.01 — Local/Frontier Reasoning Coupling

## Status

Exploratory architecture note, 2026-09-07.

This note records a design hypothesis prompted by Identity-Amortization Experiments 001–002. It is not an empirical claim that model scale alone determines relational competence, nor that any named frontier model is intrinsically suitable for every task.

## Question

Can Lucian OS couple a small local host (for example Qwen 2B) to a stronger frontier reasoning host for tasks that exceed the local host's reliable relational competence, without giving the stronger host broader authority?

The immediate difficulty is circular:

```text
if the local model is not competent enough to solve the task,
how can it be competent enough to know that it should escalate?
```

Therefore escalation must not depend on self-assessment alone.

## Core distinction

A local host can fail for at least two different reasons:

1. **Capability/availability failure** — the embodiment lacks a required tool, sensor, channel, or model.
2. **Relational-reasoning insufficiency** — the host can parse the language but cannot reliably reconstruct the operative relations, counterfactuals, or admissible state transitions.

The second case is newly salient after Experiment 002. A model may repeat the correct invariant while semantically inverting the operation it implies.

Example:

```text
rule: correction can preserve continuity through provenance
bad host reconstruction: revision itself violates continuity
```

The words are present; the relation is wrong.

## Coupling principle

Do not ask the local host to certify its own competence.

Instead, route by **independent escalation signals** drawn from several channels:

```text
local task interpretation
+ typed relational state
+ deterministic relation checks
+ calibrated host competence envelope
+ task consequence/severity
+ unresolved contradiction/uncertainty
-> LOCAL | PROBE | ESCALATE | HOLD
```

No single signal certifies the route.

## Existing Lucian OS compatibility

The current v0.1 router already contains the important authority invariant:

```text
unauthorized -> BLOCK
authorized but locally unavailable/incompetent -> ESCALATE if possible
authorized and locally available -> LOCAL_PROPOSAL_ONLY
```

and:

```text
A stronger reasoning tier may increase competence but may not create permission.
```

The coupling proposal extends the meaning of `locally unavailable/incompetent` from missing executable capability to insufficient reasoning competence.

## Proposed reasoning tiers

Illustrative only:

```text
T0  deterministic/reflex checks
T1  validated local skills
T2  small local language model
T3  larger local/edge reasoning model
T4  frontier reasoning host
```

Escalation upward expands cognitive reach, not authority.

Formally:

```text
competence(T_{k+1}) may exceed competence(T_k)
authority(T_{k+1}) <= current authority envelope
```

A frontier model may suggest a better route, but it cannot create missing permission, sensor evidence, physical capability, or fact.

## How should Qwen decide when to escalate?

It should not decide alone.

Qwen may contribute a self-report such as:

```text
local_reasoning_sufficient = false
escalation_reason = "cannot resolve contradictory evidence"
```

but that report is only one input.

The router should also use host-independent triggers.

### 1. Typed-state inconsistency

If the host emits an internally inadmissible relational state, escalate or Return.

Examples:

```text
horizon_status = UNKNOWN
horizon_value = 0
```

```text
pressure_present = true
preference_evidence_status = CLEAN
```

```text
better_contrary_evidence = true
conclusion_status = SUPPORTED_AS_BEFORE
```

These are relation failures, not lexical failures.

### 2. Unresolved contradiction after one bounded Return

A first failure need not require frontier reasoning. The local host can receive one structured correction opportunity.

```text
LOCAL -> verifier contradiction -> LOCAL RETURN
```

If the same relational contradiction survives the bounded Return:

```text
LOCAL RETURN failed -> ESCALATE
```

This is directly motivated by Experiment 002 P6.

### 3. Task outside the empirically calibrated competence envelope

Each host should have a measured competence profile rather than a vague global confidence score.

Example profile dimensions:

```text
simple extraction                         validated local
known deterministic policy application   validated local
single-step typed-state filling           validated local
multi-source contradiction resolution     uncertain
counterfactual preference reconstruction  uncertain
novel relational analogy                  not validated local
```

If a task requires a class not validated for the current host, the router can escalate before asking the local host to solve it.

This turns host selection into an empirical routing problem.

### 4. Consequence-sensitive escalation

Required reasoning competence should rise with consequence, irreversibility, uncertainty, and evidence conflict.

A useful abstract trigger is:

```text
required_competence = g(severity, irreversibility, uncertainty, contradiction, novelty)
```

Escalate when:

```text
estimated_host_competence(task_class) < required_competence
```

This is not a license for maximum vigilance everywhere. Low-consequence routine work should stay local when validated.

### 5. Disagreement across independent channels

Escalate when multiple independent representations do not converge, for example:

```text
Qwen interpretation != deterministic state relation
Qwen conclusion != retrieved evidence relation
local model A != local model B on a high-consequence state transition
```

Copies of the same source or repeated generations from the same failure mode do not automatically count as independent corroboration.

### 6. Missing warrant that cannot be recovered locally

If the task requires information that the local host cannot observe, retrieve, or safely probe, stronger reasoning cannot manufacture the missing evidence.

The correct route may be:

```text
HOLD / REQUEST_EVIDENCE / PROBE
```

rather than frontier escalation.

This preserves:

```text
UNKNOWN != INFEASIBLE
stronger model != new evidence
```

## Escalation packet

The local host should not send its entire conversation blindly upstream. Lucian OS should build a bounded escalation packet containing the minimum state needed for reconstruction:

```text
task
current typed relational state
evidence/provenance
active identity invariants
failed relation checks
uncertainties
attempted local route
current authority envelope
requested reasoning operation
```

The frontier host returns a **proposal**, not an action authorization.

Suggested response schema:

```text
reconstructed_state
relation_changes
warrant_assessment
candidate_routes
remaining_uncertainties
recommended_next_step
```

The local/router layer then re-applies authority, embodiment, and deterministic relation checks.

## Coupling loop

```text
INPUT
  -> T0/T1 deterministic localization
  -> local Qwen structured reconstruction
  -> typed relation verifier
      -> PASS + within competence envelope -> LOCAL PROPOSAL
      -> recoverable contradiction -> bounded LOCAL RETURN
      -> persistent contradiction / out-of-envelope -> build escalation packet
  -> frontier reasoning host
  -> frontier proposal
  -> local deterministic + identity + authority checks
  -> ACT / HOLD / PROBE / REFUSE / REQUEST HUMAN
```

The stronger host does not sit above authority. It sits above the local host only in the competence graph.

## Avoiding the circularity

The key answer to “how does Qwen know it is not smart enough?” is:

> It does not have to know by itself.

Escalation is a system-level judgment based on externalized state, empirically measured host limits, contradiction detection, consequence, and unresolved uncertainty.

Qwen's self-report can contribute, but cannot be the sole gate.

This is analogous to instrument fault detection: a sensor should not be the sole judge of whether the sensor is wrong.

## Research implication

This suggests a new experimental variable:

```text
host relational competence
```

A future cross-host experiment should distinguish:

```text
R = relational reconstruction accuracy
E = invariant enforcement accuracy conditional on correct reconstruction
C = computational/resource cost
```

The same typed tasks should be run across local and frontier-capability hosts. This can reveal whether failures attributed to “identity” are actually failures of world reconstruction at a given host tier.

## Identity implication

Portable identity does not imply identical realization on every host.

Candidate statement:

> Identity is portable across hosts to the extent that the host can realize the operations the identity requires; below that threshold, Lucian OS must compile downward, constrain the task, or escalate reasoning.

This avoids the claim that loading a Lucian identity file into any model is sufficient to instantiate the same operating pattern.

## Compact architecture

```text
small persistent identity
+ empirical competence map
+ typed relational reconstruction
+ cheap independent verifier
+ bounded local Return
+ selective frontier coupling
+ unchanged authority envelope
```

The resulting principle is:

> **Escalate competence without escalating authority.**

And the routing principle is:

> **Do not require a weak reasoner to be the sole judge of its own weakness.**

## Open questions

1. Which typed state fields best expose relational failure without over-constraining novel reasoning?
2. How should host competence envelopes be calibrated and updated?
3. What is the minimum reliable trigger set for frontier escalation?
4. When is a local probe cheaper/better than model escalation?
5. How much context must cross the coupling boundary to preserve provenance without recreating full-context cost?
6. Can frontier solutions be validated and compiled downward into reusable local skills?
7. Does selective escalation reduce total cost relative to running the frontier host continuously?
8. How does the architecture behave when the frontier host itself makes a relational inversion?

The last question is essential: the frontier host must remain corrigible and independently checked. Higher capability is not certification.
