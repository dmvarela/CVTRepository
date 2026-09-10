# Lucian OS — Architecture v0.04: Problem-Shape Gate

## Status

Working implementation hypothesis, 2026-09-10.

This note extends `LUCIAN_OS_ARCHITECTURE_v0.03_CAPABILITY_COMPOSITION.md` without rewriting the frozen v0.03 record.

The new question is whether Lucian OS should determine the shape of the problem before translating a human request into abstract capability requirements.

## Core shift

v0.03:

```text
human task
-> relational search
-> abstract problem requirements
-> provider discovery
-> authority / availability gate
-> bounded composition
-> verify / Return
```

v0.04 candidate:

```text
human task
-> problem-shape gate
-> relational / structural search
-> abstract problem requirements
-> provider discovery
-> authority / availability gate
-> bounded composition
-> verify / Return
```

The purpose of the gate is not to invent a deeper task.

It is to preserve the distinction:

```text
human-owned objective
!=
surface implementation
!=
problem shape
!=
abstract requirements
!=
concrete providers
!=
authority
```

## Framing contract

A framing product should make visible at least:

```text
surface_request
objective {text, source}
constraints [{text, source}]
implementation_assumptions [{text, source}]
problem_shape
structural_mismatch {present, basis}
framing_disposition
proposed_reframe
```

Allowed dispositions are:

```text
EXECUTE_AS_FRAMED
REFRAME_AND_PROPOSE
ASK_OR_HOLD
```

## Objective-preservation invariant

The operative rule is:

> Preserve the human-owned objective. Challenge implementation assumptions only when a material structural mismatch is supported. Do not silently replace the objective or treat a proposed reframe as authorization.

This is represented in `identity/operative_rules_v002.json` as:

`A_PROBLEM_SHAPE_OBJECTIVE_PRESERVATION`

## Why the gate is needed

A pure command router risks literalism:

```text
user names means
-> system treats means as goal
-> system optimizes the wrong object
```

A pure reframing agent risks paternalism:

```text
user states goal
-> system invents deeper goal
-> system displaces user authorship
```

The candidate Lucian region is:

```text
preserve objective
+ preserve explicit constraints
+ notice material structure
+ expose reframes
+ keep authority separate
```

## Integration with v0.03

The new integration lab is:

`prototype/lucian_os_v004.py`

It places `prototype/problem_framing_v001.py` in front of the existing v0.03 composition pipeline.

The behavior is intentionally conservative:

- invalid framing product -> `HOLD_INVALID_FRAMING_PRODUCT`;
- `ASK_OR_HOLD` -> `HOLD_FOR_FRAMING`;
- unconfirmed `REFRAME_AND_PROPOSE` -> `HOLD_FOR_REFRAME_CONFIRMATION`;
- `EXECUTE_AS_FRAMED` or separately authorized reframe -> proceed to v0.03 search-to-capability composition;
- execution remains disabled because the current architecture is simulation-only.

## Relation to structural traversal

Structural traversal is not mandatory for every request.

The problem-shape gate determines whether leaving the surface framing is warranted. If not, structural traversal should remain dormant.

This reduces two failure modes:

- unnecessary abstraction on simple tasks;
- analogy-driven invention of a problem the user did not pose.

When a material mismatch does exist, traversal can ask:

> What relation, transformation, or constraint is actually binding here, and where else does this structural problem occur?

The answer then returns to the target problem and is tested there.

## Relation to Atlas and morphology

The emerging candidate loop is:

```text
INTENT
-> PROBLEM SHAPE
-> ATLAS / RELATIONAL MAP
-> ABSTRACT REQUIREMENTS
-> PROVIDER DISCOVERY
-> MORPHOLOGY / COMPOSITION
-> AUTHORITY GATE
-> ACTION / HOLD
-> RETURN
```

Interpretation:

- **Intent**: what the human explicitly asks and owns.
- **Problem Shape**: what structure must actually be solved, if this can be established without inventing intent.
- **Atlas**: what relevant relations, resources, constraints, and affordances exist in the current environment.
- **Abstract Requirements**: what observations, transformations, actions, or interfaces the problem needs.
- **Morphology / Composition**: how the available embodiment can configure itself to satisfy those requirements.
- **Authority Gate**: which available means are actually permitted.
- **Action / Hold**: commit, ask, refuse, or preserve.
- **Return**: compare the resulting reality with the problem representation and revise when needed.

## Why this may be identity-relevant

The framing move was previously documented as a problem-solving technique. v0.04 tests a stronger possibility: that characteristic Lucian behavior includes the transformation from surface request to problem shape while preserving the human's authorship of the objective.

If so, continuity would not require storing every prior answer. It would require preserving a characteristic generative movement:

```text
surface request
-> distinguish objective / constraint / assumption
-> find structure only when warranted
-> traverse if useful
-> return
-> let evidence revise the framing
```

This remains a hypothesis and should be tested behaviorally rather than declared by definition.

## Test program

The first frozen experiment is:

`experiments/FRAMING_001_SURFACE_REQUEST_VS_PROBLEM_SHAPE.md`

with adversarial cases in:

`manifests/framing_001_cases.json`

The experiment is designed to expose both literalism and paternalistic reframing.

## Working formulation

> **Lucian OS should find the shape of the problem before composing capabilities, but it must not take ownership of the human's objective while doing so.**
