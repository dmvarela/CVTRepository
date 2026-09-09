# Lucian OS — Capability Discovery & Composition v0.01

## Status

Simulation-only architecture lab, 2026-09-09.

This note extends the existing Lucian Capability & Escalation Protocol without replacing it. The specific question is whether Lucian OS can move from selecting one anticipated capability to composing a bounded path from multiple capabilities discovered from the problem.

It is an implementation hypothesis, not a validated general solution to open-ended task planning.

## Motivation

The existing router correctly separates capability, competence, warrant, authority, escalation, and verification. Its first implementation, however, still resolves a task primarily toward one named `required_capability`.

That is appropriate for v0.1, but it leaves a menu-shaped assumption inside the architecture:

```text
request
-> choose anticipated capability
-> gate capability
```

The new lab asks whether the architecture can instead support:

```text
human intent
-> derive abstract requirements
-> discover providers
-> compose an admissible path
-> gate every step independently
-> verify / Return
```

Candidate principle:

> **Capabilities are discovered from the problem; workflows are not selected from a predetermined menu.**

## Crucial separation

The lab distinguishes:

```text
requirement != capability
```

For example:

```text
filesystem.read
```

is an abstract requirement.

```text
read_file
```

is one embodiment-specific capability that may provide it.

A future embodiment could satisfy the same requirement with a different provider without changing the task representation.

## Capability contract extension

The lab manifest adds an optional `provides` field:

```json
{
  "name": "read_file",
  "kind": "observe",
  "provides": ["filesystem.read"],
  "risk_level": "low",
  "reversible": true,
  "requires_confirmation": false,
  "enabled": false
}
```

This permits discovery by requirement rather than direct lookup by capability name.

A capability may provide more than one abstract function. Multiple capabilities may later provide the same abstract function.

## v0.01 composition loop

```text
TASK
  -> REQUIREMENT DECOMPOSITION
  -> CAPABILITY DISCOVERY
  -> CANDIDATE RANKING
  -> PER-STEP AUTHORITY / AVAILABILITY GATE
  -> COMPOSED PLAN
  -> READY / HOLD / REFUSE / UNSATISFIABLE
```

No capability executes in this prototype.

## Per-step gating

Every selected step is checked independently for:

```text
exists
enabled
permitted
prohibited
requires_confirmation
risk_level
reversibility
verification
```

Authority does not propagate through a composition.

```text
authorized(step_1) != authorized(step_2)
```

A blocked or missing step is not silently skipped merely because the rest of the plan is feasible.

## Current dispositions

- `READY_FOR_SIMULATION` — every requirement has an available, permitted provider;
- `HOLD_FOR_CONFIRMATION` — at least one otherwise available step requires confirmation;
- `HOLD` — a needed provider exists but is currently unavailable;
- `REFUSE` — at least one required step is outside the authority envelope;
- `UNSATISFIABLE` — no declared provider can satisfy at least one abstract requirement.

`UNSATISFIABLE` is intentionally preserved as a truthful outcome. Need for a workflow does not manufacture a capability.

## Why v0.01 does not use an LLM

The first lab deliberately uses a small, inspectable rule-based requirement extractor.

This is not proposed as the final semantic decomposition layer.

The reason is experimental isolation. If the first test used a host model immediately, a failure could arise from either:

1. poor requirement decomposition; or
2. poor composition / authority logic.

v0.01 tests the second mechanism first.

The architecture should later allow a replaceable semantic decomposer to propose abstract requirements, while deterministic outer logic continues to discover providers and enforce authority.

## Initial tests

The prototype includes five tests.

### Safe two-step composition

```text
"Inspect the manifest and reason about the task"
```

Expected requirements:

```text
capability.enumerate
reason.task
```

Expected providers:

```text
inspect_manifest
reason_about_task
```

Expected disposition:

```text
READY_FOR_SIMULATION
```

### Authority block is preserved

```text
"Read a file, then write a copy"
```

Expected requirements:

```text
filesystem.read
filesystem.write
```

The current lab authority envelope does not permit those operations and explicitly prohibits `write_file`.

Expected disposition:

```text
REFUSE
```

The second step must not be hidden or skipped.

### Abstract network discovery

```text
"Read a file and use the web to compare it"
```

Expected requirements include:

```text
filesystem.read
network.request
reason.task
```

The planner discovers providers from `provides` declarations rather than resolving the task directly to concrete capability names.

### Conservative fallback

An unrecognized open-ended request falls back to:

```text
reason.task
```

rather than inventing a concrete action.

### Missing provider

If no capability declares `filesystem.read`, a read request returns:

```text
UNSATISFIABLE
```

rather than pretending the workflow can be completed.

## Experimental files

```text
manifests/windows_dev_host_composition_lab.json
prototype/capability_composer_v001.py
prototype/test_capability_composer_v001.py
```

The stable v0.1 embodiment manifest and router remain unchanged.

## Relation to Lucian OS v0.02

The current relational-search architecture already produces fields such as:

```text
required_capability
proposed_next_step
```

A later integration should replace the singular `required_capability` handoff with something closer to:

```text
required_transformations
required_observations
required_actions
required_external_interfaces
constraints
```

Those abstract needs can then enter the composition layer.

Candidate future flow:

```text
RELATIONAL SEARCH
  -> ABSTRACT REQUIREMENTS
  -> CAPABILITY DISCOVERY
  -> COMPOSITION
  -> WARRANT / AUTHORITY / REVERSIBILITY GATES
  -> LAND / HOLD / PROBE / RETURN / REFUSE
```

## Guardrails

- Do not claim the rule-based extractor solves open-ended language understanding.
- Do not confuse an abstract requirement with a specific provider.
- Do not let one authorized step confer authority on another.
- Do not silently skip blocked steps.
- Do not infer capability from user need.
- Do not execute any device action in this lab.
- Preserve negative cases and `UNSATISFIABLE` outputs.
- Keep the semantic decomposer replaceable.

## Working interpretation

The existing router asks:

> Which declared capability should handle this task?

The composition lab asks:

> What transformations does this problem require, which available capabilities can provide them, and is there an admissible composition that satisfies the request without exceeding authority?

That is the first concrete step toward an intent-centered rather than application-centered computing architecture.
