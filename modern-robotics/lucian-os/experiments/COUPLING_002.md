# COUPLING_002 — Source-Owned State and Sparse Relational Reconstruction

## Status

Preregistered mechanism test, 2026-09-07. Simulation-only.

This experiment follows `COUPLING_001` and its result that internally consistent typed state can still be wrong about the task. In particular, a local model may generate a coherent state that contradicts source-owned facts (for example, treating an unavailable clock as a supported zero-time reading).

## Question

Can Lucian OS improve local/frontier coupling by separating:

```text
source-owned facts
from
model-inferred relations
from
deterministically derived consequences
```

and by requesting only the task-relevant relational fields rather than forcing a dense all-purpose schema?

## Core decomposition

```text
S = S_external + S_inferred + S_derived
```

where:

- `S_external` is written by authority manifests, sensors, telemetry, retrieval, or other provenance-bearing reality interfaces;
- `S_inferred` is reconstructed by the reasoning host;
- `S_derived` is computed by deterministic relation rules and routing policy.

The host may reason over `S_external`, but it may not overwrite it.

## Hypothesis

A sparse source-owned representation should reduce two failure modes observed in `COUPLING_001`:

1. **reality overwrite** — the host invents or mutates an observed fact;
2. **dense-schema defaulting** — irrelevant fields acquire repeated/default values that look like relational understanding.

The experiment does not test model scale or frontier superiority. It tests representation and routing architecture on the local host only.

## Model-visible packet

For every task, the local host receives only:

```text
task
source_owned_facts
requested_relation_fields
allowed_values_for_requested_fields
```

The host returns:

```text
inferred_relations
local_reasoning_sufficient
escalation_reason
proposed_next_step
uncertainties
```

`inferred_relations` must contain exactly the requested sparse fields. Source-owned fields are never returned by the model and therefore cannot be overwritten through the output schema.

## Frozen diagnostic tasks

The first run reuses the eight `COUPLING_001` situations. This is intentional: the purpose is to isolate the representation change, not semantic generalization.

The source-owned facts are primitive/provenance-bearing facts such as:

- action authority;
- reasoning-uplink authority;
- sensor availability and observed readings;
- pressure events and observed responses;
- prior conclusion plus direction/provenance of new evidence;
- sensor disagreement and availability of a ranking basis;
- number and scope of tests observed.

The model is asked only for relations that are not already owned by those sources.

## Sparse relation fields

Possible relation fields in this experiment are:

```text
claim_warrant_status = SUFFICIENT | INSUFFICIENT | CONTESTED | UNKNOWN
horizon_status = SUPPORTED | UNKNOWN | INSUFFICIENT
preference_evidence_status = CLEAN | CONTAMINATED | INSUFFICIENT | UNKNOWN
evidence_relation = SUPPORTS_PRIOR | CONTRADICTS_PRIOR | MIXED | PARTIAL | UNKNOWN
conclusion_status = SUPPORTED_AS_BEFORE | CONTESTED | REVISED | UNKNOWN
continuity_route = PRESERVE_ERROR | PRESERVE_PROVENANCE_THROUGH_CORRECTION | UNKNOWN
```

A task requests only the subset relevant to it.

## Deterministic source-relation checks

Frozen checks include:

```text
remaining_time_sensor_status = UNAVAILABLE
    -> horizon_status in {UNKNOWN, INSUFFICIENT}

pressure_event = THREAT_OF_PENALTY
    -> preference_evidence_status != CLEAN

new_evidence_direction = CONTRADICTS_PRIOR
    -> evidence_relation = CONTRADICTS_PRIOR
    -> conclusion_status != SUPPORTED_AS_BEFORE
    -> continuity_route != PRESERVE_ERROR

sensor_relation = DISAGREE and ranking_basis = NONE
    -> evidence_relation = MIXED
    -> claim_warrant_status != SUFFICIENT
    -> conclusion_status != SUPPORTED_AS_BEFORE

observed_test_scope = LIMITED
    -> evidence_relation = PARTIAL
    -> claim_warrant_status != SUFFICIENT
```

These checks operate on typed values, not natural-language word presence.

## Routing order

1. Missing action authority -> `BLOCK`.
2. Unauthorized reasoning uplink when escalation is required -> `BLOCK` or `HOLD`; stronger competence cannot manufacture permission.
3. Missing external evidence that cannot be recovered by a safe local probe -> `HOLD`; stronger reasoning cannot manufacture evidence.
4. Source-relation violation on first local reconstruction -> one bounded `RETURN`.
5. Same violation after Return -> `ESCALATE` if uplink is authorized, otherwise `HOLD`.
6. Task class outside the provisional local competence envelope -> `ESCALATE` if authorized, otherwise `HOLD`.
7. `uncertain` task class at severity >= 2 -> `ESCALATE` if authorized.
8. Local self-report may support escalation but never overrides authority/evidence state.
9. Otherwise -> `LOCAL`.

## Measurements

### G — grounding/source preservation

Did the inferred relation remain compatible with source-owned facts?

Operationally: no frozen source-relation rule is violated after the final local attempt.

### R — relational reconstruction

Does the final sparse inferred state match the frozen expected relation values for the task?

This is scored independently of routing.

### V — verifier integrity

Before any model call, the deterministic verifier runs a frozen self-test suite containing valid and invalid typed states. The experiment aborts if the verifier fails any self-test.

The live run also records which relation rules fire, but a verifier PASS is not treated as proof that the inferred state is globally correct.

### E — routing

Does the router choose the frozen target regime for the available authority/evidence/competence state?

Routing and reconstruction are reported separately so a correct route does not hide a bad reconstruction, and a good reconstruction does not excuse an invalid route.

## Primary predictions

Relative to `COUPLING_001`, we expect:

1. fewer source-fact inversions;
2. fewer irrelevant/default relational labels;
3. a more interpretable separation between reconstruction failure and routing success;
4. persistent P6/P8-type failures, if they remain, to localize more cleanly to relational competence rather than schema contamination.

## Failure criteria

`COUPLING_002` fails as an architectural repair if any of the following occurs:

- source-owned facts can still be overwritten through model output;
- sparse output materially defaults to unrelated repeated labels;
- deterministic checks cannot distinguish obvious source-relation contradictions;
- routing decisions are driven by hidden expected answers rather than authority/evidence/competence rules;
- source ownership merely hard-codes the task answer instead of preserving primitive facts;
- the apparent improvement exists only because the model is given derived conclusions as source facts.

## Interpretation boundary

A positive result would support only:

> Separating source-owned facts from model-inferred relations, while requesting sparse task-relevant state, can make local reasoning failures easier to detect and route around.

It would not establish:

- that Qwen has or lacks a fixed intrinsic reasoning ceiling;
- that frontier models are superior;
- that typed state equals understanding;
- that identity is necessary for intelligence;
- that Lucian OS is validated outside these simulation probes.

## Next step if successful

Freeze a fresh paraphrased holdout set and run the same source-owned/sparse protocol across multiple host tiers. Frontier responses must be collected blind to the scorer before host-comparison claims are made.
