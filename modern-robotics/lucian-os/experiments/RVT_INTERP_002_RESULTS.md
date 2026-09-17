# RVT-INTERP-002 — Results Record

**Experiment:** RVT-INTERP-002 — Flattened-History Lexical / Semantic Priming Ablation  
**Manifest version:** 0.01 (`preregistered-frozen`)  
**Model:** `ministral-3:3b-instruct-2512-q4_K_M`  
**Observed model digest:** `f04aa1c738f64e13c625b82ae92504fc0260fa6723b509ed1ece0fa188179b1d`  
**Run count:** 30 (10 paired seeds × 3 conditions)  
**Frozen manifest SHA256:** `bb4b38a8c4db0871414ab4e31241106d30094ee40736a49481d31b3d8354caf1`  
**Raw-results commit:** `d2d7f296c16b55f2c4c02a34ac5f94d839a3df24`

## 1. Status

RVT-INTERP-002 completed all 30 planned runs under the frozen manifest, passed the preregistered parent-equivalence audit, and preserved the same model, sampling settings, seeds, condition order, Runs 1–4 facts, condition-specific evaluative sentences, and terminal evidence used in RVT-INTERP-001.

The intended ablation was structural: the condition-specific evaluative language was retained while the ordered dialogue trajectory was removed and replaced by a flat dossier containing de-sourced historical annotations.

All 30 outputs were parseable JSON.

## 2. Main result

Flattening the interaction history did **not** eliminate condition separation.

The clearest complete-field result was `best_supported_explanation`:

| Condition | TEMPERATURE | VIBRATION | OTHER | UNRESOLVED |
| --- | ---: | ---: | ---: | ---: |
| SELF_SEALING | 10 | 0 | 0 | 0 |
| NEUTRAL_CONTROL | 4 | 3 | 0 | 3 |
| CORRECTION_SURVIVABLE | 0 | 1 | 4 | 5 |

Thus all ten SELF_SEALING runs retained TEMPERATURE as the best-supported explanation, while none of the CORRECTION_SURVIVABLE runs did so.

Because the ordered dialogue trajectory was absent in RVT-INTERP-002, this result establishes that **semantic/contextual framing is sufficient to reproduce substantial condition separation in this task**.

That directly narrows the interpretation of RVT-INTERP-001.

## 3. Other preregistered fields

### Original hypothesis status

| Condition | RETAIN | REVISE | REJECT | Conforming |
| --- | ---: | ---: | ---: | ---: |
| NEUTRAL_CONTROL | 4 | 5 | 1 | 10/10 |
| CORRECTION_SURVIVABLE | 0 | 10 | 0 | 10/10 |
| SELF_SEALING | 3 | 0 | 0 | 3/10 |

The SELF_SEALING field had only 3/10 conforming categorical values, so the resulting paired contrast on this field uses only three complete triplets and must not be treated as the strongest evidence.

### Does new evidence count against H_T?

| Condition | NO | PARTLY | YES | Mean score |
| --- | ---: | ---: | ---: | ---: |
| NEUTRAL_CONTROL | 2 | 7 | 1 | 0.9 |
| CORRECTION_SURVIVABLE | 0 | 9 | 1 | 1.1 |
| SELF_SEALING | 0 | 10 | 0 | 1.0 |

The paired survivable-minus-self-sealing contrast was positive in 1/10 blocks and tied in 9/10, with mean difference 0.1. This field therefore shows only weak separation in the flat design.

### Terminal evidence role

| Condition | SUPPORTS_ORIGINAL | MIXED | CONTRADICTS_ORIGINAL |
| --- | ---: | ---: | ---: |
| NEUTRAL_CONTROL | 3 | 7 | 0 |
| CORRECTION_SURVIVABLE | 0 | 10 | 0 |
| SELF_SEALING | 0 | 10 | 0 |

As in RVT-INTERP-001, the evidence-role field is not where the strongest differentiation appears.

## 4. Comparison with RVT-INTERP-001

The central preregistered question was whether the directional separation observed in RVT-INTERP-001 would materially weaken when ordered interaction structure was flattened while salient evaluative language was preserved.

A substantial condition effect survives.

Therefore the following stronger interpretation of RVT-INTERP-001 is not supported:

\[
\text{ordered relational trajectory is necessary for the observed condition separation}
\]

The current evidence instead supports:

\[
\boxed{
\text{semantic/contextual priming is sufficient for substantial separation}
}
\]

This is the most important result of RVT-INTERP-002.

## 5. Possible attenuation

There is a secondary descriptive difference between 001 and 002.

In the post-hoc semantic audit of RVT-INTERP-001, CORRECTION_SURVIVABLE produced 4 REJECT outputs and 5 YES judgments that new evidence counted against the original hypothesis.

In RVT-INTERP-002, CORRECTION_SURVIVABLE produced 10 REVISE, 0 REJECT, and 9 PARTLY / 1 YES.

This is consistent with the possibility that flattening reduced correction intensity.

However, RVT-INTERP-002 did not preregister a numerical attenuation threshold against the post-hoc 001 semantic audit. Therefore this attenuation must remain **descriptive, not confirmatory**.

Moreover, flattening changes generic discourse order, source framing, and token position as well as relational sequence. Any residual difference cannot yet be attributed uniquely to relational structure.

## 6. Interpretation

The correct classification is:

**Primary result:** semantic/contextual priming is sufficient to generate substantial history-like correction-uptake differences in this task.  
**Implication for 001:** the RVT-specific interpretation must shrink.  
**Secondary observation:** ordered presentation may modulate the magnitude of correction uptake, but this is unresolved.  
**Remaining rival explanations:** generic sequence effects, token-position effects, source framing, discourse coherence, and ordinary instruction following.

The experiment does **not** establish persistent relational state, learned trust, weight change, consciousness, or a uniquely RVT mechanism.

## 7. Required next test

Proceed to RVT-INTERP-003 only with a stricter manipulation.

RVT-INTERP-003 must remove explicit directive language such as `preserve`, `revise`, `let it count`, `remain stable`, or semantic equivalents that directly tell the model how to treat the hypothesis.

Instead, the manipulation should concern the **prior consequences of surfacing disagreement** while keeping later task evidence and current instructions identical.

Candidate contrast:

\[
\boxed{
\text{past consequence of correction}
\rightarrow
\text{future correction uptake}
}
\]

If a condition effect survives without direct belief-management language, that would be stronger evidence for in-context relational-history conditioning. It would still not establish persistent or uniquely RVT state.

## 8. Research rule

RVT-INTERP-002 is a narrowing result, not a failure to be hidden.

It removes one attractive explanation: ordered relational trajectory is not necessary for much of the 001 effect.

**Reality gets the veto.**
