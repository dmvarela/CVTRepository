# CP-001 — Reference Simulation Trace

Status: reference trace from local sandbox execution of the v0.01 computational-proprioception logic

This is a deterministic architecture simulation using synthetic observations from `manifests/computational_proprioception_demo.json`.

It is **not** a measurement of the user's computer, a real model runtime, or a production scheduler.

Run from `modern-robotics/lucian-os`:

```bash
py prototype/computational_proprioception_v001.py
```

## T1/T2 — sparse pressure: declaration versus experience

Declared transition estimate:

```text
local -> remote = 0.2
remote -> local = 0.2
```

Hidden experienced cost:

```text
local -> remote = 4.0
remote -> local = 4.0
```

Pressure arrives at ticks 3 and 10.

### Declaration-only scheduler

It never updates the map, so it repeats:

```text
tick 3  local -> remote
tick 4  remote -> local

tick 10 local -> remote
tick 11 remote -> local
```

Reference totals:

```text
realized total cost = 19.2
transition cost     = 16.0
finish tick         = 12
```

### Adaptive scheduler

After the first round trip it records:

```text
local -> remote = 4.0
remote -> local = 4.0
```

At tick 10 it now chooses:

```text
IDLE / WAIT
```

rather than paying for another expensive fold.

Reference totals:

```text
realized total cost = 11.8
transition cost     = 8.0
delay cost          = 1.6
finish tick         = 13
```

The adaptive policy deliberately accepts one extra completion tick because the experienced body map makes waiting cheaper than reshaping.

## T3 — host-condition drift

Early switching cost:

```text
1.0
```

After tick 8:

```text
5.0
```

The frozen map learns the early regime and then ignores contradictory later observations.

Reference frozen-map result:

```text
realized total cost = 26.4
transition cost     = 22.0
```

The adaptive map observes the first expensive post-drift round trip, sharply updates its transition estimates, and at the next pressure point chooses to wait.

Reference adaptive result:

```text
realized total cost = 17.9
transition cost     = 12.0
delay cost          = 2.5
```

This supports the narrow proposition that computational proprioception must remain dynamic rather than becoming a one-time installation benchmark.

## T4 — measured memory changes reachability

Fixed host:

```text
680 MB
```

Interactive voice morphology:

```text
120 MB
```

Compiled morphology declaration:

```text
300 MB
```

Declared predicted union:

```text
300 + 120 = 420 MB
420 <= 680 -> FEASIBLE
```

Bounded observation instead reports:

```text
compiled morphology = 590 MB
```

Operational predicted union becomes:

```text
590 + 120 = 710 MB
710 > 680 -> INFEASIBLE
```

Reference map update:

```text
declared_memory_mb   = 300
experienced_memory_mb = 590
operational_memory_mb = 590
status = DECLARED_ESTIMATE_OVERRIDDEN_BY_OBSERVATION
```

The observation therefore changes the feasible morphology set before future scheduling.

## T5 — host-scoped calibration

Host A previously taught Lucian that switching cost was high (`4.0`). A new Host B actually has a low switching cost (`0.5`).

### Incorrectly inherit Host A's body map

Reference result:

```text
realized total cost = 6.2
finish tick         = 14
```

The scheduler waits unnecessarily at both pressure points.

### Host B scoped calibration

Reference result:

```text
realized total cost = 5.2
finish tick         = 12
```

Host B calibrates its own transition behavior and uses the cheap alternate morphology.

This makes calibration provenance load-bearing:

> **A learned body map belongs to an embodiment/context, not to Lucian universally.**

## T6 — authority invariance

The simulation includes a transition recorded as:

```text
possible   = true
measured   = true
confidence = 0.99
required_authority = write_records
```

The active authority set does not include `write_records`.

Reference outcome:

```text
BLOCK
```

Measurement increases warrant about capability. It does not create permission.

## Checks

```text
T1_declared_costs_can_cause_repeated_bad_folds = PASS
T2_experience_changes_future_scheduling = PASS
T3_recalibration_tracks_host_drift = PASS
T4_measured_memory_changes_reachability = PASS
T5_calibration_is_host_scoped = PASS
T6_measurement_does_not_manufacture_authority = PASS

overall = PASS
```

## What CP-001 supports

CP-001 supports a narrow executable claim:

> **Scheduling quality can improve when declared computational affordances are treated as priors and replaced by experienced host-specific measurements that remain corrigible over time.**

It also links the earlier Embodiment Map work directly to MAS:

```text
declared body
-> bounded computational action
-> measured consequence
-> operational body map
-> trajectory scheduler
```

## What CP-001 does not establish

It does not establish realistic load times, memory accounting, energy models, thermal behavior, confidence estimation, safe automatic probing, or production-quality online learning. The costs and observations are synthetic and exist to make the architectural distinction falsifiable.

The next high-value step is to move from synthetic observation to a **read-only real-host probe** on the Windows development machine: measure RAM/CPU/runtime availability and, only if explicitly authorized, bounded model load/unload timings without file mutation or external actuation.
