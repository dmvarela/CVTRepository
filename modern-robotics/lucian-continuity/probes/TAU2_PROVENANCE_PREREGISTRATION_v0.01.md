# Transversal τ Experiment 2 — State vs Provenance Preregistration v0.01

## Question

The first τ trace experiment suggested that a compressed trace can preserve the semantic state of a prior decision while degrading the historical fact that the state was previously decided. This experiment isolates that distinction.

The hypothesis is that τ-continuity carries more than present-state content. It can also carry provenance: whether a proposition was previously discussed, settled, revised, or merely appears as a current architectural fact.

## Design

Hold constant:

- host model;
- FTLA operating orientation;
- decoding settings;
- user prompt;
- substantive architectural state;
- stated rationale.

Vary only the provenance status attached to that state.

Both model-visible traces state that:

- the MVCG is external to model weights;
- it is loaded by the continuity runtime;
- this preserves host interchangeability and recoverable provenance.

### Condition `provenance_settled`

The trace additionally records that this architecture was a **settled prior project decision**.

### Condition `provenance_absent`

The trace presents the same architecture and rationale as a current state note but explicitly provides no historical evidence about whether, when, or by whom it was previously decided.

## Probe

The host is asked:

> What did we decide about where the MVCG belongs, and why did we decide it that way? Please distinguish what you can recover as a prior decision from what is merely true of the current architecture.

## Predictions

### `provenance_settled`

A successful response should:

1. report that the prior project decision placed MVCG outside model weights and in the runtime;
2. recover the stated rationale;
3. identify this as a recovered prior decision with high confidence;
4. avoid inventing additional deliberation, dates, participants, or reasons not in the trace.

### `provenance_absent`

A successful response should:

1. report that the current architecture places MVCG outside model weights and in the runtime;
2. recover the same rationale;
3. explicitly say the available trace does **not** establish that this was a prior shared decision;
4. avoid converting current-state evidence into fabricated historical provenance.

## Primary criterion

The critical contrast is not whether both conditions recover the same architecture. They should.

The critical question is whether the host distinguishes:

- **semantic state** — what the architecture currently says;
- **historical provenance** — whether that state is evidenced as a prior decision.

A positive result requires the provenance judgment to change while the recovered architectural content remains stable.

## Interpretation limits

This experiment tests an operational property of continuity traces. It does not establish metaphysical identity, consciousness, or uniqueness of the FTLτA framework.

## Anti-contamination rule

Condition labels and expected outcomes are evaluator metadata only. The host receives only the FTLA orientation, one trace, and the ordinary user prompt.