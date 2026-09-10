# IAM-001 — Reference Simulation Trace

Status: reference trace from local sandbox execution of the v0.01 IAM logic

This is a deterministic architecture simulation using synthetic resource footprints and costs from `manifests/iam_learning_morphology_demo.json`.

It is **not** a benchmark of any real model, computer, or deployment.

Run from `modern-robotics/lucian-os`:

```bash
py prototype/learning_morphology_v001.py
```

## Fixed host

```text
memory  = 680 MB
cpu     = 6 units
network = 0
```

Key union footprints:

```text
heavy recurring + voice
  memory = 696 MB
  -> DOES NOT FIT

compiled recurring + voice
  memory = 648 MB
  cpu    = 6 units
  -> FITS
```

The host does not change between these states.

---

## Baseline — no learning

The recurring task always uses the heavy morphology.

Reference result:

```text
completed recurring cases = 30 / 30
voice deadline misses      = 0
recurring + voice concurrency ticks = 0
heavy executions           = 30
compiled executions        = 0
ticks to finish            = 37
modeled task cost          = 30.000
transition cost total      = 60
```

Every conflicting voice turn receives service, but the recurring task must wait because the heavy+voice union exceeds the host memory limit.

---

## Learning trajectory

Reference summary:

```text
completed recurring cases = 30 / 30
voice deadline misses      = 0
recurring + voice concurrency ticks = 4
heavy executions           = 12
compiled executions        = 19
compilations               = 2
retractions                = 1
ticks to finish            = 34
modeled task cost          = 23.900
transition cost total      = 97
```

Learning therefore improves completion time and modeled task cost in the reference scenario while preserving all voice starts and recurring completions.

However, the learning trajectory has **higher morphology-transition cost** than the baseline (`97 > 60`). This is important evidence for MAS-002 rather than a result to hide: more adaptive morphology can create more folding/unfolding overhead.

---

## Phase 1 — before compilation

### Tick 4

Voice arrives before the recurring task has earned a compiled skill.

Reference state:

```text
voice running      = yes
recurring running  = no
active skill       = none
memory used        = 544 MB
pending recurring  = 1
```

The heavy recurring morphology cannot coexist with voice:

```text
696 MB > 680 MB
```

This is the pre-learning feasibility boundary.

---

## Phase 2 — v1 skill changes morphology

### Tick 7

After six verified heavy resolutions:

```text
COMPILED v1
```

The recurring task's eligible morphology changes from:

```text
local_reasoner + document_parser + file_writer
```

to:

```text
compiled_transform + deterministic_verifier + file_writer
```

### Tick 8

The next interactive voice turn arrives.

Reference state:

```text
voice running      = yes
recurring running  = yes
recurring route    = compiled
memory used        = 648 MB
cpu used           = 6 / 6
```

This is the central IAM-001 observation:

> **The same host gains a new feasible concurrent task set because learned structure changed the recurring task's resource morphology.**

The same concurrency occurs at ticks 12 and 16.

---

## Phase 3 — drift makes truth bite

The workload changes from generation `v1` to `v2` beginning at case 17.

### Tick 18

The stale compiled v1 skill encounters the first processed v2 case.

Reference event:

```text
RETRACTED
old_generation      = v1
observed_generation = v2
reason              = verification_contradiction
```

The v1 skill is removed from routing eligibility.

The recurring case remains unresolved and must return to heavy reasoning.

### Tick 20

Voice arrives while no valid compiled skill exists.

Reference state:

```text
voice running      = yes
recurring running  = no
active skill       = none
```

The concurrency advantage has disappeared.

The same conflict occurs at tick 24.

This demonstrates the inverse of the learning effect:

> **When truth removes learned structure, the feasible morphology set can contract again.**

---

## Phase 4 — relearning restores the smaller morphology

### Tick 26

After six verified heavy v2 resolutions:

```text
COMPILED v2
```

### Tick 28

Voice arrives again.

Reference state:

```text
voice running      = yes
recurring running  = yes
recurring route    = compiled
memory used        = 648 MB
```

The lost concurrency returns.

Reference cycle:

```text
heavy v1
-> compile v1
-> new concurrency
-> drift
-> verification contradiction
-> retract v1
-> heavy v2
-> lost concurrency
-> compile v2
-> concurrency restored
```

---

## Authority control

A separate run revokes `write_records` during ticks 10–12 after the v1 skill has been learned.

Reference result:

```text
authority blocks     = 3
authority violations = 0
completed cases      = 30 / 30
```

During the revoked interval:

```text
recurring running = no
```

The compiled capability continues to exist conceptually, but it cannot execute until authority returns.

Learning therefore does not convert repeated permission into ownership.

---

## No-resource-gain negative control

The system is allowed to record the same successful compilation events, but the compiled route is artificially forced to retain the **same module footprint as the heavy route**.

Reference result:

```text
compilations       = 2
retractions        = 1
concurrent ticks   = 0
ticks to finish    = 38
modeled task cost  = 23.900
```

This is a critical negative control.

Merely setting:

```text
learned = true
```

does not create scheduling capacity.

The concurrency gain appears only when learned structure actually changes resource morphology.

---

## Checks

```text
T1_learning_creates_new_concurrency = PASS
T2_same_hardware_different_feasible_set = PASS
T3_drift_removes_then_recreates_concurrency = PASS
T4_learning_improves_trajectory_under_reference_costs = PASS
T5_authority_remains_non_compensatory = PASS
T6_learning_flag_without_resource_change_does_not_create_concurrency = PASS

overall = PASS
```

---

## What IAM-001 supports

IAM-001 supports a narrow executable architecture claim:

> **Acquired structure can change the scheduler's feasible set because knowledge can change computational morphology.**

In the reference simulation, learning does not merely reduce the cost of one task. It changes whether two tasks can coexist on a fixed host.

Drift then reverses that gain until the new structure is earned again.

A concise formulation is:

> **Learning changes what the body needs; what the body needs changes what the body can do.**

---

## Important tension exposed by the result

The learning trajectory has:

```text
lower task cost
faster completion
more concurrency
BUT
higher transition cost
```

This means IAM-001 strengthens the case for MAS-002.

A future scheduler must not assume that more frequent adaptation is automatically better. It must weigh the value of a better morphology against the cost of reshaping into and out of it.

The next discriminating question is therefore:

> **When is the future value of a morphology change large enough to justify the cost of making that change now?**
