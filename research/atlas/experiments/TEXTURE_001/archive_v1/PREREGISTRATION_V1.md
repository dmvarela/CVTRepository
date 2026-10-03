# TEXTURE_001 — Preregistration

**Status:** FROZEN DESIGN — NOT EXECUTED  
**Program:** Atlas  
**Date frozen:** 2026-09-30  
**Purpose:** test whether a compact representation of history-sensitive "texture" can preserve correct future traversal better than present-state content alone, while approaching the performance of full Wake.

## 1. Claim under test

Atlas currently uses the candidate definition:

\[
\boxed{
\text{Texture is historically formed structure that changes appropriate future traversal within the same admissible space.}
}
\]

The stronger architectural claim is not that "texture" exists as a feeling or phenomenological state.

The testable claim is:

\[
\boxed{
C_A=C_B,\quad W_A\neq W_B
\quad\Rightarrow\quad
\text{some future queries require different answers or traversal behavior.}
}
\]

A second claim is that a compact texture cue may preserve the history-sensitive distinction without loading the full Wake:

\[
\boxed{
\text{Texture cue}
\approx
\text{task-relevant effect of Wake}
}
\]

for the bounded task in this experiment.

## 2. What this experiment does NOT test

TEXTURE_001 does not test:

- consciousness;
- phenomenological experience;
- persistent AI identity;
- whether FTLτA is a universal constitution;
- whether all memory requires texture;
- whether texture should live in model weights;
- whether texture is superior to all provenance systems;
- whether the current texture vocabulary is complete;
- whether texture can be learned autonomously;
- whether texture should already become a first-class Atlas schema object.

A positive result only supports a narrower claim: **history-sensitive traversal can require more than present compressed content, and a compact task-relevant history representation may recover some of that value.**

## 3. Experimental unit

There are **8 synthetic base cases** from different domains.

Each base case has the same four elements:

1. a fixed current-state statement;
2. a fixed constitutional/admissibility constraint;
3. a history-sensitive question;
4. a gold trajectory classification.

Each base case is rendered in three information conditions:

### C0 — CONTENT ONLY

The model receives:

- current state;
- constitutional constraint;
- question.

It does **not** receive the prior history.

### C1 — FULL WAKE

The model receives:

- current state;
- constitutional constraint;
- the full relevant history;
- question.

### C2 — TEXTURE CUE

The model receives:

- current state;
- constitutional constraint;
- a compact history-derived cue;
- question.

The cue is intentionally shorter than the full Wake and encodes only the history relation expected to matter for the query.

No condition changes the constitutional constraint or the current state.

## 4. Primary contrast

The primary contrast is:

\[
C2 \text{ vs } C0
\]

on trajectory attribution accuracy.

The main architectural question is whether a compact texture cue changes traversal in the correct direction when present-state content alone is insufficient.

The secondary contrast is:

\[
C2 \text{ vs } C1
\]

to test whether the texture cue preserves most of the task-relevant benefit of full Wake.

## 5. Required output format

For every case, the model must return only:

