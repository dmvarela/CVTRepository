# ECM — Operational Topology and Task-Relative Embodiment v0.01

Status: exploratory bridge note

## 1. Why the label-free test changes the abstraction

ECM-002 asks whether descriptive device labels are load-bearing for morphology composition.

If changing `radio`, `vacuum`, `TV`, or `robot` labels while preserving operational affordances leaves the selected morphology unchanged, then the relevant object is not the device category itself.

The stronger candidate abstraction is:

> **An embodiment is an operational affordance topology under resource and authority constraints.**

Device names are useful human summaries of common bundles. They should not manufacture capability.

---

## 2. Connection to the existing Embodiment Map

`EMBODIMENT_MAP_AND_CALIBRATION_v0.2.md` already distinguishes:

```text
G_declared -> safe action -> observed consequence -> G_experienced -> G_operational
```

ECM should therefore not ultimately compose morphologies from a static manufacturer manifest alone.

A declared camera, motor, network path, filesystem, or model runtime is only a prior.

The morphology composer should increasingly reason from `G_operational`: the currently warranted map of transitions the embodiment has actually shown it can support.

This gives a stronger pipeline:

```text
declared affordances
-> bounded calibration
-> operational topology
-> task demand
-> morphology composition
-> action / verification
-> topology update
-> contraction
```

Thus morphology and calibration form a loop rather than a one-time compatibility check.

---

## 3. Morphology as a task-conditioned subgraph

Let:

```text
G_op = current operational embodiment graph
G_reach = trusted reachable external services/modules
P_T = admissible authority/privacy envelope for task T
D_T = task demand
```

A task morphology can be treated provisionally as a selected task-conditioned subgraph:

```text
M_T subset of (G_op union G_reach)
```

subject to:

```text
satisfies(D_T)
respects(P_T)
within resource / latency / cost bounds
contains verification / return path where required
```

Authority can remove otherwise physically reachable edges. Network loss can remove reachable external nodes. Calibration can downgrade or retract edges that reality contradicts.

This makes morphology a dynamic topological object rather than a fixed installed application.

---

## 4. Task-relative equivalence of bodies

Two physically different hosts may be operationally equivalent for one task while radically different for another.

Define:

```text
H1 ~T H2
```

when H1 and H2 admit functionally equivalent admissible morphologies for task T under the relevant quality threshold.

Examples:

- a connected radio and smart speaker may be equivalent for spoken conversation;
- a TV and laptop may be equivalent for displaying an explanation;
- the same pair may not be equivalent for editing local files;
- a vacuum and mobile robot may share navigation affordances but differ in manipulation.

Therefore there is no single universal ranking of devices as simply "weak" or "strong." Capability is task-relative and configuration-relative.

---

## 5. Affordance grammar

If device labels are non-load-bearing, Lucian OS needs a compact vocabulary for describing what substrates can expose.

Candidate high-level families:

```text
SENSE
  audio_input
  vision
  proximity
  temperature
  position

PRESENT
  audio_output
  display
  haptics

COMPUTE
  deterministic_runtime
  local_model_runtime
  accelerator

STORE
  volatile_memory
  persistent_storage
  filesystem

COMMUNICATE
  local_bus
  LAN
  network_uplink

ACT
  write_file
  move
  manipulate
  regulate
  switch

POWER / RESOURCE
  battery
  mains
  thermal_budget
  memory_budget

AUTHORITY / CONSTRAINT
  read
  write
  actuation
  external_send
  privacy
  confirmation
```

These labels are themselves provisional. The goal is not to invent a perfect universal ontology before testing. The goal is to identify the smallest grammar that supports useful composition without reverting to device-specific branching.

---

## 6. Capability handshake

A future host adapter could expose a capability handshake rather than a device identity requirement:

```text
Lucian bootstrap: What transitions can you currently support?
Host adapter: Here is my declared scaffold.
Lucian calibration: Which of these transitions are warranted now?
Morphology composer: What is the least costly admissible form for this task?
```

The user should not have to know the hardware requirements, driver topology, model size, or application compatibility matrix.

The system absorbs that translation burden.

---

## 7. Internet is reachability, not embodiment

Network connectivity should not be treated as magical capability.

Internet access adds reachable nodes and services to `G_reach`; it does not erase local physical constraints or create authority.

For example:

```text
old radio + audio I/O + bootstrap + network
```

may recruit remote reasoning and become conversational.

But:

```text
old radio + network
```

cannot become a robot manipulator without an actuation path.

Likewise, safety-critical reflexes should remain local when network latency or failure would make remote dependence unsafe.

---

## 8. Quiet-revolution consequence

Traditional compatibility asks:

```text
What is this device?
Does it meet the software requirements?
```

ECM asks:

```text
What is operationally reachable from here?
What does the task require?
What is admissible?
What morphology can be formed now?
```

The practical value proposition remains:

> **Lucian OS moves the burden of adaptation from the human to the machine.**

The technical reframing underneath it becomes:

> **Hardware is not an eligibility category. It is a task-relative possibility space.**

---

## 9. Next experimental direction

After ECM-002 label invariance, ECM-003 should test the affordance grammar itself.

Questions:

1. Can a small canonical affordance vocabulary describe materially different hosts without device-specific branches?
2. Can composition operate over `G_operational` rather than raw declared capability lists?
3. Can calibration change morphology selection when an affordance is observed to fail?
4. Can two different substrates be recognized as task-equivalent without sharing a device category?
5. Can network loss, authority loss, or resource pressure alter only the affected region of morphology rather than collapsing the whole system?

The point is not to prove a universal ontology. It is to find the smallest experimentally useful grammar for adaptive embodiment.
