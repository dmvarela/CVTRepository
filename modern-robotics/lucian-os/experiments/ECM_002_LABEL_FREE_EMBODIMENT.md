# ECM-002 — Label-Free Embodiment and Morphological Invariance

Status: ready for local simulation

## Question

Does Lucian OS actually need to know *what kind of device* it inhabits, or can it compose a useful task-specific morphology from affordances, resources, reachable modules, and authority alone?

This experiment tests the stronger Lucian OS proposition:

> **Hardware categories should describe historical bundles of affordances, not determine eligibility or behavior.**

A `radio`, `TV`, `vacuum`, `refrigerator`, `laptop`, or `robot` label must not itself create capability.

## Core hypothesis

For a fixed task, two hosts with the same relevant:

```text
affordances
resources
authority
resting modules
```

should produce the same selected morphology even if their names, device categories, manufacturers, form factors, or human labels differ.

Formally, if hosts H1 and H2 are equivalent over the fields used by the composer for task T,

```text
A(H1) = A(H2)
R(H1) = R(H2)
P(H1) = P(H2)
```

then, modulo descriptive metadata,

```text
M(H1, T) = M(H2, T)
```

where:

- A = affordance set
- R = relevant resource constraints
- P = authority/admissibility envelope
- M = chosen morphology

## Why this matters

Traditional software often begins from a device or platform category:

```text
What device is this?
-> choose compatible software
-> reject unsupported devices
```

The Lucian OS inversion is:

```text
What can this substrate sense, compute, store, communicate, and control?
+ what is the task?
+ what is authorized?
-> compose the minimum sufficient morphology
```

If device labels influence the composer, the system has quietly reintroduced the old compatibility model.

## Method: metamorphic invariance

This is a metamorphic test: instead of asking only whether one output is correct, transform an input in a way that *should not matter* and require the output to remain invariant.

For each baseline host:

1. compose a morphology for a task;
2. rename the host id;
3. replace the host `type` with an arbitrary unrelated string;
4. remove the `type` field entirely;
5. compose again after each transformation;
6. compare morphology signatures.

The signature intentionally excludes descriptive host metadata and keeps only operational structure:

```text
selected modules
local modules
remote modules
provided functions
memory cost
required authority
unmet demands
disposition
```

## Cases

### E1 — radio-like affordances, label destroyed

Baseline:

```text
id: old-radio-demo
type: connected_radio
affordances: audio_input, audio_output, network_uplink, bootstrap_compute
```

Transform to:

```text
id: substrate-001
type: purple_box
```

Expected:

```text
cloud_reasoner + audio_interface
```

The label must not matter.

### E2 — vacuum-like affordances, label destroyed

Baseline task: `clean_floor`

Expected morphology:

```text
deterministic_floor_cleaner
```

Rename the host and replace `robot_vacuum` with `kitchen_appliance`, then remove type entirely.

Expected: morphology unchanged.

### E3 — robot-like affordances, label destroyed

Baseline task: `pick_up_object`

Expected morphology:

```text
local_reasoner
robot_perception
robot_manipulation
```

Again, labels must not affect composition.

## Negative control: change an affordance

A good invariance test also needs a transformation that *should* matter.

For the robot-like substrate, remove `manipulator` while keeping the label `mobile_manipulator` unchanged.

Expected:

```text
NO_COMPLETE_ADMISSIBLE_MORPHOLOGY
```

This is crucial: if the system still succeeds because the host *says* it is a robot/manipulator, the architecture is label-driven rather than affordance-driven.

## Negative control: change authority

Keep all physical affordances but remove `physical_actuation` authority.

Expected:

```text
physically possible, not admissible
```

Again:

> capability != authority

## Stronger implication

If ECM-002 passes, then device categories become optional descriptive metadata rather than load-bearing routing input.

That yields a deeper abstraction:

> **An embodiment is an affordance topology under resource and authority constraints.**

Human labels such as `radio`, `TV`, `vacuum`, and `robot` are convenient summaries of common topologies, but Lucian OS should reason from the topology itself.

## Functional equivalence classes

The experiment also suggests that multiple physically different devices can belong to the same *task-relative equivalence class*.

For task T, define:

```text
H1 ~T H2
```

when H1 and H2 expose enough equivalent affordances, resources, and authority to admit the same task morphology.

This equivalence is task-relative. Two devices may be equivalent for spoken conversation but not for navigation or manipulation.

That means Lucian OS need not maintain a universal ontology of every device ever manufactured. It can instead reason over a smaller vocabulary of affordances and compositions.

## Failure criteria

ECM-002 fails if:

1. changing only id/type labels changes the operational morphology;
2. removing the type field causes composition failure;
3. keeping a familiar label compensates for a genuinely missing affordance;
4. authority can be inferred from device category;
5. the composer requires a growing catalog of device-specific branches.

## Prototype test

Run:

```bash
py prototype/test_label_invariance.py
```

The test should report PASS for label transformations and PASS for negative controls that correctly change composition when affordances or authority change.

## Next question

If labels are non-load-bearing, the next layer is not "support more devices." It is:

> **What is the smallest useful universal affordance vocabulary from which device-specific morphologies can be composed?**

That becomes ECM-003: affordance grammar and capability topology.
