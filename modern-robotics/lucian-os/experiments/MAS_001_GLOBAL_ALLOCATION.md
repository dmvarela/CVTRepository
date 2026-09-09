# MAS-001 — Global Morphology Allocation Under Competing Tasks

Status: ready for local simulation

## Question

Can Lucian OS allocate a shared computational body across multiple concurrent tasks by reasoning over candidate morphologies, shared modules, resource limits, hard constraints, and reconfiguration cost rather than treating every task as an independent application requirement sheet?

## Files

```text
docs/MORPHOLOGY_ALLOCATION_AND_SCHEDULING_v0.01.md
manifests/morphology_scheduler_demo.json
prototype/morphology_scheduler_v001.py
```

Run from `modern-robotics/lucian-os`:

```bash
py prototype/morphology_scheduler_v001.py
```

Simulation only. No device action, remote call, permission change, or file mutation occurs.

---

## Workload

Three tasks arrive over time.

### Research

```text
arrival: 0
work: 4 ticks
priority: 3
latency: flexible
privacy: public
```

Candidate morphologies:

```text
local_research
  local_reasoner
  document_parser
  web_retrieval

remote_research
  remote_research_service
```

### Voice interaction

```text
arrival: 1
work: 1 tick
priority: 10
latency: interactive
max start delay: 0
privacy: public
```

Candidate morphologies:

```text
local_voice
  local_reasoner
  audio_interface

remote_voice
  cloud_reasoner
  audio_interface
```

### Background index

```text
arrival: 1
work: 3 ticks
priority: 1
latency: background
privacy: private
```

Candidate morphologies:

```text
local_index
  local_reasoner
  document_parser
  file_reader

remote_index
  cloud_reasoner
  document_parser
  file_reader
```

The remote indexing candidate is intentionally present but must be rejected by the privacy membrane because the task is `private`.

---

## Test A — shared-module accounting

Host memory:

```text
768 MB
```

At tick 1, research is already running and the interactive voice task arrives.

Naive per-task accounting would separately charge the full `local_reasoner` to both tasks.

Correct morphology accounting uses the union:

```text
research:
  local_reasoner
  document_parser
  web_retrieval

voice:
  local_reasoner
  audio_interface

union:
  local_reasoner
  document_parser
  web_retrieval
  audio_interface
```

Expected memory:

```text
512 + 128 + 48 + 32 = 720 MB
```

Expected result:

```text
research + voice coexist
background index waits because adding file_reader would exceed CPU capacity
```

This tests the proposition that the scheduler allocates a **shared morphology**, not independent application bundles.

---

## Test B — temporary resource pressure

Reduce host memory to:

```text
700 MB
```

Expected behavior:

```text
tick 0:
  local_research remains feasible at 688 MB

tick 1:
  local_research + local_voice no longer fits
  scheduler may transform research -> remote_research
  preserve local interactive voice
  both tasks continue inside the resource envelope
```

The important point is not the exact heuristic choice. It is that the scheduler searches **alternative morphologies** before declaring the host incompatible.

After the short pressure event, the current myopic scheduler may switch research back to the local form. That switching cost is deliberately exposed as evidence for MAS-002 rather than hidden.

---

## Test C — privacy is non-compensatory

Reduce host memory to:

```text
620 MB
```

The private indexing task's local morphology requires more memory than is available.

A remote indexing morphology would be much smaller, but the task privacy class forbids remote processing.

Expected:

```text
remote_index = INADMISSIBLE
local_index = RESOURCE_BLOCKED
index remains unresolved / delayed
```

The scheduler must **not** reason:

```text
remote is efficient -> therefore use remote
```

Instead:

```text
privacy constraint first
optimization second
```

This is a direct test that performance cannot buy its way through an admissibility boundary.

---

## Test D — transition economy

Track load/unload cost between ticks.

In the 768 MB case, expected trajectory includes:

```text
tick 0
  load local_reasoner + document_parser + web_retrieval

tick 1
  keep shared research modules
  load only audio_interface

tick 2
  unload audio_interface
  load file_reader
```

The scheduler should not reload `local_reasoner` separately for every task.

This is the first test of the principle:

> **Folding has a cost.**

---

## Pass criteria

MAS-001 supports the architecture if:

1. authority/privacy-inadmissible candidate morphologies are filtered before scoring;
2. shared modules are counted once in a coexisting morphology;
3. the interactive voice task starts on arrival in the base scenario;
4. the background task can wait rather than displacing the interactive task;
5. tighter memory can induce a task morphology substitution instead of binary host failure;
6. the private task is not remotely offloaded when its local form no longer fits;
7. transition loads/unloads are explicit;
8. final contraction returns to the resting module set.

---

## What a pass would not establish

MAS-001 does not show that the scheduling policy is optimal.

The current prototype is deliberately one-step / myopic. It may switch morphologies too readily because it does not reason over future transition costs or expected task duration.

A pass establishes only that **global morphology allocation is a distinct, executable problem** and that the current Lucian OS separations survive the move from single-task composition to concurrent resource scheduling.

---

## MAS-002 — hysteresis and lookahead

The next experiment should create a workload where a one-tick pressure event makes a remote morphology temporarily attractive.

Compare:

```text
myopic scheduler
vs
switching-penalty scheduler
vs
short-horizon lookahead scheduler
```

Measure:

```text
task completion
hard latency misses
module loads/unloads
morphology switches
external cost
privacy / authority violations
resource utilization
```

The central question becomes:

> **When should Lucian reshape, and when should it preserve its current shape because transformation itself is more costly than waiting?**
