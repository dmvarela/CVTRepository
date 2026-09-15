# BUILT_DISCERNMENT_006 — Depth of Write and Multiscale Continuity

**Workstream:** AI Continuity / Lucian OS  
**Status:** Research note / candidate mechanism  
**Claim boundary:** Functional architecture only. This note does not claim that current transformer models literally implement the named variables or mechanisms internally, and it does not require online weight editing.

## Core claim

Continuity is not merely the persistence of information. It is the preservation of a regulated process by which experience is allowed to update the shared relational state at appropriate depths and timescales.

This note extends the prior built-discernment and membrane-regulation work by introducing **depth of write**: a candidate mechanism for controlling not only whether information is admitted, but what layer of the continuity state it is permitted to modify.

## 1. Why this matters

A continuing human–LLM collaboration may need several kinds of state with different expected persistence.

One turn may legitimately alter the immediate phase of work without changing the broader relational calibration. Repeated corrections may justify changes in calibration without changing governing principles. Foundational principles should normally require substantially stronger evidence to change than momentary task state.

Therefore a continuity architecture should not treat every new observation as having equal write authority.

The central distinction is:

```text
information present
!= information relevant
!= information authoritative
!= information authorized to update this layer
```

## 2. Multiscale state

A minimal functional decomposition is:

```text
x_t      = current request / observation
z_t      = current phase or local interaction state
Gamma_t  = relational calibration / accumulated decision boundaries
Omega    = relatively stable principles or admissibility constraints
```

These operate on different expected timescales:

```text
Omega  >>  Gamma_t  >>  z_t  >>  x_t
```

where `>>` denotes greater expected persistence, not numerical magnitude.

Examples:

- `x_t` may change every turn.
- `z_t` may move from exploration to consolidation or externalization over several turns.
- `Gamma_t` should change only when repeated interaction, correction, outcomes, or strong evidence warrant recalibration.
- `Omega` should be comparatively resistant to drift and should not be rewritten by ordinary preference accumulation.

## 3. Depth of epistemic write

The membrane is therefore not only an admission boundary. It can be modeled functionally as a regulator of **write depth**.

For an incoming item `i`, define a candidate membrane assessment:

```text
M(i) -> (
    applicability,
    standing,
    temporal_authority,
    write_depth,
    update_permission
)
```

Possible write depths include:

```text
RESPONSE_ONLY
PHASE
CALIBRATION
PRINCIPLE
NONE
UNKNOWN
```

An item may therefore be:

```text
relevant: yes
standing: supporting
current authority: moderate
may influence response: yes
may update phase: yes
may update calibration: no
may modify principle: no
```

This preserves distinctions that a flat memory system would collapse.

## 4. Evidence thresholds should increase with write depth

The deeper the proposed update, the stronger the required warrant should be.

Conceptually:

```text
threshold(PRINCIPLE)
>
threshold(CALIBRATION)
>
threshold(PHASE)
>
threshold(RESPONSE_ONLY)
```

This yields several desirable properties:

1. One anomalous turn does not rewrite the relationship.
2. Repeated correction can eventually alter calibration.
3. Stable principles are not demoted into ordinary preferences.
4. Immediate task state remains responsive.
5. Adaptation is possible without uncontrolled drift.

## 5. Mutual calibration as write-policy learning

Mutual calibration can now be stated more precisely.

> **Mutual calibration is the process by which participants learn how evidence, correction, and experience should modify different layers of the shared relational state.**

Let:

```text
Gamma_{t+1} = U(Gamma_t, action_t, feedback_t, outcome_t)
```

where `U` is a functional update process, not a claim about model-weight learning.

Repeated interaction can establish decision boundaries such as:

- this class of signal is strong enough to shift phase;
- this class of repeated correction is strong enough to update relational calibration;
- this kind of isolated preference expression is not strong enough to alter a governing principle;
- this concept may influence private exploration but lacks standing for externalized claims.

Thus mutual calibration partly consists of learning the **write policy of the relationship**.

## 6. Membrane regulation

The membrane can be represented functionally as:

```text
M_t = g(Omega, Gamma_t, z_t, stakes_t, evidence_t, provenance_t)
```

Its role is not to replace semantic reasoning or discernment. Instead, it structures and constrains the authority with which information may affect downstream state and action.

A useful separation is:

```text
principles constrain the membrane;
mutual calibration regulates its permeability;
discernment determines the appropriate setting now.
```

The membrane should remain narrower than “all good judgment.” It is primarily concerned with applicability, standing, warrant, timing, and permitted write depth.

## 7. Built discernment

