# Affordance Grammar v0.01

Status: exploratory architecture hypothesis

## Question

What is the smallest device-agnostic vocabulary Lucian OS needs in order to describe radically different embodiments well enough to compose task-specific morphologies?

The goal is not to classify devices. The goal is to describe **relations that a current substrate can actually support**.

> A device label is metadata. An affordance is operational structure.

## Candidate grammar

For v0.01, a host is described through six primitive relation families plus two constraint layers:

```text
SENSE        what can enter the system from the world
PRESENT      what the system can expose back to a user/world
COMPUTE      what transformations can be performed locally
STORE        what state can persist locally
COMMUNICATE  what other computational surfaces can be reached
ACT          what physical/digital state can be changed

RESOURCES    memory, power, bandwidth, latency and similar scarcity
AUTHORITY    which otherwise feasible actions/recruitments are admissible
```

A candidate host therefore has the form:

```text
H = (sense, present, compute, store, communicate, act, resources, authority)
```

This is intentionally not claimed to be mathematically minimal. ECM-003 tests whether it is **sufficiently small and sufficiently expressive** to replace product categories in the current prototype. Later ablations should try to merge or remove categories.

## Grammar rule 1 — primitive relations, not products

Allowed vocabulary should describe operational primitives:

```text
sense: proximity_sensors
present: audio_output
compute: local_model_runtime
store: filesystem
communicate: network_uplink
act: manipulator
```

The grammar should not need:

```text
vacuum_cleaner
smart_tv
robot
laptop
refrigerator
```

Those labels may be useful to humans, but they must not manufacture capability.

## Grammar rule 2 — capability and authority remain separate

`act.manipulator` means a manipulation path exists or is declared.

It does **not** mean Lucian may use it.

Likewise, `communicate.network_uplink` does not automatically authorize network use.

Thus:

```text
physical/reachable affordance != admissible affordance
```

The authority membrane remains an external constraint on composition.

## Grammar rule 3 — declared grammar is only a prior

This grammar describes the host interface Lucian is initially given. It does not supersede the Embodiment Map work.

The intended progression is:

```text
declared affordance grammar
-> bounded calibration
-> observed transition evidence
-> operational embodiment map
-> task-conditioned morphology
```

If reality contradicts the declaration, the operational map must win.

## Grammar rule 4 — modules depend on affordances, not device classes

A module should declare what relations it requires.

Example:

```text
robot_manipulation
requires:
  sense/perception path
  compute/reasoning path
  act.manipulator
  act.motor_controller
  authority.physical_actuation
```

It should not declare:

```text
requires_device_type: robot
```

## Grammar rule 5 — reachable capability can extend morphology without erasing embodiment

A weak local substrate may recruit remote reasoning through `communicate.network_uplink` when authorized.

This extends the reachable envelope but does not invent local sensors, displays, storage, or actuators.

> Internet extends the body's reach; it does not erase the body.

## Task-relative equivalence

Two substrates can be equivalent for one task and different for another.

Define:

```text
H1 ~_T H2
```

when the same admissible task morphology can be formed for task `T` from both hosts, up to irrelevant implementation differences.

This means there is no universal ordering such as:

```text
radio < TV < laptop < robot
```

The relevant question is whether the host's current affordance topology can support the task.

## Capability handshake

A future Lucian bootstrap should effectively ask:

```text
What can I sense?
What can I present?
What can I compute?
What can I store?
What can I communicate with?
What can I act upon?
What resources are currently scarce?
What am I authorized to use?
Which of these claims are empirically reliable?
```

The answer should form a provisional embodiment description rather than a pass/fail compatibility verdict.

## Quiet-revolution consequence

Traditional software asks:

> Is this device supported?

Lucian OS should ask:

> **What useful, bounded morphology can be composed from what is actually available here?**

This is the affordance-level implementation of the broader value proposition:

> **Lucian OS moves the burden of adaptation from the human to the machine.**

## ECM-003 target

The v0.01 grammar is successful only if:

1. current radio-like, TV-like, vacuum-like, refrigerator-like, laptop-like, and robot-like demos can be represented with no device `type` field;
2. the existing morphology composer can operate after a grammar-to-affordance compilation step;
3. renaming a substrate does not change composition;
4. removing a required primitive affordance does change composition;
5. authority remains separable from capability;
6. no device-specific conditional is required.

See `experiments/ECM_003_MINIMAL_AFFORDANCE_GRAMMAR.md` and `prototype/affordance_grammar_v001.py`.
