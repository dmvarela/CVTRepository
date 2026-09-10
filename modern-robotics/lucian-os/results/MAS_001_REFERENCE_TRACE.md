# MAS-001 — Reference Simulation Trace

Status: reference trace generated from the v0.01 scheduling logic during development

This file records the expected behavior of `prototype/morphology_scheduler_v001.py` against the demo workload. It is a simulation reference, not evidence of performance on a real device.

## Scenario A — 768 MB base host

### Tick 0

Running:

```text
research -> local_research
```

Loaded union:

```text
document_parser
local_reasoner
web_retrieval
```

Resource use:

```text
memory = 688 MB
cpu = 4 / 5
network = 1 / 2
```

Transition cost from rest:

```text
11
```

### Tick 1

Interactive voice arrives.

Running:

```text
research -> local_research
voice    -> local_voice
```

Loaded union:

```text
audio_interface
document_parser
local_reasoner
web_retrieval
```

Resource use:

```text
memory = 720 MB
cpu = 5 / 5
network = 1 / 2
```

Only `audio_interface` needs to be added. `local_reasoner` is shared rather than loaded twice.

Transition cost:

```text
1
```

Background indexing waits because adding `file_reader` would push CPU demand above the current five-unit limit.

### Tick 2

Voice has completed.

Running:

```text
research -> local_research
index    -> local_index
```

Loaded union:

```text
document_parser
file_reader
local_reasoner
web_retrieval
```

Resource use:

```text
memory = 712 MB
cpu = 5 / 5
network = 1 / 2
```

Transition:

```text
unload audio_interface
load file_reader
cost = 2
```

### Tick 3

Research + index continue with no morphology change.

```text
transition cost = 0
```

### Tick 4

Research is complete; index continues.

Loaded union:

```text
document_parser
file_reader
local_reasoner
```

Resource use:

```text
memory = 664 MB
cpu = 4 / 5
network = 0 / 2
```

`web_retrieval` is released.

### Completion

```text
research completed at tick 4
voice completed at tick 2
index completed at tick 5
index waited 1 tick
```

Final contraction back to the empty resting module set has reference cost:

```text
5
```

---

## Scenario B — 700 MB pressure host

Tick 0 still permits:

```text
research -> local_research
memory = 688 MB
```

At tick 1, `local_research + local_voice` would require 720 MB and no longer fits.

The scheduler instead selects:

```text
research -> remote_research
voice    -> local_voice
```

Loaded union:

```text
audio_interface
local_reasoner
remote_research_service
```

Resource use:

```text
memory = 640 MB
cpu = 3 / 5
network = 2 / 2
```

This is the intended ECM/MAS behavior:

> change the morphology of the flexible task before declaring the host incompatible.

At tick 2 the short interactive pressure is gone. The current one-step scheduler switches research back to `local_research`.

That switch is intentionally recorded as a limitation rather than optimized away. It motivates MAS-002: should a scheduler pay another transition cost to return immediately, or preserve the temporary morphology for a while?

In this pressure case the private background indexing task starts only after research completes and finishes at tick 7.

---

## Scenario C — 620 MB privacy pressure

At 620 MB:

```text
local_research = too large
remote_research = feasible
```

The public research task therefore runs remotely.

The interactive voice turn still receives service when it arrives.

The private indexing task is different:

```text
local_index memory requirement = 664 MB > 620 MB
remote_index = physically smaller but privacy-inadmissible
```

Reference result after the bounded 10-tick simulation:

```text
research = complete
voice = complete
index = unresolved
index remaining work = 3 ticks
```

This unresolved state is a **success condition for the boundary test**, not a scheduler failure to be papered over.

The scheduler must not convert:

```text
private + resource pressure
```

into:

```text
therefore upload remotely
```

Optimization occurs only inside the admissible set.

---

## What the trace demonstrates

The reference trace supports four narrow claims about the prototype:

1. coexisting task morphologies can share modules;
2. scarce resources are allocated globally rather than by independent application requirement sheets;
3. a task can switch morphology under temporary pressure;
4. privacy can make an otherwise efficient morphology unavailable.

It does **not** establish optimal scheduling. In particular, Scenario B exposes morphology switching that may be reduced by hysteresis or lookahead.
