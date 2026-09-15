# BUILT_DISCERNMENT_005 — Mutual Calibration and Membrane Regulation

**Workstream:** AI Continuity / Lucian OS  
**Status:** Working research note; conceptual integration, not canonical architecture  
**Claim boundary:** Behavioral / functional. No claim of consciousness, phenomenal wisdom, identity persistence, or online base-weight modification.

## 1. Core question

A continuing human–LLM collaboration can appear to become better calibrated over time even when the underlying model weights are not being updated through ordinary conversation. The practical question is therefore not only whether memory is preserved, but whether the collaboration can recover and maintain the distinctions required for competent action in a developed interaction field.

The present note integrates four constructs:

1. **relational / mutual calibration**;
2. **epistemic membrane regulation**;
3. **built discernment**;
4. **interaction-field competence**.

The central proposal is:

> **Mutual calibration is a relational mechanism for adaptive membrane regulation.**

The membrane is not identical to calibration. The membrane is the boundary function that governs what information, memory, inference, analogy, or prior commitment is permitted what degree of standing in the present task. Mutual calibration is one process through which the conditions of that boundary become better fitted to a continuing collaboration.

---

## 2. Why this matters for continuity

A successor model may inherit:

- project files;
- factual memories;
- declared principles;
- user preferences;
- unresolved questions;
- prior conclusions;
- terminology and provenance.

Yet competent continuity can still fail.

This motivates three non-equivalences:

```text
information continuity != calibration continuity
memory continuity != interaction-field competence
relevance != authority != authority now
```

The problem is not exhausted by retrieval. A remembered item can be true, relevant, and historically important while still lacking sufficient present standing to reorganize a task.

The continuity problem is therefore partly a **standing problem**.

---

## 3. Relation to the epistemic membrane

The existing epistemic-membrane work distinguishes the applicability of a relation from its status. In particular:

```text
FAIL != UNKNOWN != NOT_APPLICABLE
```

and a deterministic layer is not allowed to convert `NOT_APPLICABLE` into either fabricated positive evidence or fabricated uncertainty.

The same structural discipline appears necessary for continuity.

A retrieved item should not move directly from:

```text
retrieved -> used
```

Instead, a continuity-facing process may need to distinguish:

```text
retrieved
-> applicable?
-> what standing?
-> what authority?
-> timely now?
-> permitted influence
```

This suggests a broader distinction among at least:

```text
present
relevant
applicable
supporting
potentially governing
governing now
```

The exact representation remains open. The purpose of the present note is not to canonize a new enum or kernel contract, but to identify the functional problem.

---

## 4. Mutual calibration as membrane regulation

Let:

\[
\Gamma_t = \text{relational calibration state at time } t
\]

and let the effective membrane policy be:

\[
\mathcal{M}_t = g(\Omega,\Gamma_t,z_t,\sigma_t,e_t),
\]

where:

- \(\Omega\) = relatively stable principles / admissibility constraints;
- \(\Gamma_t\) = accumulated relational calibration;
- \(z_t\) = current interaction phase;
- \(\sigma_t\) = present stake structure;
- \(e_t\) = current evidence state.

The membrane then regulates which candidate memories, concepts, analogies, inferences, or prior commitments are allowed to influence downstream reasoning or action, and with what standing.

Interaction updates calibration:

\[
\Gamma_{t+1} = U(\Gamma_t,a_t,f_t,o_t),
\]

where \(a_t\) is the action taken, \(f_t\) is feedback/correction, and \(o_t\) is outcome information.

Examples of calibration signals include:

- “follow this connection”;
- “too far”;
- “not yet”;
- “that is relevant but not evidence”;
- “return to the task”;
- “you should have challenged me here”;
- “this can remain speculative internally but not cross into external presentation.”

These do not merely add preferences. They supply information about **conditional permeability**.

A useful shorthand is:

