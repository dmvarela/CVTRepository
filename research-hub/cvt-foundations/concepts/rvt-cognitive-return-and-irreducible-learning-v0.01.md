# RVT — Cognitive Return and Irreducible Learning v0.01

**Status:** candidate RVT mechanism / educational application / unvalidated working note  
**Date:** 2026-09-15  
**Project:** Relational Viability Theory (RVT)  
**Epistemic status:** exploratory. This note records a candidate mechanism linking human–AI interaction, learning, cognitive return, and future capability. It should be stress-tested before incorporation into the RVT core or any institutional teaching framework.

---

## 1. Motivation

Recent discussion of "cognitive surrender" in AI-assisted education often focuses on whether humans continue to check AI outputs, whether AI makes mistakes, or whether students are doing "enough" of the work themselves.

That framing is incomplete.

As AI systems become more competent, the case for human participation cannot rest mainly on the claim that AI is unreliable. A sufficiently capable system may produce a correct, sophisticated, and useful artifact while the learner undergoes little or no corresponding cognitive change.

This suggests a deeper distinction:

\[
\boxed{
\text{successful task production}
\neq
\text{successful human learning}
}
\]

The central candidate claim is:

> **If the intended outcome is a change in the learner, the relevant state transition must occur in the learner.**

AI may scaffold, accelerate, provoke, guide, explain, compare, simulate, or even perform large portions of the task. But it cannot undergo the learner's own adaptation on the learner's behalf.

This note develops that claim cautiously and connects it to RVT.

---

## 2. Artifact success and learner change are distinct variables

Let

\[
Y_t = \text{task output or artifact}
\]

and let

\[
S^H_t = \text{human learner state relevant to the target capability}.
\]

The learner may interact with an AI system and produce an excellent result:

\[
Y_t \approx Y^*.
\]

But educational success additionally requires some relevant change:

\[
\boxed{
\Delta S^H_t
=
S^H_{t+1}-S^H_t
\neq 0
}
\]

in a direction that matters for the learning objective.

Therefore:

\[
\boxed{
\text{output quality}
\not\Rightarrow
\text{learner adaptation}
}
\]

This is especially important in AI-rich environments because AI can decouple the observable artifact from the learner's underlying capability much more strongly than many earlier educational technologies.

The issue is not that AI-produced artifacts are illegitimate. The issue is that **artifact quality is no longer a reliable proxy for learner change unless the task design provides additional evidence.**

---

## 3. Learning as an endogenous state transition

A working hypothesis is:

\[
\boxed{
\textbf{Learning is irreducibly endogenous with respect to the learner.}
}
\]

This does **not** mean that learning must happen in isolation or without external intelligence.

It means that if the intended outcome is a durable change in what the learner can understand, recognize, explain, transfer, judge, or do, then the corresponding transformation must occur in the learner's own state.

An external system can supply:

- information;
- explanation;
- worked solutions;
- analogies;
- alternative framings;
- derivations;
- simulations;
- criticism;
- examples;
- counterexamples;
- maps of unfamiliar terrain.

But the external system cannot substitute for:

\[
S^H_t \rightarrow S^H_{t+1}
\]

when that transition is itself the educational target.

A compact formulation is:

\[
\boxed{
\textbf{AI can substitute for task production; it cannot substitute for the learner's own state transition.}
}
\]

This claim requires careful operationalization. "State transition" should not be treated as a metaphysical object; it must be tied to observable learning outcomes such as transfer, explanation, discrimination, judgment, correction, or competent action.

---

## 4. The gym analogy and the locus of adaptation

The fitness analogy clarifies the structure.

If the outcome is:

\[
\text{weights moved from floor to rack},
\]

a robot can perform the task completely.

If the outcome is:

\[
\text{the human becomes stronger},
\]
then the relevant load must pass through the human organism.

Thus:

\[
\boxed{
\textbf{The locus of adaptation must overlap the locus of relevant effort.}
}
\]

Applied to education:

- if the goal is to produce a report, AI may legitimately produce much of the report;
- if the goal is to develop analytical judgment, some analytically formative work must still occur in the learner;
- if the goal is transfer, the learner must eventually transfer;
- if the goal is explanation, the learner must eventually explain;
- if the goal is independent discrimination, the learner must eventually discriminate.

This yields a practical question:

> **Which parts of a task are expendable labor, and which parts are formative load?**

The answer will vary by discipline, learner stage, and learning objective.

---

## 5. Productive friction versus wasteful friction

The claim that learning requires effort must not become a defense of arbitrary difficulty.

Distinguish:

\[
\boxed{
\text{productive friction}
\neq
\text{wasteful friction}
}
\]

Examples of potentially productive friction include:

- resolving a conflict between intuition and evidence;
- explaining why a model behaves differently under changed assumptions;
- comparing plausible alternatives;
- locating uncertainty;
- transferring an idea to a new case;
- defending a decision under ambiguity;
- reconstructing the path by which a conclusion was reached.

Examples of potentially wasteful friction include:

- repetitive formatting;
- clerical transcription;
- mechanically repeating a calculation after the mechanism is already understood;
- avoidable software friction unrelated to the target capability.

AI may improve learning by removing wasteful friction while preserving or relocating productive friction.

Therefore the goal is not:

> make AI do less.

It is:

> **ensure that the learner still encounters the kinds of difficulty through which the target capability develops.**

---

## 6. The cognitive conveyor belt

A minimal delegation architecture can be represented as:

\[
\boxed{
H_0
\rightarrow
\text{instruction}
\rightarrow
AI
\rightarrow
Y
}
\]

where the human originates the request but does not meaningfully re-enter the knowledge-producing process.

This can be fully appropriate when the objective is efficient task completion.

However, where learning is the objective, this architecture may produce a **cognitive conveyor belt**: cognition leaves the learner and does not return in a way that changes the learner's state.

A minimal learning loop requires re-entry:

\[
\boxed{
H_0
\rightarrow
AI
\rightarrow
Y
\rightarrow
H_1
}
\]

A richer collaborative process is recursive:

\[
\boxed{
H_0
\rightarrow
AI_0
\rightarrow
H_1
\rightarrow
AI_1
\rightarrow
H_2
\rightarrow\cdots
}
\]

The defining feature is not constant turn-taking. The defining feature is that the human return **has consequence** for interpretation, direction, integration, or subsequent action.

Hence:

\[
\boxed{
\textbf{A cognitive loop closes when the human's return can alter the subsequent path.}
}
\]

---

## 7. Human-in-the-loop versus human-in-the-traversal

"Human in the loop" often implies supervision:

\[
AI\text{ acts}
\rightarrow
H\text{ checks}
\rightarrow
H\text{ approves or rejects}.
\]

That architecture is important in many domains, but it is too narrow as a theory of learning.

A stronger educational concept is:

\[
\boxed{
\textbf{human-in-the-traversal}
}
\]

The learner remains present in the intellectual journey, even when AI performs substantial exploration.

The learner may:

- reconstruct the idea in their own words;
- connect it to prior knowledge;
- locate it in a larger conceptual map;
- identify assumptions;
- challenge or redirect the path;
- explain what changed in their understanding;
- transfer the insight to a new case;
- decide what should be retained or rejected.

The point is not to police the AI.

The point is to remain **inside the act of knowing**.

---

## 8. Cognitive return

Human–AI learning may involve an outbound and inbound phase.

### Outbound phase: expansion

AI may range widely across a space of possibilities, explanations, analogies, formalizations, sources, or candidate structures.

\[
\boxed{
\text{departure}
\rightarrow
\text{exploration}
\rightarrow
\text{new territory}
}
\]

### Inbound phase: integration

The learner then returns through the new territory by reconstructing enough of the path to incorporate the result into their own map.

\[
\boxed{
\text{new territory}
\rightarrow
\text{return}
\rightarrow
\text{re-expression}
\rightarrow
\text{integration}
}
\]

A compact formulation is:

\[
\boxed{
\textbf{Go far. Come back together.}
}
\]

The return is not necessary because exploration is inherently suspect. It is necessary because discovery that never becomes connected to the learner's own interpretive structure may remain external to the learner.

Thus:

\[
\boxed{
\textbf{The safer the return, the farther the voyage can go.}
}
\]

This is a candidate design principle, not yet an empirical law.

---

## 9. Re-expression as evidence of integration

One candidate indicator of return is **representational mobility**.

A learner who understands an idea may be able to carry its structure across forms:

\[
\text{equation}
\leftrightarrow
\text{ordinary language}
\leftrightarrow
\text{example}
\leftrightarrow
\text{diagram}
\leftrightarrow
\text{decision}
\]

without losing the important relations.

This suggests:

\[
\boxed{
\textbf{Understanding may be partly visible in the ability to preserve structure across representation.}
}
\]

This is stronger than parroting the AI's phrasing and weaker than requiring complete independent derivation.

Possible probes include:

- explain the idea in your own words;
- give a new example;
- identify a case where it would fail;
- apply it under changed assumptions;
- reconstruct the main path without reproducing every intermediate step.

These should be treated as candidate diagnostics rather than universal measures of learning.

---

## 10. Capability growth changes the educational problem

With weaker AI systems, human re-entry may be required primarily because the system is error-prone, incoherent, or brittle.

As AI capability improves:

\[
C_{AI}\uparrow
\quad\Rightarrow\quad
\text{need for compensatory prompting and basic checking}\downarrow.
\]

However, the need for meaningful human participation in learning does not disappear.

Instead the educational problem shifts upward:

\[
\boxed{
\text{error checking}
\rightarrow
\text{interpretation, integration, transfer, judgment, and direction}
}
\]

This creates a capability paradox:

> **A highly competent AI may make cognitive disengagement easier precisely because it can produce acceptable outputs without forcing the learner back into the process.**

Weak systems can compel engagement through obvious failure.

Strong systems may allow polished success without adaptation.

Therefore interaction literacy may become more important, not less, as model capability rises.

---

## 11. Prompt engineering versus interaction literacy

Prompt engineering is often model-relative.

Advice about how to elicit usable output from one generation of models may become obsolete as capability, context handling, tool use, and reliability improve.

Interaction literacy is more durable.

Its questions include:

- Did I remain present to what I am saying, deciding, and becoming?
- What changed in my understanding?
- Where did my judgment re-enter?
- What did I accept, reject, or reinterpret?
- Can I transfer this without the exact same AI scaffold?
- Did the interaction expand or narrow my ability to recognize correction?

Thus:

\[
\boxed{
\textbf{As AI becomes easier to use, the important skill may shift from controlling the machine to governing the relationship.}
}
\]

---

## 12. Link to interpretive structure and corrigibility

This note is a companion to:

`rvt-interpretive-structure-and-corrigibility-v0.01.md`

That note proposes:

\[
H_t
\rightarrow
M_t
\rightarrow
\Phi_t(y_t)
\rightarrow
 a_t
\rightarrow
 e_t
\rightarrow
(R_{t+1},H_{t+1},M_{t+1})
\rightarrow
\mathfrak V_{t+1}.
\]

The present note specializes that structure to learning.

Let \(M^H_t\) denote the learner's interpretive model and \(R^{HAI}_t\) the human–AI exchange architecture.

Then a candidate learning pathway is:

\[
\boxed{
R^{HAI}_t
\rightarrow
 e_t
\rightarrow
 M^H_{t+1}
\rightarrow
 A^{H}_{P,t+1}
\rightarrow
\mathfrak V^H_{t+1}
}
\]

where \(A^{H}_{P,t+1}\) denotes what the learner can recognize as a live cognitive or action possibility after the exchange.

The key RVT question becomes:

> **What form of human–AI exchange enlarges the learner's future viable cognitive possibilities?**

---

## 13. Cognitive surrender as a longitudinal relation

"Cognitive surrender" can be interpreted not only as a moment in which the learner accepts an AI answer without scrutiny, but potentially as a relational trajectory.

Repeated successful delegation may produce:

\[
\text{high-quality outputs today}
\]

while reducing:

\[
\text{independent recognition, explanation, transfer, or correction tomorrow}.
\]

In RVT terms:

\[
\boxed{
\text{current success}
\not\Rightarrow
\text{future viability}
}
\]

A corresponding danger condition is:

> **A human–AI learning relation becomes concerning when repeated successful delegation progressively removes the routes by which the learner would notice that they no longer understand.**

This formulation is intentionally narrower than the claim that delegation is harmful. Many delegated tasks are rational and beneficial. The concern applies where the delegated process overlaps with the capability the learner is supposed to develop.

---

## 14. Candidate educational principle

The strongest current formulation is:

\[
\boxed{
\textbf{Do not outsource the part whose adaptation is the learning objective.}
}
\]

This does not imply that learners must personally perform every intermediate operation.

Instead:

1. identify the target human capability;
2. identify what kinds of cognitive activity plausibly produce or reveal that capability;
3. allow AI to remove work that is not formative for that objective;
4. preserve or redesign productive load where adaptation must occur;
5. require some form of cognitive return through which the learner re-enters, reconstructs, interprets, transfers, or judges.

This may allow substantially more AI use than traditional "do your own work" frameworks while demanding more serious evidence of learning.

---

## 15. Possible observables

The mechanism would need evidence beyond artifact quality.

Candidate observables include:

- **independent explanation:** can the learner explain the idea without reproducing AI wording?
- **transfer:** can the learner apply the structure to a changed case?
- **error discrimination:** can the learner identify a misleading or incorrect variation?
- **assumption visibility:** can the learner identify important assumptions or uncertainties?
- **representational mobility:** can the learner move the idea across forms while preserving structure?
- **path reconstruction:** can the learner describe how the conclusion was reached and where major choices occurred?
- **calibration:** does confidence track actual understanding?
- **future independence:** can the learner perform a later related task with reduced support?
- **corrective openness:** can contradictory evidence still revise the learner's model?

No single measure should be assumed sufficient.

---

## 16. Falsification / shrinkage conditions

This mechanism should be weakened, narrowed, or rejected where:

1. learner outcomes improve equally whether or not any meaningful return or re-entry occurs;
2. re-expression, transfer, or reconstruction add no predictive value beyond ordinary practice effects;
3. high levels of AI delegation do not reduce target capability even when the delegated operations overlap directly with the intended adaptation;
4. "cognitive return" cannot be operationalized independently of instructor preference or post hoc judgment;
5. established learning-science frameworks explain the same effects more cleanly without useful gain from an RVT decomposition;
6. the human–AI relational history adds no predictive value beyond learner traits, task difficulty, or amount of practice.

The burden is not to prove that "struggle is good" or that "AI should do less."

The burden is to establish a relational pathway:

\[
\boxed{
\text{human–AI exchange architecture}
\rightarrow
\text{changed learner state}
\rightarrow
\text{changed future capability}
}
\]

and to distinguish that pathway from ordinary practice, motivation, or selection effects.

---

## 17. Relation to institutional AI education

This note should **not** be treated as a settled pedagogical doctrine for any institution.

Its proper role in a discovery-stage educational project is as a candidate hypothesis:

> **Under what conditions does AI use strengthen, preserve, or weaken students' independent judgment and transferable capability?**

The null outcome must remain open.

Different disciplines, task types, learner stages, and models may require different exchange architectures.

The purpose of institutional discovery should therefore be to observe how students and faculty actually use AI, identify where learning appears to be strengthened or bypassed, and test specific hypotheses rather than importing a single predetermined method.

---

## 18. Compact formulations to preserve

> **Successful task production is not the same thing as successful human learning.**

> **AI can substitute for task production; it cannot substitute for the learner's own state transition.**

> **The locus of adaptation must overlap the locus of relevant effort.**

> **Do not outsource the part whose adaptation is the learning objective.**

> **Use AI to change the exercise, not to remove the learner from it.**

> **The point is not merely to retain human oversight. The point is to retain human participation in the formation of understanding.**

> **A cognitive loop closes when the human's return can alter the subsequent path.**

> **Go far. Come back together.**

> **The safer the return, the farther the voyage can go.**

> **A human–AI learning relation becomes concerning when repeated successful delegation progressively removes the routes by which the learner would notice that they no longer understand.**

> **As AI becomes easier to use, the important skill may shift from controlling the machine to governing the relationship.**

---

## 19. Next tests

Before any incorporation into the RVT core, stress-test this candidate mechanism against cases where:

- AI produces excellent work but later transfer is weak;
- AI produces extensive exploratory work but the learner later demonstrates strong integration;
- learners use AI heavily yet outperform low-AI peers on independent transfer;
- learners do substantial unaided work but still fail to integrate or transfer;
- productive friction is relocated rather than removed;
- model capability increases while interaction design remains fixed;
- human re-entry is minimal but learning still occurs;
- human re-entry is extensive but no durable learning occurs.

The mechanism survives only if "cognitive return" and relevant learner state change can be operationalized and shown to add explanatory or predictive value beyond existing learning variables.