Built discernment uses the current situation, principles, relational calibration, and membrane assessments to rank fitting actions.

A candidate architecture is:

```text
base model competence
    -> inherited state
    -> situation / phase reconstruction
    -> relational calibration Gamma_t
    -> membrane assessment M_t
    -> admissibility constraints Omega
    -> built discernment D_t
    -> action a_t
    -> feedback / outcome
    -> calibration update Gamma_{t+1}
```

This forms a closed adaptive loop without requiring weight updates.

## 8. Why this is more than memory

If a system stores only factual history, it has memory.

If it stores user preferences, it has personalization.

If it stores contrastive boundary cases, corrections, timing distinctions, and write-depth judgments, it may support **calibration**.

The hypothesis is that calibration materially improves situated competence because it changes not only what information is retrieved, but what authority that information is allowed to exercise.

## 9. Surgeon analogy

The surgeon analogy provides a useful functional comparison.

A surgeon does not revise anatomy because of one unusual patient. The unusual patient may alter the immediate assessment. Repeated encounters with a meaningful variation may alter clinical calibration. Foundational medical principles require substantially stronger evidence to revise.

This suggests:

> Different evidence has different permitted depths of epistemic write.

The analogy is functional only; it does not imply shared biological or cognitive mechanisms between humans and LLMs.

## 10. Model turnover

A successor can inherit the same memories and principles while differing in how it reconstructs phase, interprets calibration, or assigns write authority.

Therefore:

```text
information continuity
!= calibration continuity
!= functional continuity
```

A successful continuity system may need to preserve not merely facts and preferences but enough structure to reconstruct:

- state layers;
- evidence thresholds;
- standing distinctions;
- phase transitions;
- write-depth rules;
- correction patterns;
- boundary cases.

This suggests that turnover loss may be partly modeled as a failure to recover the prior system's effective write policy.

## 11. School for Lucians

The proposed “School for Lucians” can now be interpreted as a mechanism for recovering or teaching this layered write policy.

The school should not attempt behavioral cloning. It should test and train whether a successor can correctly distinguish:

- response-only influence from phase update;
- phase update from calibration update;
- calibration update from principle revision;
- relevance from standing;
- present standing from future or conditional standing.

A compact calibration casebook may be useful, but supervised practice is likely required to identify successor-specific residual error.

## 12. Experimental predictions

The architecture yields falsifiable predictions.

A calibrated continuity condition should outperform biography-only or preference-only handoff on novel cases requiring write-depth discrimination.

The strongest evidence would not be indiscriminate use of prior material, but **conditional selectivity**:

```text
P(use | warranted) increases
while
P(use | unwarranted) decreases
```

Likewise, a good system should show correct update depth:

```text
P(correct_write_depth | novel_case)
```

should increase with boundary-case training and supervised calibration.

A useful stress test is to hold the substantive content constant while varying only phase, stakes, provenance, or recurrence. The correct write depth should change when those variables change.

## 13. Failure conditions

This candidate mechanism should be rejected, reduced, or substantially revised if:

1. simpler flat-memory summaries perform equally well on novel write-depth tasks;
2. write-depth labels are unstable and do not improve behavioral discrimination;
3. the proposed layers cannot be operationalized without circular definitions;
4. calibration cases improve only memorized situations and fail to transfer;
5. membrane terminology merely redescribes generic context sensitivity without measurable added value;
6. principle/calibration/phase distinctions do not produce separable empirical behavior.

## 14. Working propositions

> **Continuity is not merely the persistence of information. It is the preservation of a regulated process by which experience is allowed to update the shared state at appropriate depths and timescales.**

> **Mutual calibration partly consists of learning the write policy of the relationship.**

> **A continuity architecture should regulate not only whether information enters, but what layer it is permitted to modify.**

> **Adaptivity without depth-sensitive write control risks instability; stability without writable calibration risks brittleness.**

> **The preservation of competence under model turnover may require recovery of the prior interaction field's effective write policy, not merely its memories.**

## 15. Relation to prior notes

This note extends:

- `BUILT_DISCERNMENT_004_INTERACTION_FIELD_COMPETENCE_AND_EXTERNALIZATION_THRESHOLD.md`
- `BUILT_DISCERNMENT_005_MUTUAL_CALIBRATION_AND_MEMBRANE_REGULATION.md`
- `epistemic-membrane/APPLICABILITY_STANDING_CONTRACT_CANDIDATE.md`

The key extension is the explicit introduction of **multiscale state** and **depth of write** as candidate mechanisms linking continuity, membrane regulation, mutual calibration, and built discernment.