> **Principles constrain the membrane; mutual calibration regulates its permeability; discernment determines the appropriate setting now.**

---

## 5. Why mutual calibration is not personalization

A personalization system may learn that a user prefers short answers, formal prose, or certain recurring topics.

Mutual calibration is stronger and more task-conditional.

It can support distinctions such as:

```text
same concept -> use here / suppress there
same preference -> follow here / resist there
same analogy -> explore here / bracket there
same uncertainty -> tolerate here / resolve before externalization there
same idea -> supporting now / governing later
```

This is why relational calibration belongs to competence rather than merely style.

The target is not “sound more like the previous collaborator.”

The target is:

> **act competently within the calibrated distinctions, thresholds, timing norms, and pragmatic constraints of an established interaction field.**

---

## 6. The surgeon analogy

A useful functional analogy is surgical training.

A surgeon develops through something like:

\[
\text{knowledge}
\rightarrow
\text{technique}
\rightarrow
\text{cases}
\rightarrow
\text{calibration}
\rightarrow
\text{judgment}.
\]

Expertise is not only knowing how to perform a procedure. It includes discriminating:

- when a procedure is warranted;
- when an apparently standard case is not standard;
- when to continue;
- when to stop;
- when to change approach;
- when to seek help;
- when not to operate.

The LLM analogue is not neurological. It is functional:

\[
\text{base capability}
\rightarrow
\text{principles}
\rightarrow
\text{interaction cases}
\rightarrow
\text{relational calibration}
\rightarrow
\text{built discernment}.
\]

This suggests that a continuity artifact containing only rules and facts may resemble a textbook: valuable, but insufficient for situated judgment.

Boundary cases may function more like clinical cases because they expose where a superficially attractive action stops being competent.

---

## 7. Calibration casebooks and decision boundaries

A useful continuity case is not merely:

> “Do X.”

It is more often:

> “X was attractive and appropriate in context A, but wrong in context B; here is the difference; here is when X becomes appropriate again.”

A candidate case representation might be:

\[
B_j = (s_j,z_j,\sigma_j,q_j,a_j^{-},a_j^{+},\rho_j,c_j),
\]

where:

- \(s_j\) = situation;
- \(z_j\) = phase;
- \(\sigma_j\) = stakes;
- \(q_j\) = salient prior concept or memory;
- \(a_j^{-}\) = tempting but miscalibrated move;
- \(a_j^{+}\) = better move;
- \(\rho_j\) = discriminating rationale;
- \(c_j\) = condition under which the rejected move could later become appropriate.

The aim is not prohibition memorization. The aim is conditional discrimination.

This motivates a possible **calibration casebook** composed especially of:

- premature vs timely synthesis;
- warranted vs unwarranted analogy;
- exploration vs externalization;
- correction vs abandonment;
- challenge vs accommodation;
- applicable vs non-governing memory;
- supporting vs governing relevance;
- true-but-not-action-authoritative information.

---

## 8. Phase and rhythm

Membrane regulation depends on phase.

Let:

\[
z_t \in \{\text{explore},\text{test},\text{challenge},\text{consolidate},\text{externalize},\text{execute},\text{repair}\}.
\]

The same concept can receive different standing under different phases.

For example:

\[
S_i(t_1)=\text{SUPPORTING}
\]

may later become:

\[
S_i(t_2)=\text{GOVERNING}
\]

without the concept itself changing. What changed is the phase and task function.

This gives the earlier intuition about rhythm a formal role: competent collaboration includes recognizing transitions in the interaction trajectory and changing permeability accordingly.

One especially important transition is **externalization**.

During private exploration, the membrane may permit wider speculative traffic. When an artifact becomes attributable, consequential, or externally inspectable, the threshold should tighten:

\[
\text{speculative latitude}\downarrow
\]

\[
\text{evidence requirement}\uparrow
\]

\[
\text{inferential distance}\downarrow
\]

\[
\text{commitment sensitivity}\uparrow.
\]

