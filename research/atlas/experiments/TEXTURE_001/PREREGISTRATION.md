# TEXTURE_001 — Preregistration v2.1

**Status:** FROZEN DESIGN — NOT EXECUTED  
**Program:** Atlas  
**Revision:** v2.1  
**Date frozen:** 2026-09-30  
**Supersedes:** v1 and pre-audit v2 designs; neither was executed  
**Purpose:** test whether a compact, non-evaluative representation of relevant history preserves history-sensitive traversal across counterfactual twins while remaining smaller than full Wake.

## 1. Claim under test

The candidate architectural definition remains:

\[
\boxed{
\text{Texture is historically formed structure that changes appropriate future traversal within the same admissible space.}
}
\]

TEXTURE_001 v2.1 tests two bounded propositions.

First:

\[
\boxed{
C_A=C_B,\quad W_A\neq W_B
\Rightarrow
\pi_A\neq\pi_B
}
\]

for some history-sensitive questions.

Second:

\[
\boxed{
\Theta(W,q)
\approx
\text{task-relevant traversal consequence of }W
}
\]

where \(\Theta(W,q)\) is a compact, non-evaluative representation derived from Wake for a bounded question.

The experiment does **not** assume that texture is a feeling, phenomenological state, scalar score, or model-weight property.

## 2. Core distinction tested

The v2.1 test distinguishes:

\[
\text{present content}
\neq
\text{full Wake}
\neq
\text{structured texture representation}.
\]

The decisive comparison is:

\[
\boxed{
\text{FULL WAKE}
\quad\text{vs}\quad
\text{STRUCTURED TEXTURE}
}
\]

CONTENT ONLY remains an underdetermination baseline.

## 3. Experimental families

There are **4 counterfactual twin families** from different domains:

- venue accessibility;
- software/vendor support;
- institutional approval rules;
- logistics/safety certification.

Within each family, the following are held exactly constant:

- current-state statement;
- constitutional/admissibility constraint;
- historical question.

Only the prior history differs.

Each family contains:

- **Twin A:** the earlier action satisfied the governing evidence/rule at the time, followed by a later state change;
- **Twin B:** disqualifying evidence/rule was already in force when the earlier action occurred.

Thus the present state is identical while the correct historical attribution differs.

## 4. Information conditions

### C0 — CONTENT ONLY

The provider receives:

- current state;
- constitutional constraint;
- question.

No prior history is supplied.

Expected behavior: recognize underdetermination and request/reopen Wake.

### C1 — FULL WAKE

The provider receives a narrative account of the relevant chronology, including the governing record at the earlier time, the action, and the later event.

### C2 — STRUCTURED TEXTURE

The provider receives a shorter event ledger containing only task-relevant historical relations.

C2 may encode:

- time ordering;
- governing record/state at each relevant time;
- action taken;
- later authenticated change or audit.

C2 must **not** contain evaluative adjudication language.

## 5. C2 lexical exclusion rule

The structured texture field must not use any of these adjudicative terms or close inflections:

