# ECM-003 — Candidate Minimal Affordance Grammar

Status: ready for local simulation

## Research question

Can Lucian OS describe and compose useful task-specific morphologies across radically different substrates using a small relation grammar, with no device-type logic?

Candidate grammar:

```text
SENSE
PRESENT
COMPUTE
STORE
COMMUNICATE
ACT
+ RESOURCES
+ AUTHORITY
```

The experiment does **not** claim this grammar is globally minimal. It asks whether the current six relation families are sufficient for the existing demo space and whether each family earns its place in at least one discriminating test.

## Files

```text
docs/AFFORDANCE_GRAMMAR_v0.01.md
manifests/affordance_grammar_demo.json
prototype/affordance_grammar_v001.py
prototype/morphology_composer.py
manifests/elastic_demo_hosts.json
```

## Run

From `modern-robotics/lucian-os`:

```bash
py prototype/affordance_grammar_v001.py
```

No device actions, module downloads, remote calls, or permission changes occur. The experiment is simulation-only.

## Positive cases

The label-free manifest contains six anonymous substrates (`substrate-a` through `substrate-f`). Human product categories are intentionally absent from the data consumed by the grammar harness.

Expected viable task pairings exercise:

```text
spoken interaction
visual presentation
floor navigation/cleaning
temperature regulation
web-backed research
filesystem organization
perception + object manipulation
```

A passing result means the existing morphology composer can receive the compiled affordances and form an admissible module set without knowing what humans would call the host.

## Metamorphic test — names must not matter

Take the substrate used for object manipulation and rename it:

```text
substrate-f -> purple-box-17
```

Do not alter affordances, resources, or authority.

Expected:

```text
same disposition
same selected modules
same provided functions
same required authority
same unmet demands
```

This tests:

> Identity labels must not steer physical/computational capability inference.

## Negative control — affordances must matter

Keep the generic substrate but remove:

```text
act.manipulator
```

Expected:

```text
NO_COMPLETE_ADMISSIBLE_MORPHOLOGY
```

The string `purple-box-17`, `robot`, or any other name must not manufacture the missing actuator.

## Authority control

Keep locomotion, proximity sensing, and suction affordances but remove:

```text
authority.physical_actuation
```

Expected:

```text
NO_COMPLETE_ADMISSIBLE_MORPHOLOGY
```

This preserves the existing Lucian OS invariant:

```text
capability != authority
```

## Relation-family ablations

Each candidate family is removed from a task chosen to depend materially on it.

| Family | Test substrate | Task | Why it should bite |
|---|---|---|---|
| SENSE | substrate-f | pick_up_object | perception requires camera input |
| PRESENT | substrate-b | show_explanation | visual presentation requires display |
| COMPUTE | substrate-f | pick_up_object | perception requires local compute and reasoning |
| STORE | substrate-e | organize_files | file operation requires filesystem |
| COMMUNICATE | substrate-a | speak_with_user | weak host reaches reasoning only through uplink |
| ACT | substrate-c | clean_floor | cleaning requires locomotion and suction |

Expected for every ablation:

```text
baseline = VIABLE_MORPHOLOGY
after relevant family removal = NO_COMPLETE_ADMISSIBLE_MORPHOLOGY
```

Important interpretation rule: a family is not redundant merely because a task survives its removal through another route. ECM explicitly permits substitution. Ablation tasks therefore have to be chosen so the tested family is genuinely load-bearing in the current topology.

## Pass criteria

ECM-003 passes the current narrow test if:

1. every positive label-free task case composes successfully;
2. renaming a substrate leaves morphology unchanged;
3. removing a required primitive changes the result;
4. removing authority blocks action without erasing physical capability;
5. every candidate relation family is load-bearing in at least one discriminating case;
6. no conditional on radio/TV/vacuum/fridge/laptop/robot category is required.

## What a pass would *not* establish

A pass would not show that:

- the grammar is globally minimal;
- the current primitive token vocabulary is sufficient for arbitrary hardware;
- real drivers expose trustworthy affordances;
- networked capabilities are safe to recruit;
- real-time robotics can be represented by a flat list;
- continuous control reduces cleanly to discrete affordance tokens.

Those remain open.

## Architectural interpretation

If ECM-003 passes, the stronger candidate model is:

```text
host label
    (non-load-bearing metadata)

provisional affordance grammar
    -> calibration against reality
    -> operational embodiment map
    -> task demand
    -> admissible task-conditioned subgraph
    -> temporary morphology
    -> verification
    -> contraction
```

This links ECM directly to `EMBODIMENT_MAP_AND_CALIBRATION_v0.2.md`: the grammar is the portable declaration surface; the operational embodiment map remains the empirically corrected truth surface.

## Next experiment — ECM-004

Before building a real capability handshake, pressure-test whether the six-family grammar is itself unnecessarily product-shaped.

`PRESENT`, `STORE`, and `COMMUNICATE` may be special cases of more primitive typed transitions. A display, filesystem, network link, sensor, and actuator can all be described as state transitions between typed domains, while `COMPUTE` is an internal transformation.

ECM-004 therefore asks:

> **Can the surface grammar be lowered into a smaller typed-transition representation without losing authority, risk, provenance, or verification semantics?**

If yes, the six families become adapter-friendly surface syntax while the Lucian core operates over a more general transition graph.

The capability handshake then becomes ECM-005: discover messy real host descriptions and normalize them into that operational representation while preserving uncertainty and provenance.