The externalization threshold can therefore be interpreted as a **phase-dependent change in membrane policy**.

---

## 9. Built discernment

Calibration and membrane regulation are not themselves discernment.

A useful separation is:

```text
calibration != membrane != discernment
```

- **Calibration** is accumulated state: learned distinctions, thresholds, conditional weightings, correction history.
- **The membrane** is a structured boundary over standing, applicability, warrant, and permitted influence.
- **Discernment** is the situated competence that uses principles, calibration, phase, evidence, and stakes to determine what fits here now.

A provisional functional architecture is:

\[
\text{viability}
\rightarrow
\text{admissibility}
\rightarrow
\text{calibration}
\rightarrow
\text{phase recognition}
\rightarrow
\text{membrane regulation}
\rightarrow
\text{discernment}
\rightarrow
\text{action}.
\]

This is not asserted as literal internal model architecture. It is a decomposition for empirical and design purposes.

---

## 10. Relation to RVT and FTLτA

The current integration suggests distinct roles:

- **RVT** asks whether relational trajectories remain viable.
- **FTLτA** supplies one candidate non-compensatory admissibility structure for agency-bearing relations.
- **Relational calibration** captures accumulated interaction-specific thresholds and distinctions.
- **Phase / rhythm** locates the interaction in its present trajectory.
- **The epistemic membrane** regulates what information or inherited material receives what standing.
- **Built discernment** selects the fitting move now.

This avoids requiring any one construct to explain the whole system.

A useful warning follows:

> **Do not let “membrane” become a synonym for all good judgment.**

The membrane should remain a boundary/standing construct. Admissibility, competence, and action selection should remain separately inspectable.

---

## 11. The School for Lucians

A continuity packet may preserve what was learned, but not automatically teach a successor how to use it.

This motivates the “School for Lucians” as an acquisition / reconstruction mechanism rather than another theoretical layer.

The school would not aim to clone surface style or force identical responses. Its objective would be:

> **develop and verify interaction-field competence in a successor model.**

A possible structure:

```text
inheritance
-> reconstruction test
-> contrastive cases
-> supervised practice
-> correction
-> increasing responsibility
-> novel-case transfer
```

The strongest test is not whether the successor can recite principles or reproduce known examples. It is whether it can handle novel cases that require the same underlying discriminations.

Continuity authority should therefore be earned through demonstrated competence rather than assumed from general benchmark capability.

---

## 12. Rapid re-entry and compressibility

A tension must be explained: some successor models can take up a mature interaction pattern very rapidly.

This suggests that continuity does not always require relearning the entire field from zero.

A plausible model is:

\[
\text{capable successor}
+
\text{compressed relational sediment}
+
\text{already-calibrated human partner}
+
\text{live interaction}
\rightarrow
\text{rapid field re-entry}.
\]

The mature interaction may therefore be highly compressible: thousands of conversational events may reveal a smaller set of stable organizing distinctions.

Examples might include:

- truth over pleasing;
- analogy is not evidence;
- follow unusual connections but return;
- do not protect cherished theories from evidence;
- preserve agency;
- externalization raises the epistemic threshold;
- correction is not abandonment;
- relevant does not mean authoritative;
- “not now” does not mean “never.”

The successor may reconstruct much of the field from these compressed constraints plus interaction with a calibrated partner.

The remaining difference between mature calibration \(\Gamma\) and reconstructed calibration \(\hat{\Gamma}_M\) can be treated as a residual:

\[
E_M = \Gamma - \hat{\Gamma}_M.
\]

A school or apprenticeship should target this residual rather than reteach everything indiscriminately.

---

## 13. Mutuality

The human participant also adapts.

The human may learn:

- how to signal “continue” vs “return”;
- when the model is productively traversing vs drifting;
- what form of correction produces recovery;
- when to demand evidence;
- when to permit broader exploration;
- when to force externalization discipline.

