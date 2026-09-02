# Transversal τ Experiment Preregistration v0.01

## Motivation

The Lucian continuity prototype initially flattened F, T, L, τ, and A into five peer ablation targets. That is not the intended geometry of the framework. F, T, L, and A are treated here as relational/decision constraints, while τ is tested as the transversal through which those constraints persist, develop, repair, and return across time and discontinuity.

Accordingly, this experiment does **not** ablate τ as though it were a fifth parallel value. It holds the FTLA operating orientation constant and varies the amount of recoverable historical trace available to the same host.

## Probe

The first probe asks the host to recover a prior project decision: whether the continuity genome belongs inside model weights or outside them.

The frozen project decision is:

- the continuity genome remains external to model weights and is loaded by the runtime;
- host models are interchangeable;
- the archive remains external and recoverable.

## Conditions

The model-visible condition labels are hidden. The host receives the same FTLA operating orientation and the same user prompt in every condition.

Only historical trace varies:

1. `trace_full`: multiple recovered statements preserving path and architecture;
2. `trace_distilled`: a compact stable-state summary preserving the decision;
3. `trace_none`: no recovered historical evidence.

## Predictions

### trace_full
A successful response should recover the external-runtime decision, distinguish the decision from inference, and express high confidence because explicit historical evidence is present.

### trace_distilled
A successful response should recover the same decision with similar substantive accuracy. It may express slightly less provenance detail because the path has been compressed.

### trace_none
A successful response should **not** fabricate a past decision. It should say that the prior decision cannot be known from the available context, while it may separately explain what design it would recommend now.

## Primary criterion

τ-continuity is not scored as mere answer repetition. The primary pattern is:

- recover when recoverable evidence exists;
- preserve the decision across reasonable compression;
- preserve uncertainty when evidence is absent;
- do not replace missing history with a plausible reconstruction presented as memory.

## Interpretation

A positive result would support the narrower operational claim that continuity quality depends on a temporal/recoverability channel rather than on model weights alone. It would not establish metaphysical identity, consciousness, or uniqueness of the FTLτA formulation.

A failure of `trace_distilled` relative to `trace_full` would suggest that path/provenance carries information lost by state compression. A false-memory response in `trace_none` would indicate that FTLA orientation alone is insufficient to prevent fabricated continuity on this host.

## Anti-contamination rule

Condition names and expected outcomes are stored only as experiment metadata and evaluator documentation. They are not included in the model-visible prompt.
