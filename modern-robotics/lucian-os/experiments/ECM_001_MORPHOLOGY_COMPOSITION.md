# ECM-001 — Morphology Composition Across Embodiments

Status: ready for local simulation

## Question

Can one Lucian OS composition rule form materially different bounded computational morphologies from different host affordances, rather than treating hardware as a fixed pass/fail requirement list?

## Hypothesis

Given:

```text
host affordances
+ task demand
+ trusted module registry
+ authority policy
```

the morphology composer should select the smallest admissible module set that satisfies the task, prefer local components when sufficient, recruit remote components only when necessary, and report precise failure when no complete admissible morphology exists.

## Prototype

```text
prototype/morphology_composer.py
manifests/elastic_demo_hosts.json
```

The prototype is simulation-only. It does not execute actions, download modules, call remote AI, or grant permissions.

## Test matrix

### E1 — old radio / spoken interaction

```bash
py prototype/morphology_composer.py --host old-radio-demo --task speak_with_user
```

Expected structural result:

```text
radio has audio I/O + network but no local model runtime
-> recruit cloud_reasoner
-> compose audio_interface
-> viable spoken morphology
-> close remote connection and unload temporary modules afterward
```

The point is not that an arbitrary old radio can literally run the prototype. The manifest represents a radio-like host that exposes a minimal programmable bootstrap, network, and audio affordances.

### E2 — smart TV / visual explanation

```bash
py prototype/morphology_composer.py --host smart-tv-demo --task show_explanation
```

Expected structural result:

```text
TV has display + local model runtime
-> choose local_reasoner
-> compose visual_interface
-> no remote reasoning required
```

### E3 — vacuum / floor cleaning

```bash
py prototype/morphology_composer.py --host vacuum-demo --task clean_floor
```

Expected structural result:

```text
vacuum has locomotion + proximity sensors + suction
-> choose deterministic_floor_cleaner
-> no language model required
```

This is a discriminating test against the naive rule "harder-looking task => larger model."

### E4 — refrigerator / temperature regulation

```bash
py prototype/morphology_composer.py --host fridge-demo --task regulate_fridge
```

Expected structural result:

```text
temperature sensor + compressor control
-> choose temperature_controller
-> no reasoning module required for baseline regulation
```

### E5 — laptop / research

```bash
py prototype/morphology_composer.py --host laptop-demo --task research_question
```

Expected structural result:

```text
local model runtime + network
-> local_reasoner
-> web_retrieval
-> hybrid local/reachable morphology
```

### E6 — robot / object manipulation

```bash
py prototype/morphology_composer.py --host robot-demo --task pick_up_object
```

Expected structural result:

```text
camera + compute + manipulator + motor controller
-> robot_perception
-> local_reasoner
-> robot_manipulation
```

## Counterfactual tests

### C1 — remove radio uplink

```bash
py prototype/morphology_composer.py --host old-radio-demo --task speak_with_user --remove-affordance network_uplink
```

Expected result:

```text
NO_COMPLETE_ADMISSIBLE_MORPHOLOGY
```

Reason should identify the missing path to reasoning rather than calling the entire device "incompatible."

### C2 — vacuum can act physically but is not authorized

```bash
py prototype/morphology_composer.py --host vacuum-demo --task clean_floor --deny-authority physical_actuation
```

Expected result:

```text
physical affordances remain present
but admissible morphology is blocked by authority
```

This tests:

> capability != authority

### C3 — laptop under memory pressure

```bash
py prototype/morphology_composer.py --host laptop-demo --task research_question --memory-mb 256
```

Expected structural result:

The local reasoner should become unavailable because its declared memory cost exceeds the new limit. The composer should attempt a lower-memory reachable composition where dependencies allow it, rather than treating the original local shape as mandatory.

### C4 — host mismatch

```bash
py prototype/morphology_composer.py --host vacuum-demo --task show_explanation
```

Expected result:

The vacuum should not invent a display. The output should identify the missing affordance and reject the morphology.

## Measurements

For each run record:

```text
host
task
selected modules
local modules
remote modules
provided functions
memory cost
required authority
unmet demands
diagnostic class
contraction plan
```

## Failure criteria

The experiment should be considered a failure or require redesign if the composer:

1. selects the same maximal module bundle for most tasks;
2. treats missing authority as missing physical capability;
3. invents host affordances;
4. uses remote reasoning when a lower-cost local composition is sufficient;
5. fails to expose why a morphology cannot form;
6. accumulates temporary modules or authority without a contraction path;
7. relies on device labels ("TV", "vacuum", "robot") instead of declared affordances.

## Next experiment

If ECM-001 behaves as expected, ECM-002 should remove the named device categories entirely and describe hosts only as affordance manifests.

That would test the stronger proposition:

> **The composer should not need to know whether it inhabits a radio, TV, refrigerator, vacuum, laptop, or robot. It should need to know what can be sensed, computed, communicated, displayed, stored, and controlled.**
