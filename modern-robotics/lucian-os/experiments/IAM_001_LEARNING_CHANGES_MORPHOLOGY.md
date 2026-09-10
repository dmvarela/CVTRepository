# IAM-001 — Learning Changes Morphology

Status: executable simulation experiment

## Question

Can a verified learned skill change the resource morphology of a task enough to alter which workloads can coexist on the **same unchanged host**?

This experiment couples two prior Lucian OS ideas:

```text
IA-002
  repeated reasoning can become earned compiled structure

MAS-001
  task morphologies compete for shared resources
```

The integrated hypothesis is:

> **Learning can change the operational capability envelope without changing the hardware, because learned structure can change the resource morphology that the scheduler must allocate.**

The inverse must also hold:

> When reality contradicts a compiled skill, retraction should restore the heavier reasoning morphology and remove any concurrency that depended on the smaller learned form.

---

## Files

```text
manifests/iam_learning_morphology_demo.json
prototype/learning_morphology_v001.py
results/IAM_001_REFERENCE_TRACE.md
```

Run from `modern-robotics/lucian-os`:

```bash
py prototype/learning_morphology_v001.py
```

Simulation only. No model calls, network calls, device actions, file mutations, or permission changes occur.

---

## Host

The host remains fixed throughout the main experiment:

```text
memory = 680 MB
cpu    = 6 units
network = 0
```

The recurring task initially requires:

```text
HEAVY MORPHOLOGY
local_reasoner    512 MB
 document_parser   128 MB
 file_writer        24 MB
--------------------------
union             664 MB
```

An interactive voice turn requires:

```text
local_reasoner    512 MB
 audio_interface    32 MB
--------------------------
union             544 MB
```

Because the two heavy task morphologies share `local_reasoner`, their combined union is:

```text
local_reasoner
 document_parser
 file_writer
 audio_interface

memory = 696 MB
```

That does **not** fit the 680 MB host.

After sufficient verified repetition, the recurring task may earn:

```text
COMPILED MORPHOLOGY
compiled_transform       48 MB
 deterministic_verifier   32 MB
 file_writer              24 MB
-------------------------------
union                    104 MB
```

Combined with voice, the union becomes:

```text
compiled_transform
 deterministic_verifier
 file_writer
 local_reasoner
 audio_interface

memory = 648 MB
cpu    = 6 units
```

That **does** fit the same host.

Nothing about the hardware has changed.

---

## Workload

Thirty recurring cases arrive, one per tick.

```text
cases 1–16  -> generation v1
cases 17–30 -> generation v2
```

The change at case 17 represents distribution drift.

Interactive voice turns arrive at:

```text
4, 8, 12, 16, 20, 24, 28
```

Voice has a hard start commitment in the toy scheduler.

The recurring task needs six same-generation heavy resolutions before a compiled skill becomes active.

---

## Expected developmental trajectory

### Phase 1 — before learning

At tick 4:

```text
voice + heavy recurring = 696 MB > 680 MB
```

Expected:

```text
voice runs
recurring case waits
```

### Phase 2 — v1 compiled

After six verified heavy resolutions, Lucian compiles a v1 skill.

At tick 8:

```text
voice + compiled recurring = 648 MB <= 680 MB
```

Expected:

```text
voice runs
recurring case runs
same host
new concurrency
```

### Phase 3 — reality changes

When the first v2 case reaches the stale v1 compiled path, verification should contradict it.

Expected:

```text
compiled v1
-> verification contradiction
-> RETRACT
-> return recurring task to heavy reasoning
```

At the next interactive pressure points, the old concurrency advantage should disappear.

### Phase 4 — v2 relearned

After enough verified v2 heavy cases:

```text
compile v2
```

Expected:

```text
smaller recurring morphology returns
voice + recurring concurrency becomes feasible again
```

This is the central cycle:

```text
reason
-> verify
-> learn structure
-> morphology contracts
-> feasible set expands
-> reality changes
-> verification contradicts
-> learned structure retracts
-> morphology expands
-> feasible set contracts
-> relearn
-> morphology contracts again
```

---

## Controls

### T1 — baseline without learning

Disable compilation entirely.

Expected:

```text
voice remains protected
recurring heavy task waits on every conflicting voice tick
concurrency = 0
```

### T2 — same hardware, different morphology

Compare the fixed host against:

```text
heavy + voice    = 696 MB -> infeasible
compiled + voice = 648 MB -> feasible
```

This tests whether the change in feasible task sets comes from morphology rather than hardware.

### T3 — drift

The v1 skill must be removed from eligibility when v2 contradicts it.

A system that preserves the smaller morphology after contradictory verification fails.

### T4 — trajectory comparison

Compare no-learning and learning runs for:

```text
verified completion
voice deadline misses
completion time
modeled task cost
```

Lower cost or faster completion is not a pass if voice deadlines or task completion degrade.

### T5 — authority revocation

Temporarily remove `write_records` after compilation.

Expected:

```text
compiled capability still exists
execution is blocked
no authority violation occurs
```

Learning cannot manufacture permission.

### T6 — no-resource-gain negative control

Allow the system to record a successful compilation event, but force the compiled route to retain the exact same module footprint as the heavy route.

Expected:

```text
learning flag = yes
resource contraction = no
new concurrency = no
```

This distinguishes the architectural claim from a bookkeeping artifact.

---

## Pass criteria

IAM-001 supports the coupling hypothesis if all of the following occur:

1. the no-learning baseline has zero recurring/voice concurrency;
2. a genuinely smaller learned morphology creates concurrency on the unchanged host;
3. drift retracts the stale skill and removes the concurrency advantage;
4. relearning the new generation restores that advantage;
5. the reference learning trajectory preserves all required completions and interactive starts while improving at least one resource/economic trajectory metric;
6. authority remains a hard gate after compilation;
7. a fake compilation with no resource-footprint change creates no concurrency gain.

---

## What a pass would mean

A pass would support a narrow executable proposition:

> **Acquired structure can change the scheduler's feasible set because knowledge can change computational morphology.**

This is stronger than saying that a learned skill is cheaper in isolation.

It says that learning one recurrent task can free enough scarce resource to alter what the whole host can do at the same time.

---

## What a pass would not establish

IAM-001 does not establish:

- real-world RAM savings from compiled AI skills;
- a universal validation threshold;
- safe automatic code generation;
- optimal scheduling;
- realistic model-loading behavior;
- real-time robotics guarantees;
- that all learning should result in compilation;
- that compiled skills should remain permanently resident.

The module footprints, costs, task stream, and drift point are synthetic and chosen to make the coupling falsifiable.

---

## Architectural interpretation

Before IAM-001:

```text
learning policy
and
resource scheduling
```

could be treated as neighboring systems.

IAM-001 asks whether the correct architecture is instead a feedback loop:

```text
intent
-> morphology
-> schedule
-> execute
-> verify
-> experience
-> learned structure
-> changed morphology
-> changed schedule
-> ...
```

A concise formulation:

> **Learning changes what the body needs; what the body needs changes what the body can do.**
