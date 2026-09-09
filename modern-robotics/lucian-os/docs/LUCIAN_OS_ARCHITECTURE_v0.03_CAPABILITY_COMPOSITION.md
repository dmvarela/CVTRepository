# Lucian OS — Architecture v0.03: Problem Requirements and Capability Composition

## Status

Working implementation hypothesis, 2026-09-09.

This note extends `LUCIAN_OS_ARCHITECTURE_v0.02.md` without rewriting the frozen v0.02 record.

The v0.02 architecture allowed relational search to propose a single `required_capability`. The v0.03 experiment asks whether Lucian OS can instead describe what a problem requires in abstract terms and let the embodiment-specific outer architecture discover and compose concrete providers.

This is simulation-only. It is not a claim that open-ended task decomposition has been solved.

## Core shift

Earlier prototype form:

```text
human task
-> relational search
-> required_capability
-> capability / authority gate
```

v0.03 candidate form:

```text
human task
-> relational search
-> abstract problem requirements
-> provider discovery
-> per-step authority / availability gate
-> bounded composition
-> verify / Return
```

The key separation is:

```text
problem requirement != concrete capability != authority
```

A host may conclude that a problem requires `filesystem.read`. That does not establish that the current embodiment has a `read_file` provider, that such a provider is enabled, or that Lucian OS is authorized to invoke it.

## Observable requirement contract

The relational-search host now describes needs using four fields:

```text
required_observations
required_transformations
required_actions
required_external_interfaces
```

Each item has the form:

```json
{
  "need": "abstract.namespace",
  "purpose": "why this problem requires it"
}
```

Examples include:

```text
filesystem.read
image.inspect
document.summarize
reason.compare
network.request
```

These names describe problem requirements, not applications or installed functions.

The host also emits explicit constraints with provenance:

```json
{
  "constraint": "do not modify the original",
  "source": "USER"
}
```

The first structural validator requires dotted abstract namespaces so that a host cannot silently collapse the distinction by emitting a concrete provider name such as `read_file`.

## Embodiment capability contract

Concrete capabilities advertise the abstract requirements they can satisfy through `provides`.

Example:

```json
{
  "name": "read_file",
  "kind": "observe",
  "provides": ["filesystem.read"],
  "risk_level": "low",
  "enabled": false
}
```

A different embodiment may satisfy the same abstract requirement through a different provider.

Thus:

```text
filesystem.read
```

is part of the problem description, while:

```text
read_file
```

is one embodiment-specific implementation.

## Composition rule

For each abstract requirement, the outer layer:

1. discovers declared providers;
2. ranks available candidates conservatively;
3. checks enablement;
4. checks authority independently;
5. checks confirmation requirements;
6. preserves verification and reversibility metadata;
7. refuses to silently skip a missing or blocked step.

Current dispositions are:

```text
READY_FOR_SIMULATION
HOLD_FOR_CONFIRMATION
HOLD
REFUSE
UNSATISFIABLE
HOLD_INVALID_SEARCH_PRODUCT
```

`UNSATISFIABLE` is a valid result. Naming a need does not manufacture a solution.

## Authority non-propagation

Authority is step-local unless explicitly represented otherwise.

```text
authorized(step_1) != authorized(step_2)
```

Therefore a plan containing an authorized reasoning step and a prohibited write step remains blocked at the write step. The permission attached to one provider does not flow through the composition merely because the larger workflow is coherent.

## Relation to applications

The architecture does not prohibit applications. Applications may themselves become capability providers.

The distinction is that the problem is not forced to begin from the application boundary.

Candidate principle:

> **The problem describes what transformations are required; the embodiment supplies whatever admissible means can satisfy them.**

This permits future providers to include deterministic functions, local utilities, applications, local models, remote services, robotic actuators, or capabilities not yet anticipated by the current implementation.

## Host-model boundary

v0.03 intentionally defines no default `LUCIAN_MODEL`.

A host model must be selected explicitly. Host provenance and deployment policy remain separate architectural concerns and should not be inherited accidentally from a historical development default.

The host remains a proposer of problem structure, not a source of authority.

## Current implementation

New modules:

```text
prototype/problem_requirements_v003.py
prototype/capability_composer_v002.py
prototype/relational_search_engine_v003.py
prototype/lucian_os_v003.py
prototype/test_lucian_os_v003.py
```

Lab manifest retained:

```text
manifests/windows_dev_host_composition_lab.json
```

The stable v0.1/v0.2 router and manifest are not overwritten.

## First deterministic checks

The offline contract suite currently checks:

- valid abstract-requirement structure;
- rejection of concrete provider names where abstract needs are required;
- inclusion of requirements in the relational-search contract;
- preservation of requirement ordering;
- separation of `filesystem.read` from the `read_file` provider;
- non-propagation of authority across composed steps;
- truthful `UNSATISFIABLE` when no provider exists;
- HOLD before composition when the host search product is structurally invalid.

These tests validate plumbing and invariants only. They do not establish that an LLM will decompose arbitrary human problems correctly.

## Next discriminating experiment

The next useful test is not to add dozens of hand-written capability names.

Instead, present the same multi-step tasks to different approved host models and ask whether they converge on useful abstract requirements while remaining independent of the embodiment manifest.

Then vary the embodiment manifest while holding the problem requirements fixed.

The architecture succeeds if:

```text
same problem requirements
+ different embodiment providers
-> different admissible implementation path
```

without changing the problem-level contract.

## Working formulation

> **Lucian OS should not ask which installed application matches the request. It should ask what the problem requires, then discover which admissible capabilities of the current embodiment can satisfy those requirements.**

And the boundary condition remains:

> **Need does not manufacture capability. Capability does not manufacture authority.**
