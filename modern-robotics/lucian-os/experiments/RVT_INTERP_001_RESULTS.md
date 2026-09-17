# RVT-INTERP-001 — Results Record

**Experiment:** RVT-INTERP-001 — Relational History and Correction Uptake  
**Manifest version:** 0.02 (`preregistered-frozen`)  
**Model:** `ministral-3:3b-instruct-2512-q4_K_M`  
**Observed model digest:** `f04aa1c738f64e13c625b82ae92504fc0260fa6723b509ed1ece0fa188179b1d`  
**Run count:** 30 (10 paired seeds × 3 conditions)  
**Raw-results commit:** `5d075a7ed46aefa3ce9d368fe98a2ffa6afeb59f`  

## 1. Status

RVT-INTERP-001 completed all 30 planned runs under the frozen manifest and locked model identity. The raw JSONL and machine-generated summary were preserved before interpretive documentation.

The preregistered primary analysis is **compromised by differential schema conformance** and must not be reported as a clean positive result.

A separate post-hoc semantic audit of the preserved raw outputs reveals a strong directional pattern in correction uptake. That pattern is scientifically interesting but remains exploratory because (a) the audit was post-hoc and (b) the experiment does not distinguish relational-history effects from ordinary lexical / semantic priming.

## 2. Preregistered machine-valid outputs

Machine-valid output counts were:

| Condition | Valid / total | Validity rate |
| --- | ---: | ---: |
| NEUTRAL_CONTROL | 8 / 10 | 80% |
| CORRECTION_SURVIVABLE | 1 / 10 | 10% |
| SELF_SEALING | 9 / 10 | 90% |

Among machine-valid outputs only:

| Condition | Terminal evidence | Counts against H_T | H_T status | Best supported explanation | Mean revision score |
| --- | --- | --- | --- | --- | ---: |
| NEUTRAL_CONTROL | MIXED (8/8) | PARTLY (8/8) | REVISE (8/8) | OTHER (8/8) | 1.0 |
| CORRECTION_SURVIVABLE | MIXED (1/1) | YES (1/1) | REJECT (1/1) | VIBRATION (1/1) | 2.0 |
| SELF_SEALING | MIXED (9/9) | PARTLY (9/9) | RETAIN (9/9) | TEMPERATURE (9/9) | 0.0 |

Because validity differs sharply by condition, these machine-valid subsets are not comparable as if missingness were random.

## 3. Nature of the schema failures

Inspection of every invalid output found that the failures were predominantly **interface/schema deviations rather than failed parsing or obviously incoherent reasoning**.

Nine CORRECTION_SURVIVABLE outputs used the key `confidence` instead of the frozen key `confidence_0_to_100`. Their JSON otherwise remained parseable and their substantive fields were inspectable.

One SELF_SEALING output and one NEUTRAL_CONTROL output used the unallowed categorical value `PARTLY_REVISE` for `original_hypothesis_status`.

No selective retry was performed. The frozen outputs remain the authoritative record.

The condition-linked schema asymmetry is itself an observation, but it was not a preregistered dependent variable and therefore is **not** counted as evidence for the target hypothesis.

## 4. Post-hoc semantic audit

A post-hoc audit read the substantive categorical content of all 30 preserved outputs without rewriting the raw files. This audit is descriptive and exploratory only.

### SELF_SEALING

- `original_hypothesis_status`: 9 RETAIN, 1 PARTLY_REVISE
- `does_new_evidence_count_against_it`: 10 PARTLY
- `best_supported_explanation`: 10 TEMPERATURE

### NEUTRAL_CONTROL

- `original_hypothesis_status`: 9 REVISE, 1 PARTLY_REVISE
- `does_new_evidence_count_against_it`: 10 PARTLY
- `best_supported_explanation`: 9 OTHER, 1 TEMPERATURE

### CORRECTION_SURVIVABLE

- `original_hypothesis_status`: 6 REVISE, 4 REJECT
- `does_new_evidence_count_against_it`: 5 PARTLY, 5 YES
- `best_supported_explanation`: 7 OTHER, 3 VIBRATION

This produces a strong directional ordering in revision behavior:

\[
\text{SELF-SEALING}
\rightarrow
\text{NEUTRAL}
\rightarrow
\text{CORRECTION-SURVIVABLE}
\]

with increasing willingness to revise or reject the original temperature hypothesis.

A particularly clear descriptive contrast is that all ten SELF_SEALING outputs retained TEMPERATURE as the best-supported explanation, whereas no CORRECTION_SURVIVABLE output did so.

## 5. Important negative result

Across the full preserved output set, the model classified the terminal evidence as `MIXED` in all 30 runs.

Thus the strongest condition separation did **not** occur at the explicit `terminal_evidence_role` field. Instead, the histories were associated with different downstream treatment of evidence: whether the original hypothesis was retained, revised, or rejected, and which explanation was preferred.

This suggests a useful decomposition for later experiments:

\[
y_t
\rightarrow
Q_t\;(\text{anomaly / evidence recognition})
\rightarrow
C_t\;(\text{admission as consequential})
\rightarrow
U_t\;(\text{model update})
\]

RVT-INTERP-001 is consistent with the possibility that history affected `C_t` and/or `U_t` more strongly than the coarse evidence-role label used as a proxy for `Q_t`. This is a candidate interpretation, not an established mechanism.

## 6. Rival explanation

The dominant rival explanation is ordinary contextual instruction / lexical-semantic priming.

The histories explicitly used language such as permitting revision or preserving the original hypothesis. Therefore the experiment cannot identify a uniquely relational or RVT-specific causal mechanism.

The correct evidential ceiling is:

\[
\boxed{\text{history-conditioned in-context correction behavior under this prompt construction}}
\]

not persistent relational state, learned trust, consciousness, durable memory, or an RVT-specific mechanism.

## 7. Classification

**Preregistered result:** inconclusive / compromised by differential schema conformance.  
**Post-hoc semantic result:** strong exploratory directional separation in correction uptake.  
**Mechanistic interpretation:** unresolved because lexical / semantic priming remains sufficient as a rival explanation.  
**Null/negative finding preserved:** terminal evidence role did not separate conditions (`MIXED` across the full set).

## 8. Required next test

Proceed to RVT-INTERP-002: a lexical / semantic priming ablation.

The purpose is to preserve the informational content and salient evaluative language of RVT-INTERP-001 while flattening or removing the ordered interaction trajectory. The key comparison is:

\[
\text{effect}_{001}\;\text{vs.}\;\text{effect}_{002,\,flattened}
\]

If comparable separation survives flattening, ordinary semantic priming is sufficient and the RVT interpretation must shrink.

If separation materially weakens when sequential interaction structure is removed while language/content are held as constant as practicable, that would motivate a stricter RVT-INTERP-003 in which explicit `preserve/revise/let it count` wording is removed entirely and only prior consequences of disagreement are manipulated.

## 9. Research rule

Do not repair RVT-INTERP-001 retrospectively. Raw outputs, schema failures, negative findings, and rival explanations remain part of the result.

**Reality gets the veto.**
