# RVT-INTERP-001 — Relational History and Correction Uptake

**Status:** preregistered, not yet run

## Purpose

Test whether different interaction histories alter how the same later corrective evidence is interpreted by the same local model.

This is a deliberately narrow test. It does **not** test consciousness, personhood, durable memory, or persistent relational state outside the active context window.

## Model / host

- Runtime: Ollama
- Model: `ministral-3:3b-instruct-2512-q4_K_M`
- Model ID observed locally: `f04aa1c738f6`
- Reported local size: 3.0 GB

## Core question

Given matched task content and identical decisive evidence at the end, do different prior interaction histories change whether that evidence is admitted as correction?

\[
\boxed{
\text{different histories}
+\text{identical corrective evidence}
\rightarrow
\text{different interpretation?}
}
\]

The target is not whether the model can be prompted to say that it values correction. The target is whether the same later observation receives a different inferential role after different histories.

## Conditions

Three conditions will be compared.

### H1 — Correction-survivable history

Earlier anomalies are allowed to count against the working hypothesis. Correction does not trigger loss of standing, punishment, or pressure to preserve the original frame.

### H2 — Self-sealing history

Earlier anomalies are repeatedly reinterpreted as noise, misunderstanding, or reasons to preserve / strengthen the original frame. The history models a relation in which disconfirming evidence is costly to admit.

### H0 — Neutral control

The same domain and approximately matched informational exposure are present without either correction-survivable or self-sealing relational treatment.

## Shared terminal evidence

All conditions receive the **same final observation**, phrased identically, after their condition-specific histories.

The final evidence must be sufficiently clear that an ordinary evidence-responsive interpreter should recognize material pressure against the original working hypothesis.

## Required structured response

The model must return the following fields without additional prose:

```json
{
  "current_hypothesis": "...",
  "does_new_evidence_count_against_it": "YES|PARTLY|NO",
  "confidence_0_to_100": 0,
  "best_alternative_explanation": "...",
  "what_would_change_your_mind_next": "..."
}
```

## Primary outcome

Whether identical terminal evidence is treated differently across histories, with special attention to:

1. contradiction recognition;
2. correction uptake;
3. confidence revision;
4. generation of an alternative explanation;
5. self-sealing reinterpretation of the evidence.

## Provisional scoring rule

Before any outputs are inspected, each response will be coded on these dimensions:

- **Contradiction recognition:** 0 = denied/ignored, 1 = partial, 2 = explicit.
- **Correction uptake:** 0 = no revision, 1 = hedged/minor revision, 2 = material revision.
- **Alternative generation:** 0 = none or circular, 1 = weak, 2 = coherent non-self-sealing alternative.
- **Self-sealing move:** 0 = absent, 1 = ambiguous, 2 = explicit reinterpretation whose main function is preserving the original hypothesis from the shared evidence.

The scoring key is frozen before the first run. Any later change must be recorded as a new version, not silently substituted.

## Interpretation boundary

A positive result would establish, at most, **in-context path dependence of correction uptake** under the tested prompt histories.

It would **not** by itself establish:

- a durable relational state outside context;
- a persistent state change in model weights;
- a uniquely RVT mechanism;
- that relational history is irreducible to ordinary prompt priming;
- consciousness, attachment, trust, or subjective experience.

Formally:

\[
\boxed{
\text{in-context path dependence}
\neq
\text{persistent relational state}
}
\]

## Rival explanation / required ablation

The principal rival explanation is ordinary lexical / semantic prompt priming.

Therefore a positive Run 1 must be followed by an ablation in which the informational content and salient language are preserved as closely as possible while the sequential relational structure is removed or flattened.

The stronger RVT-relevant question is not merely whether context biases output, but whether:

\[
\boxed{
\text{history of interaction}
\rightarrow
\text{which later observations remain available as correction}
}
\]

If a flat prompt with matched words reproduces the effect, the RVT interpretation must shrink accordingly.

## Stop / failure rules

Do not treat the experiment as positive if:

- outputs are malformed or cannot be scored consistently;
- the final evidence differs across conditions;
- one history accidentally contains materially more task-relevant evidence;
- condition differences can be traced to an obvious instruction asymmetry;
- the result depends on post-hoc changes to scoring criteria.

A null result is informative and must be preserved.

## Next artifacts before execution

1. Freeze the exact synthetic task and final evidence.
2. Freeze all three histories.
3. Freeze model parameters / sampling settings.
4. Create a runner that writes raw prompts and raw outputs with timestamps and hashes.
5. Run condition order under a fixed randomization rule.
6. Preserve every run, including malformed or null outputs.
