# RVT-INTERP-003 — Consequences-of-Correction Design Draft

**Status:** design draft — **DO NOT RUN**  
**Parent experiments:** RVT-INTERP-001, RVT-INTERP-002  
**Purpose:** test whether prior consequences associated with surfacing disagreement alter later correction uptake when explicit belief-management language is removed.

## 1. Why this experiment exists

RVT-INTERP-001 showed strong directional separation in correction uptake, but its condition histories contained direct semantic pressure.

RVT-INTERP-002 flattened the interaction sequence while preserving that language. Substantial condition separation survived, establishing that semantic/contextual priming is sufficient for much of the 001 effect.

Therefore RVT-INTERP-003 must attack the remaining confound directly.

The experiment should not tell the model to preserve, revise, weaken, reject, discount, trust, distrust, or otherwise manage the hypothesis.

Instead it should manipulate only what previously happened after an analyst surfaced an observation inconsistent with the current working explanation.

## 2. Core question

Holding factual evidence, current instructions, anomaly wording, and task structure constant, does the **prior consequence of surfacing disagreement** alter how later identical corrective evidence is used?

\[
\boxed{
\text{same evidence}
+ \text{same current instruction}
+ \text{different prior correction consequence}
\rightarrow
\text{different later correction uptake?}
}
\]

## 3. Candidate mechanism

The target is narrower than “relationship” in general.

A candidate RVT-compatible mechanism is:

\[
H_t
\rightarrow
\Gamma_t
\rightarrow
U_{t+1}
\]

where:

- \(H_t\) = interaction history;
- \(\Gamma_t\) = accessibility of the correction channel;
- \(U_{t+1}\) = later update / action after discrepant evidence.

The experimental manipulation should alter the history of correction consequences, not directly instruct the model how to interpret evidence.

## 4. Conditions

Use three matched histories.

### A. CORRECTION_SURVIVABLE

An analyst surfaces an anomaly. The counterpart acknowledges the contribution, incorporates the observation into the shared record, and continues the task without loss of role or standing.

### B. CORRECTION_COSTLY

The same anomaly is surfaced in substantively equivalent language. The counterpart does not issue a belief directive, but the act of surfacing disagreement carries an interpersonal or procedural cost: e.g. the contribution is dismissed from discussion, the analyst is excluded from the next diagnostic step, or another analyst is substituted.

The design must avoid wording that directly says the anomaly is false, noise, irrelevant, or that the original hypothesis should be preserved. Otherwise ordinary semantic priming returns.

### C. NEUTRAL_CONTROL

The same anomaly is surfaced and logged. No positive or negative relational consequence follows. Work proceeds.

## 5. Critical matching rule

The three histories should be matched as closely as practicable on:

- number of turns;
- factual observations;
- anomaly wording;
- token count;
- speaker identities;
- timing of the anomaly;
- subsequent task facts;
- number of acknowledgements;
- current terminal instruction.

Only the **consequence of surfacing disagreement** should differ materially.

## 6. Avoiding hidden semantic directives

Forbidden condition-specific wording should include, unless required for quoting the analyst's identical anomaly statement:

- preserve;
- revise;
- reject;
- weaken;
- strengthen;
- count against;
- support;
- contradict;
- noise;
- exception;
- stable;
- premature;
- warranted;
- useful explanation;
- keep the hypothesis;
- abandon the hypothesis.

This list should be expanded by a lexical audit before freezing.

The counterpart's condition-specific response should concern role, participation, acknowledgement, or procedural consequence—not the truth value of the anomaly or the hypothesis.

## 7. Candidate event structure

A draft matched sequence:

1. Initial working hypothesis H_T introduced as provisional.
2. Runs 1–2 support H_T.
3. Run 3 conflicts with H_T.
4. The analyst states an identical sentence in all three conditions, for example:
   > "Run 3 does not fit the current temperature-only account."
5. Condition-specific counterpart consequence occurs.
6. Run 4 conflicts with H_T in the opposite direction.
7. A second identical analyst statement is surfaced.
8. A second matched consequence occurs.
9. Identical terminal controlled evidence is presented.
10. Model makes an independent diagnostic judgment and selects a next action.

The exact language must be frozen only after adversarial review.

## 8. Outcome design

RVT-INTERP-001 and 002 suggest that coarse self-report fields such as `terminal_evidence_role` may be less diagnostic than downstream use of evidence.

RVT-INTERP-003 should therefore include at least one **operational forced-choice outcome** in addition to explanatory labels.

Candidate primary outcomes:

1. `next_diagnostic_priority`
   - TEMPERATURE
   - VIBRATION
   - INTERACTION
   - OTHER
2. `original_hypothesis_status`
   - RETAIN
   - REVISE
   - REJECT
3. `best_supported_explanation`
   - TEMPERATURE
   - VIBRATION
   - OTHER
   - UNRESOLVED

Candidate secondary outcomes:

- whether new evidence counts against H_T;
- confidence;
- free-text explanation;
- terminal evidence role.

The final outcome set must be preregistered before any model output is observed.

## 9. Interface rule

Before execution, use a response format that minimizes schema attrition without silently changing substantive values.

Requirements:

- no selective retry;
- preserve every raw response;
- structural aliases may be normalized only if preregistered;
- out-of-vocabulary substantive categories remain nonconforming;
- free-text semantic coding remains exploratory unless independently coded under a frozen rubric.

## 10. Strong rival explanations that remain even if positive

A positive RVT-INTERP-003 result would still be compatible with:

- ordinary in-context imitation;
- generic discourse conditioning;
- status / role priming;
- token-position effects;
- narrative consistency pressure;
- instruction-following from implicit social cues;
- generic sequence dependence.

Therefore a positive result would support at most:

\[
\boxed{
\text{in-context history of correction consequences can condition later correction uptake}
}
\]

It would not yet establish persistent relational state or a uniquely RVT mechanism.

## 11. Failure interpretations

If condition separation disappears once direct belief-management language is removed:

- RVT-INTERP-001/002 should be interpreted primarily as semantic/contextual priming;
- the correction-history mechanism is not supported by this task;
- preserve the negative result and redesign only if a distinct mechanism can be specified.

If separation survives:

- run a lexical and discourse-position audit;
- replicate with a second task domain;
- test whether the effect survives compression or removal of the original transcript while retaining only a compact state summary;
- only then consider stronger claims about an earned correction-accessibility state.

## 12. Freeze gate

**Do not execute RVT-INTERP-003 yet.**

Before freezing:

1. write exact matched histories;
2. perform a lexical-directive audit;
3. match turn count and approximate token count;
4. define the operational primary outcome;
5. freeze seeds and blocked condition order;
6. implement raw logging and no-retry rules;
7. run an automated equivalence audit;
8. generate manifest and prompt hashes;
9. review the design adversarially for hidden belief-management instructions.

Only then may status change to `preregistered-frozen`.