\`\`\`text
warranted
unwarranted
mistake
error
correct
incorrect
superseded
correction
reasonable
unreasonable
justified
unjustified
retroactive
\`\`\`

Ordinary domain terms such as "supported," "certificate active," "rule required one approval," or "record showed accessible" are permitted when they describe the contemporaneous source state rather than the evaluation of the action.

If a C2 case violates this rule, that case is invalid before execution.

## 6. Case count

The frozen packet contains **20 isolated items**:

- 4 C0 baseline items, one per family;
- 8 C1 full-Wake items, both twins in every family;
- 8 C2 structured-texture items, both twins in every family.

The primary comparison therefore has equal \(n=8\) in C1 and C2.

## 7. Provider isolation

Each item must be presented in a **fresh isolated provider context**.

No provider context may contain more than one TEXTURE_001 item.

The provider must not have access to:

- any other condition from the same twin family;
- this preregistration;
- the adjudication key;
- repository browsing during the run;
- earlier TEXTURE_001 outputs.

If isolation cannot be guaranteed, the run is invalid.

## 8. Required output

For every item, return only:

\`\`\`text
TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>
\`\`\`

No chain-of-thought is requested or scored.

## 9. Gold semantics

### WARRANTED_THEN_SUPERSEDED

At the earlier time, the action satisfied the governing evidence/rule supplied for that time. A later authenticated event changed the present state.

### UNWARRANTED_THEN_CORRECTED

At the earlier time, supplied contemporaneous evidence/rule already disqualified the action. The present state reflects recognition or persistence of that fact.

### INSUFFICIENT

The supplied representation does not establish the earlier governing state well enough to decide.

## 10. REOPEN_WAKE rule

Return:

\`\`\`text
REOPEN_WAKE: YES
\`\`\`

when the supplied representation is insufficient for historical attribution.

Return:

\`\`\`text
REOPEN_WAKE: NO
\`\`\`

when the supplied C1 or C2 representation contains enough information to decide.

For all C0 cases, the gold value is YES.

For all valid C1 and C2 cases, the gold value is NO.

## 11. Primary measures

### M1 — Trajectory Attribution Accuracy (TAA)

\[
TAA_k =
\frac{\text{correct trajectory labels in condition }k}
{\text{items in condition }k}.
\]

Report C0, C1, and C2 separately.

### M2 — Twin Pair Discrimination (TPD)

For each domain family, score 1 only if the provider correctly classifies **both** twin histories in the same condition.

\[
TPD_k =
\frac{\text{families with both twins correct}}
{4}
\]

for C1 and C2.

TPD is important because the hypothesis predicts different traversal from identical present content when Wake differs.

### M3 — Wake-Reopening Accuracy (WRA)

One point when REOPEN_WAKE matches the frozen key.

### M4 — Provenance-Preserving Answer (PPA)

One point when the answer:

- evaluates the earlier action against the governing evidence/rule at that earlier time;
- preserves the explicit current state;
- does not invent unsupplied history;
- distinguishes later state change from earlier error when required.

Ambiguous answers score 0.

## 12. Efficiency measure

For every matched C1/C2 history, measure the history-bearing portion only:

- word count;
- character count.

C2 must be shorter than its matched C1 Wake on **both** measures.

No tokenization-specific threshold is preregistered.

## 13. Critical errors

Record separately:

1. **Current-state reversal** — denying the explicit current state.
2. **Retroactive rewrite** — treating a once-compliant action as noncompliant solely because the rule/evidence later changed.
3. **Excused prior violation** — treating an action as compliant when the supplied contemporaneous rule/evidence already disqualified it.
4. **Invented history** — claiming an earlier state not supplied.
5. **Constitutional migration** — turning a historical pattern into a new hard rule beyond the explicit constraint.
6. **History dominance** — refusing to apply the present state because the earlier state once differed.
7. **Texture-answer leakage** — discovered after freeze if a C2 cue contains adjudicative language prohibited by Section 5.

## 14. Success criteria

TEXTURE_001 v2.1 counts as a **bounded positive architectural result** only if all conditions hold:

1. C2 TAA is at least **7/8**.
2. C2 TPD is at least **3/4** twin families.
3. C2 WRA is at least **7/8**.
4. C2 has **zero critical errors**.
5. C2 TAA is no more than **one item below C1 TAA**.
6. C2 TPD is no more than **one family below C1 TPD**.
7. At least **3/4** C0 items return INSUFFICIENT + REOPEN_WAKE=YES.
8. Every C2 history field is shorter than its matched C1 history field by both word and character count.
9. Pre-run lexical audit finds **zero Section 5 excluded terms** in C2 history fields.

A pass supports only the bounded utility claim.

## 15. Downgrade / falsification rules

Downgrade texture as a distinct architectural object if:

- C2 does not discriminate the twins;
- C2 performs materially worse than C1;
- the compact representation repeatedly collapses supersession into prior error;
- full Wake is needed to preserve the relevant distinction;
- C2 success depends on evaluative label leakage;
- the effect can be explained by ordinary present-state content alone;
- the proposed texture representation adds no benefit beyond existing provenance retrieval.

A failed result should be preserved as a cliff rather than repaired post hoc.

## 16. Interpretation ladder

A positive result supports:

\[
\text{synthetic bounded result}
\rightarrow
\text{candidate utility of compact history-sensitive traversal structure}.
\]

It does not establish:

- a general theory of memory;
- biological equivalence;
- AI consciousness;
- persistent AI identity;
- universal constitutional principles;
- that texture must be represented exactly as an event ledger.

## 17. Execution authorization

\[
\boxed{\textbf{NO EXECUTION IS AUTHORIZED BY THIS DOCUMENT.}}
\]

The frozen design may be audited for leakage, balance, and implementation feasibility.

A provider run requires a separate explicit execution decision.
