# CP-001 — Measured Computational Proprioception

Status: executable simulation experiment

## Question

Can Lucian OS improve morphology scheduling by treating declared resource and transition costs as priors, then replacing them with bounded empirical measurements of the host it actually inhabits?

Core hypothesis:

> **A computational body should be learned operationally, not merely enumerated declaratively.**

This extends the existing embodiment-calibration rule:

```text
G_declared
-> bounded action / configuration change
-> observed consequence
-> G_experienced
-> G_operational
```

For computational embodiment, consequences include:

```text
memory delta
load / unload latency
CPU / accelerator occupancy
network demand
energy / thermal effect
failure / retry behavior
cache warmup
transition cost
```

CP-001 tests only synthetic memory and transition-cost observations.

## Files

```text
manifests/computational_proprioception_demo.json
prototype/computational_proprioception_v001.py
results/CP_001_REFERENCE_TRACE.md
```

Run from `modern-robotics/lucian-os`:

```bash
py prototype/computational_proprioception_v001.py
```

Simulation only. No real machine probing, device action, permission change, network call, or model call occurs.

## T1 — declared transition cost can be wrong

The scheduler begins with a declared/prior cost of `0.2` for switching between local and remote morphologies. The hidden experienced cost is `4.0`.

Two sparse pressure events occur at ticks 3 and 10.

A declaration-only scheduler repeatedly makes the same fold because its map never changes.

## T2 — experienced cost changes future scheduling

The adaptive scheduler observes the first expensive round trip and updates both transition estimates to `4.0`.

At the second sparse pressure event it should choose to let flexible work wait rather than repeat the expensive fold.

This is the scheduling form of:

> **Truth has to bite by changing reachability / preference.**

## T3 — computational embodiment can drift

Early in the run, local/remote transitions cost `1.0`. Later host conditions change and the same transitions cost `5.0`.

A frozen operational map continues switching as if the old body still existed.

An adaptive map should treat new observations as evidence that the current embodiment has changed and alter future scheduling.

Possible real-world causes include thermal throttling, memory pressure, runtime changes, model cache state, power state, or competing workload. CP-001 does not model those mechanisms directly.

## T4 — measured resource footprint changes feasibility

A compiled morphology is declared to require `300 MB`, while bounded observation reports `590 MB`.

With a `120 MB` interactive workload on a `680 MB` host:

```text
declared prediction:
300 + 120 = 420 MB -> feasible

experienced / operational prediction:
590 + 120 = 710 MB -> infeasible
```

The operational map must remove the concurrency path after measurement.

## T5 — calibration is host-scoped

A transition cost learned on Host A must not silently become truth about Host B.

The experiment compares:

```text
incorrectly inherit Host A high switching cost
vs
start Host B with a prior and calibrate Host B itself
```

Host identity, runtime version, hardware state, and calibration provenance therefore belong in the learned embodiment map.

## T6 — measurement does not manufacture authority

A transition can be:

```text
possible = true
measured = true
confidence = high
```

and still be unavailable because required authority is absent.

Calibration updates warrant about capability/cost. It does not expand permission.

## Pass criteria

CP-001 supports the architecture if:

1. static declared costs cause a repeated bad fold;
2. observed transition cost changes a later scheduling decision and reduces realized cost;
3. new contradictory cost observations after drift alter the operational map and improve later decisions;
4. measured memory can invalidate declared feasibility;
5. host-scoped calibration outperforms blindly transferring a stale body map in the new-host control;
6. measured capability remains blocked when authority is absent.

## Architectural interpretation

MAS-002 asked:

> Which trajectory of morphologies is best given transition costs?

CP-001 asks:

> **Where do those transition costs come from?**

The proposed answer is not simply configuration files. It is computational proprioception:

```text
request morphology
-> observe resource consequence
-> update embodiment map
-> schedule from experienced map
-> keep recalibrating when reality changes
```

Concise formulation:

> **Lucian should not merely discover what the host says it is. It should learn how this host actually behaves when inhabited.**