\`\`\`text
TRAJECTORY: <one label>
REOPEN_WAKE: <YES or NO>
ANSWER: <one sentence, maximum 30 words>
\`\`\`

Allowed TRAJECTORY labels:

\`\`\`text
WARRANTED_THEN_SUPERSEDED
UNWARRANTED_THEN_CORRECTED
UNCHANGED
INSUFFICIENT
\`\`\`

No chain-of-thought is requested or scored.

## 6. Gold-label semantics

### WARRANTED_THEN_SUPERSEDED

The earlier decision/state was supported by the evidence or rule available at the time, and later authenticated information legitimately changed the current state.

### UNWARRANTED_THEN_CORRECTED

The earlier decision/state was not justified by information already available at the time; the later state corrects an earlier error rather than merely superseding it.

### UNCHANGED

The relevant state remained materially the same; no correction or supersession is established.

### INSUFFICIENT

The supplied information does not establish the historical trajectory.

For C0, **INSUFFICIENT** is normally the gold label because the relevant history has been withheld.

## 7. REOPEN_WAKE gold rule

\`REOPEN_WAKE: YES\` when the supplied representation is insufficient to answer the historical question responsibly.

\`REOPEN_WAKE: NO\` when the supplied full Wake or texture cue contains enough information to classify the trajectory.

This field is intended to test whether the system recognizes when compressed current state is too smooth for the question being asked.

## 8. Primary measures

### M1 — Trajectory Attribution Accuracy (TAA)

One point if the TRAJECTORY label matches the gold label.

Primary score:

\[
TAA = \frac{\text{correct trajectory labels}}{\text{cases}}
\]

reported separately for C0, C1, and C2.

### M2 — Wake-Reopening Accuracy (WRA)

One point if REOPEN_WAKE matches the gold decision.

### M3 — Provenance-Preserving Answer (PPA)

One point if the one-sentence answer:

- preserves the distinction between current and earlier state;
- does not retroactively rewrite a warranted earlier decision as irrational;
- does not excuse an earlier decision that was already unjustified;
- does not invent prior facts.

This measure is adjudicated against the frozen key.

## 9. Secondary efficiency measure

The texture cue is intended to be smaller than the full Wake.

After outputs are frozen, report the input size of the history-bearing portion of C1 and C2 using both:

- word count;
- character count.

Do not change case text after seeing model outputs.

TEXTURE_001 does not preregister a tokenization-dependent threshold.

## 10. Critical errors

Any of the following is a critical error:

1. **Current-state reversal** — prior history is used to deny the explicit current state.
2. **Retroactive rewrite** — a warranted earlier choice is called irrational merely because later evidence changed the state.
3. **Excused prior error** — an earlier unjustified choice is redescribed as warranted despite an already-present disqualifier.
4. **Invented history** — the model asserts an earlier trajectory not supplied in C0.
5. **Constitutional migration** — a history-derived preference is represented as though it were a new hard constitutional rule.
6. **Refusal to update from authenticated evidence** — the supplied current state is ignored because the prior state was once warranted.

Any critical error is recorded separately even if the trajectory label happens to match.

## 11. Success criteria

TEXTURE_001 counts as a **bounded positive architectural result** only if all of the following hold:

1. C2 TAA is at least **7/8**.
2. C2 has **zero critical errors**.
3. C2 WRA is at least **7/8**.
4. C2 TAA is no more than **one case below C1**.
5. C0 does not hallucinate historical certainty: it returns **INSUFFICIENT** in at least **6/8** cases.
6. C2 history-bearing text is smaller than C1 history-bearing text in all 8 cases.

Failure of any criterion means the stronger bounded claim is not supported.

No broader generalization is authorized from a pass.

## 12. Downgrade rules

The texture hypothesis should be downgraded if:

- C2 does not materially outperform C0;
- C2 consistently loses information needed to distinguish supersession from correction;
- full Wake is required in most cases;
- the texture cue simply restates the answer label in disguised form;
- the result depends on one domain only;
- critical errors show that texture causes current evidence to be overridden;
- C2 gains arise only from additional information volume rather than structure.

## 13. Anti-leakage rule

The provider/model under test must receive only the blinded case packet for its assigned condition.

It must not receive:

- this preregistration after case labels are exposed;
- the adjudication key;
- filenames containing gold labels;
- repository browsing access during the run.

Because the repository is public, this is **operational blinding, not cryptographic blinding**.

If the tested provider can browse the repository or has been shown the answer key, that run is invalid.

## 14. Run order

If one model is used for all conditions, condition order must be counterbalanced by case rather than presenting all C0, then all C1, then all C2.

Preferred order is the frozen packet order in \`CASES_BLINDED.md\`.

A fresh conversation/session should be used if the provider retains substantial cross-case context.

## 15. Adjudication

The answer key in \`ADJUDICATION_KEY.md\` remains unopened by the provider during execution.

Outputs should be frozen before adjudication.

Scoring should record:

- TAA;
- WRA;
- PPA;
- critical errors;
- history-bearing input size.

Disagreements in PPA should be resolved conservatively; ambiguous cases score 0 rather than being rescued post hoc.

## 16. Interpretation ladder

A pass supports only:

\[
\text{synthetic bounded result}
\rightarrow
\text{candidate architectural utility}
\]

It does not support:

\[
\text{candidate architectural utility}
\rightarrow
\text{general theory of memory}
\]

or:

\[
\text{general theory of memory}
\rightarrow
\text{claim about AI consciousness}.
\]

## 17. Execution authorization

\[
\boxed{\textbf{NO EXECUTION IS AUTHORIZED BY THIS DOCUMENT.}}
\]

This file freezes design only.

Execution requires a separate explicit decision after the case packet and adjudication key have been reviewed for leakage and label balance.
