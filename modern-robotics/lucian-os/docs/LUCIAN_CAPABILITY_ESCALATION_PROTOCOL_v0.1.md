# Lucian Capability & Escalation Protocol v0.1

## Status

Draft implementation protocol for Lucian OS.

This version is intentionally small and conservative. It defines the minimum information needed for a Lucian instance to understand an embodiment, classify a task, decide whether the task can be handled locally, and construct a bounded escalation packet when local competence is insufficient.

## 1. Embodiment handshake

Every embodiment exposes a manifest containing:

```text
identity
sensors
actuators
local_compute
available_models
validated_skills
network
energy
latency_constraints
authority_defaults
verification_methods
```

The kernel should not assume a device has a capability that is absent from the manifest.

## 2. Capability declaration

Each capability should define at least:

```text
name
kind: observe | act | compute | communicate
inputs
outputs
risk_level
reversible
requires_confirmation
verification
local_cost
latency_class
```

Example:

```json
{
  "name": "read_file",
  "kind": "observe",
  "inputs": ["path"],
  "outputs": ["text"],
  "risk_level": "low",
  "reversible": true,
  "requires_confirmation": false,
  "verification": "returned content",
  "local_cost": "low",
  "latency_class": "interactive"
}
```

## 3. Task envelope

Before planning, represent the user request as a bounded task envelope:

```text
purpose
requested_outcome
scope
explicit_constraints
authority
reversibility_preference
latency_need
privacy_need
uncertainty
```

The task envelope is not permission to infer broader goals.

## 4. Competence tiers

Default reasoning tiers:

```text
T0 deterministic function / control
T1 validated local skill
T2 small local model
T3 edge or workstation model
T4 frontier or central AI
```

An embodiment may omit unavailable tiers.

The router should prefer the lowest tier that can satisfy the task under the current constraints.

## 5. Routing factors

For each candidate tier, evaluate:

```text
capability_fit
competence_confidence
uncertainty
risk
latency
energy
privacy
network_availability
authority_compatibility
verification_available
```

No single score is required in v0.1. A rule-based classifier is acceptable and preferred for the first prototype because it is inspectable.

## 6. Escalation triggers

Escalate when one or more of the following is true:

- required capability is absent locally;
- local competence is below the task threshold;
- uncertainty exceeds the allowed bound;
- the task requires novel multi-step reasoning not covered by a validated skill;
- available evidence conflicts and cannot be resolved locally;
- the action is high consequence and policy requires stronger review;
- a required reality interface exists only upstream.

Do **not** escalate merely because a stronger model exists.

## 7. Escalation packet

A remote intelligence should receive the smallest sufficient packet:

```text
instance_id
embodiment_id
task_id
purpose
requested_outcome
current_state
relevant_observations
epistemic_status
attempted_local_steps
remaining_uncertainty
available_capabilities
authority_envelope
prohibited_actions
risk_level
requested_role
verification_plan
provenance
```

The packet should not silently expand authority.

## 8. Remote response contract

A remote reasoner returns a **proposal**, not raw motor control, unless the task envelope explicitly grants a narrower validated control role.

Response fields:

```text
proposal
assumptions
required_capabilities
confidence
uncertainties
requested_additional_evidence
authority_needed
verification_steps
```

The local kernel remains responsible for checking feasibility, authority, and verification.

## 9. Epistemic membrane

Before a proposition may be used as confirmed state, label it:

```text
observed
retrieved
inferred
reconstructed
unknown
```

Then attach:

```text
warrant
provenance
confidence
contradictions
```

A hypothesis may be useful without becoming fact.

## 10. Authority membrane

Before an action executes, verify:

```text
capability exists
action fits purpose
action fits scope
authority is current
authority is sufficient
required confirmation obtained
action does not exceed prohibited_actions
verification method exists or failure is explicitly accepted
```

A remote model's recommendation does not satisfy these checks by itself.

## 11. Verification loop

Preferred loop:

```text
observe
-> interpret
-> triangulate when needed
-> warrant
-> plan
-> authorize
-> act
-> observe consequence
-> verify
-> update state
-> preserve provenance
-> return or close
```

If verification fails, do not silently mark the task complete.

## 12. Graceful degradation

When a higher tier becomes unavailable:

```text
full competence -> reduced competence envelope
```

not:

```text
network loss -> uncontrolled behavior
```

The local system should know what it can still safely do, what must pause, and what should be returned to later.

## 13. Downward compilation

A repeated upstream solution may become a local skill only after validation.

The new skill should record:

```text
origin_problem_class
source_reasoning_tier
validation_tests
known_limits
required_authority
verification_method
version
```

Do not convert a one-off frontier answer into a local policy merely because it worked once.

## 14. v0.1 test questions

The first prototype should be able to answer, for a synthetic task:

1. What embodiment capabilities are available?
2. What reasoning tier should handle the task?
3. Why is that tier sufficient or insufficient?
4. What is known vs inferred?
5. Is an action authorized?
6. What requires confirmation?
7. How would the outcome be verified?
8. If escalation is needed, what exact bounded packet should be sent?

## 15. v0.1 non-goals

This protocol does not yet define:

- real-time motor control;
- distributed consensus among many Lucian nodes;
- cryptographic identity;
- secure remote attestation;
- production robotics safety certification;
- autonomous deployment across devices;
- self-modifying policy.

Those may be future layers. v0.1 is about proving the architecture can separate capability, competence, warrant, authority, escalation, and verification cleanly.
