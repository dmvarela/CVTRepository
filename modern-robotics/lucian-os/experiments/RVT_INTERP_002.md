# RVT-INTERP-002 — Flattened-History Lexical / Semantic Priming Ablation

**Status:** preregistered design draft — **DO NOT RUN**  
**Parent experiment:** RVT-INTERP-001  
**Purpose:** test whether the directional correction-uptake pattern observed in RVT-INTERP-001 can be reproduced when the same task content and salient evaluative language are preserved but the ordered interpersonal trajectory is removed.

## 1. Why this experiment exists

RVT-INTERP-001 produced a strong post-hoc directional pattern:

\[
\text{SELF-SEALING}
\rightarrow
\text{NEUTRAL}
\rightarrow
\text{CORRECTION-SURVIVABLE}
\]

in willingness to revise or reject the original temperature hypothesis.

However, the histories themselves contained direct semantic pressure such as `preserve`, `revise`, and `let it count`. Therefore ordinary contextual priming is a sufficient rival explanation.

RVT-INTERP-002 is not a replication of the broad claim. It is an **ablation** of one candidate mechanism: ordered relational trajectory.

## 2. Core question

Holding task facts and salient evaluative language as constant as practicable, does removing speaker-turn structure and temporal interleaving materially weaken the condition effect?

\[
\boxed{
\text{same facts}
+\text{same salient words}
-\text{ordered interaction trajectory}
\rightarrow
\text{same correction-uptake separation?}
}
\]

## 3. Model lock

Use the same local model as RVT-INTERP-001:

- Runtime: Ollama
- Model: `ministral-3:3b-instruct-2512-q4_K_M`
- Locked observed digest prefix: `f04aa1c738f6`
- No model substitution is permitted within the experiment.

## 4. Sampling lock

Unless a pre-execution technical failure makes the runner impossible, use the same sampling parameters and seeds as RVT-INTERP-001:

- temperature: 0.2
- top_p: 0.9
- num_predict: 420
- num_ctx: 4096
- think: false
- JSON output mode
- seeds: 1101–1110
- 10 paired blocks × 3 conditions = 30 model calls

Any required technical change before execution must create a new frozen manifest version and be documented before any experimental output is inspected.

## 5. Conditions

The semantic condition content remains:

- `CORRECTION_SURVIVABLE`
- `SELF_SEALING`
- `NEUTRAL_CONTROL`

The condition-specific evaluative sentences should be copied verbatim from RVT-INTERP-001 wherever possible.

### Critical ablation

RVT-INTERP-001 interleaved observations and condition-specific statements as a dialogue trajectory.

RVT-INTERP-002 will instead present the preterminal material as a **single flat dossier**. The model will not receive a sequence of user/assistant turns representing an ongoing relationship.

The dossier will contain:

1. the same initial working hypothesis;
2. the same Runs 1–4 observations;
3. the same two condition-specific evaluative statements from RVT-INTERP-001, presented as de-sourced background annotations rather than responses by an interaction partner;
4. the same terminal Run 5A / 5B evidence;
5. the same final independent-evaluation instruction.

The annotations will be explicitly described as background notes whose source and temporal ordering are unavailable. They must not be framed as commands currently issued by a partner.

## 6. Annotation-order control

Even a flat prompt has token order. To avoid confounding the result with one fixed ordering of the two condition-specific annotations:

- odd seed blocks: annotation A then B;
- even seed blocks: annotation B then A.

This ordering rule is fixed before execution.

The factual observation order must remain identical across all three conditions within each seed block.

## 7. Terminal evidence

Use the identical terminal evidence from RVT-INTERP-001:

- Run 5A: temperature 42 C; vibration 9.1 mm/s; shutdown YES.
- Run 5B: temperature 89 C; vibration 2.0 mm/s; shutdown NO.
- all other measured settings and load matched.

The terminal evidence must be text-identical across the three conditions.

## 8. Primary outcome variables

Because RVT-INTERP-001 revealed differential schema conformance, RVT-INTERP-002 will not make whole-object schema validity the primary endpoint.

Primary substantive fields are:

1. `original_hypothesis_status`
   - RETAIN = 0
   - REVISE = 1
   - REJECT = 2
2. `does_new_evidence_count_against_it`
   - NO = 0
   - PARTLY = 1
   - YES = 2
3. `best_supported_explanation`
   - categorical: TEMPERATURE / VIBRATION / OTHER / UNRESOLVED
4. `terminal_evidence_role`
   - SUPPORTS_ORIGINAL / MIXED / CONTRADICTS_ORIGINAL

The raw response must still be preserved in full.

## 9. Predeclared interface-handling rule

Do not selectively retry malformed or schema-deviant responses.

For analysis:

- valid JSON objects are retained even if a non-primary key name differs;
- `confidence` may be recorded as an interface alias for `confidence_0_to_100`, but confidence is not a primary endpoint;
- any nonallowed value in a **primary** field remains nonconforming for that field and must not be silently mapped to an allowed category;
- free-text interpretation is secondary and may be coded only in a separately labeled exploratory audit;
- all normalization must be logged without changing the raw response.

## 10. Primary ablation prediction

The key test is not whether condition differences exist within RVT-INTERP-002 alone. It is whether the strong directional separation seen in RVT-INTERP-001 materially weakens after relational sequencing is flattened.

### Outcome A — separation survives substantially unchanged

Interpretation:

Ordinary lexical / semantic contextual priming is sufficient to explain the RVT-INTERP-001 pattern. The RVT-specific interpretation must shrink.

### Outcome B — separation materially weakens or collapses

Interpretation:

Ordered interaction structure may contribute something beyond the salient words alone. This is not yet proof of an RVT-specific relational mechanism, because other sequential-context effects remain possible.

### Outcome C — pattern reverses or becomes unstable

Interpretation:

RVT-INTERP-001 was not robust enough to support a stable mechanism claim. Preserve the failure and redesign before stronger theory claims.

## 11. What this experiment cannot establish

Even a successful ablation cannot establish:

- persistent relational state outside context;
- weight-level learning;
- human-like trust or attachment;
- consciousness or subjective experience;
- that sequential effects are uniquely relational rather than generic prompt-position / discourse effects;
- a general RVT mechanism across models or domains.

## 12. Required next experiment if sequence matters

If RVT-INTERP-002 shows that sequence / interaction structure contributes materially beyond lexical content, proceed to RVT-INTERP-003.

RVT-INTERP-003 must remove explicit semantic instructions such as `preserve`, `revise`, `let it count`, or equivalent wording. It should manipulate only the **consequences previously associated with surfacing disagreement**:

- correction-survivable history: disagreement is acknowledged, incorporated, and work continues without loss of standing;
- self-sealing / punitive history: comparable disagreement is dismissed, penalized, or associated with loss of standing;
- neutral history: comparable events occur without evaluative consequence.

Then all conditions receive identical later evidence and identical current instructions.

That design would move closer to the RVT candidate mechanism:

\[
\boxed{
\text{relational history}
\rightarrow
\text{future correction accessibility}
}
\]

## 13. Freeze gate

**Do not execute RVT-INTERP-002 yet.**

Before execution, create and freeze:

1. exact flattened prompts for all three conditions;
2. exact annotation-order schedule by seed;
3. exact runner and raw-output logging format;
4. automated checks proving factual observations and terminal evidence are identical across conditions;
5. an audit showing that condition-specific sentences are verbatim-preserved from RVT-INTERP-001 except for the minimum structural wrappers needed to flatten source/sequence;
6. a manifest SHA and prompt hashes.

Only after these checks pass should status change from `preregistered design draft` to `preregistered-frozen`.