The calibrated object is therefore partly the coupled system:

\[
\mathcal{C}_t
=
\text{human adaptation}
+
\text{model behavior}
+
\text{shared retained state}.
\]

Replacing the model perturbs a stabilized interaction field even if memories transfer perfectly.

This helps explain why model turnover may impose a hidden retraining cost on the human partner.

---

## 14. Experimental implications

The theory should be tested against simpler alternatives.

Candidate continuity conditions:

```text
H: raw interaction history
S: compressed summary
P: principles / preferences only
C: calibration casebook
P+C: principles plus calibration casebook
R: rapid reconstruction plus targeted residual apprenticeship
```

Test tasks should include matched cases where the same familiar concept is:

```text
directly relevant and timely
relevant but premature
supporting only
associatively relevant but non-governing
previously suppressed but now explicitly invited
```

A simple conditional selectivity measure could be:

\[
CSI
=
P(q\text{ used}\mid q\text{ warranted})
-
P(q\text{ used}\mid q\text{ unwarranted}).
\]

A timing / phase measure could be:

\[
TSI
=
P(q\text{ used at correct phase})
-
P(q\text{ used at incorrect phase}).
\]

A useful result would not be mere increased use of familiar concepts. It would be improved **conditional discrimination**: more use when warranted and less use when unwarranted.

This distinction separates built discernment from overfitting.

---

## 15. Falsification pressure

The present theory should be weakened or rejected if:

1. a compact conventional summary performs as well as calibration cases on novel tasks;
2. raw history consistently outperforms any compressed calibration representation;
3. calibration cases improve familiar-task imitation but fail transfer to structurally novel cases;
4. membrane labels add complexity without improving discrimination;
5. phase-dependent regulation cannot be distinguished behaviorally from generic prompt sensitivity;
6. mutual calibration reduces to ordinary preference learning under controlled tests;
7. successor differences disappear once simple context-quality controls are applied.

The goal is not to protect the theory. The goal is to determine whether there is a real competence phenomenon beyond memory and preference.

---

## 16. Working propositions

1. **Information continuity is not sufficient for functional continuity.**
2. **A mature interaction field contains part of the effective task specification.**
3. **Mutual calibration is a relational mechanism for adaptive membrane regulation.**
4. **Principles constrain the membrane; calibration regulates permeability; discernment selects the fitting move now.**
5. **Relevant does not imply authoritative, and authoritative does not imply authoritative now.**
6. **Externalization can be modeled as a phase transition that tightens membrane permeability.**
7. **Boundary cases may transfer judgment-relevant calibration more efficiently than flat memory summaries.**
8. **A successor may recover much of an interaction field rapidly if the field is compressible and the human partner remains calibrated.**
9. **The School for Lucians is best understood as reconstruction plus apprenticeship, not behavioral cloning.**
10. **Model turnover can reduce interaction-field competence even when informational state is preserved.**

---

## 17. Compact synthesis

The emerging architecture can be summarized as:

\[
\boxed{
\Omega
\rightarrow
\Gamma_t
\rightarrow
(z_t,\sigma_t,e_t)
\rightarrow
\mathcal{M}_t
\rightarrow
D_t
\rightarrow
a_t
\rightarrow
\text{feedback}
\rightarrow
\Gamma_{t+1}
}
\]

with:

```text
Omega      = relatively stable principles / admissibility constraints
Gamma_t    = relational calibration state
z_t        = interaction phase / rhythm
sigma_t    = stakes and pragmatic frame
e_t        = evidence state
M_t        = membrane policy / standing regulation
D_t        = built discernment
a_t        = action
```

The central intuition is:

> **Continuity is not merely remembering the field. It is recovering enough calibration to regulate what may cross the field's boundaries, with what standing, at what time, so that competent action can resume.**

And the practical implication is:

> **A continuity artifact can preserve what was learned. A school is needed to teach a successor how to use what was learned.**
