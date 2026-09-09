# Lucian OS — Morphology Allocation & Scheduling v0.01

Status: exploratory architecture hypothesis

## Core distinction

A capability manifest answers:

> What components and transitions might be available?

A morphology composer answers:

> What admissible configuration can solve this task?

A morphology scheduler answers a different question:

> **Given multiple active tasks, scarce shared resources, alternative morphologies, and non-zero reconfiguration cost, how should the available computational body be organized over time?**

This is the distinction between **inventory**, **composition**, and **orchestration**.

```text
DISCOVERY
  what exists?

CALIBRATION
  what actually works?

COMPOSITION
  what forms can solve each task?

ALLOCATION / SCHEDULING
  which forms should coexist, wait, substitute, or transform now?
```

The scheduler is therefore not another hardware detector. It is the layer that turns a possibility space into an evolving resource policy.

---

## Morphology as trajectory

A task does not necessarily have one fixed morphology.

```text
resting morphology
-> parse morphology
-> reasoning morphology
-> verification morphology
-> presentation morphology
-> resting morphology
```

For concurrent tasks, Lucian OS must reason over a sequence:

```text
M_0 -> M_1 -> ... -> M_t -> ... -> M_n
```

Each transition has a cost. Loading/unloading models, opening/closing remote paths, moving data, warming caches, requesting authority, and reallocating memory are not free.

Define a transition cost:

```text
K(M_i, M_j)
```

A globally sensible schedule may therefore keep a component resident even when it is briefly unused if unloading and reloading it would cost more than retaining it.

This introduces a future requirement for **hysteresis / anti-thrashing**.

---

## Hard constraints before optimization

The scheduler must not collapse authority, privacy, truth, and performance into one compensatory score.

First construct the admissible set:

```text
F_t = {
  schedules / morphologies that are physically reachable,
  sufficiently competent,
  authorized,
  privacy-compatible,
  within hard safety constraints,
  and grounded in the current operational embodiment map
}
```

Only then optimize inside `F_t`.

A high-priority task cannot purchase unauthorized authority. A lower-latency route cannot justify prohibited data exposure. A stronger model cannot manufacture a missing actuator. Resource pressure cannot change epistemic status by itself.

Candidate lexicographic policy for v0.01:

1. reject inadmissible candidates;
2. avoid hard latency/deadline violations;
3. maximize useful service across active tasks;
4. prefer lower external / privacy / monetary exposure where otherwise comparable;
5. minimize reconfiguration cost;
6. preserve headroom where useful.

This order is provisional and must be tested.

---

## Shared modules matter

Two task morphologies cannot be costed independently when they share components.

Example:

```text
research morphology:
  local_reasoner
  document_parser
  web_retrieval

voice morphology:
  local_reasoner
  audio_interface
```

Naive accounting:

```text
research memory + voice memory
```

Morphological accounting:

```text
union(research modules, voice modules)
```

`local_reasoner` is loaded once and can serve both tasks if scheduling / throughput constraints permit.

This is one reason the scheduling object is a **configuration graph**, not a sum of application requirement sheets.

---

## Alternative morphologies

The same task may have several admissible forms.

```text
public research
  A: local reasoner + local parser + web retrieval
  B: bounded remote research service
```

Under abundant local resources, `A` may be preferred.

Under temporary memory pressure, `B` may permit an interactive task to run without terminating the research task.

This is the important distinction:

> **Degrade or transform morphology before declaring device incompatibility.**

But substitution remains constrained. A private task whose policy forbids remote processing may have no admissible remote morphology. In that case the scheduler must delay, degrade through another local path, or report infeasibility; it must not silently offload the task.

---

## Task attributes

A future scheduler will need more than a scalar priority.

Candidate task state:

```text
task_id
arrival_time
remaining_work
latency_class
hard_deadline / max_start_delay
priority / service importance
interruptibility
minimum quality
privacy class
authority requirements
candidate morphologies
verification requirement
```

Important distinctions:

- interactive latency is not the same as task importance;
- background work may be important but deferrable;
- non-preemptible control loops differ from batch analysis;
- a task can remain epistemically uncertain while receiving a different scheduling posture.

This should remain compatible with `DECISION_AXES_v0.03.md`: scheduling pressure may change reasoning regime or commitment posture without manufacturing truth or authority.

---

## Resource state

The scheduler consumes live computational proprioception rather than static machine specifications.

Candidate state:

```text
memory_free
cpu_headroom
gpu / accelerator occupancy
network capacity
battery / power budget
thermal state
loaded modules
cache state
reachable services
current authority
privacy constraints
active tasks
```

The correct scheduling decision can change while the hardware list stays constant.

---

## v0.01 scheduler object

For the first simulation, each task supplies one or more already-composed candidate morphologies.

The scheduler does **not** yet discover modules itself. It chooses among candidate task morphologies.

At each tick:

```text
1. collect arrived unfinished tasks
2. remove inadmissible candidate morphologies
3. enumerate feasible coexisting task/morphology assignments
4. account for shared modules by union, not duplicate sum
5. reject assignments exceeding resource limits
6. rank remaining assignments lexicographically
7. advance selected tasks
8. record morphology transition cost
9. repeat
10. contract to resting morphology when finished
```

This separation is intentional:

```text
Morphology Planner
  -> candidate forms per task

Morphology Scheduler
  -> globally compatible form(s) now
```

---

## Known limitations of v0.01

The first scheduler is deliberately small and myopic.

It does not yet model:

- lookahead over future arrivals;
- true parallel throughput contention inside a shared model;
- GPU kernels or accelerator residency;
- continuous-control deadlines;
- stochastic task duration;
- thermal or battery dynamics;
- bandwidth that scales per consumer rather than per loaded module;
- explicit quality degradation curves;
- starvation guarantees;
- learned transition costs;
- distributed multi-host scheduling;
- authority changes during a task.

Most importantly, a one-step scheduler can **thrash** between morphologies when a short-lived pressure event makes a temporary alternative attractive. That behavior should be measured rather than hidden. A later version should add lookahead, switching penalties, or hysteresis.

---

## Quiet-revolution interpretation

The user should not have to perform manual morphology scheduling by saying:

```text
close this program
move that job to another computer
use the web version
turn quality down
pause indexing
free memory
switch models
```

Those are currently human decisions about how to shape the machine around work.

Lucian OS aims to internalize that reasoning while preserving explicit authority, privacy, and truth constraints.

> **A capability manifest tells Lucian what might be possible. Intelligence begins when Lucian decides how those possibilities should be organized in service of the task.**

See `experiments/MAS_001_GLOBAL_ALLOCATION.md` and `prototype/morphology_scheduler_v001.py`.