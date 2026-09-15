# RVT — Interpretive Structure and Corrigibility v0.01

**Status:** candidate RVT mechanism / unvalidated working note  
**Date:** 2026-09-15  
**Project:** Relational Viability Theory (RVT)  
**Epistemic status:** exploratory. This note records a candidate mechanism that should be stress-tested before incorporation into the RVT core.

---

## 1. Motivation

RVT currently asks how relational exchange reshapes the conditions of future viable exchange and action.

A further candidate mechanism has emerged:

> **Relations may change not only what is possible next, but what participants can recognize as possible, evidential, threatening, corrective, or worth attempting.**

This suggests that relational history may alter future viability partly by altering the interpretive structures through which later events are perceived.

This is not a claim that all cognition is relational, that all interpretation is socially produced, or that every bias is an RVT phenomenon. The narrower hypothesis is that **some relational histories causally modify interpretive structures, and those modified structures can alter later action and viability.**

---

## 2. Extend the state description

Let the relational state be augmented from

\[
Z_t=(X_t,R_t,H_t,\theta_t)
\]

to

\[
\boxed{
Z_t=(X_t,R_t,H_t,M_t,\theta_t)
}
\]

where:

- \(X_t\): constituent states;
- \(R_t\): relational/exchange architecture;
- \(H_t\): accumulated history relevant to future dynamics;
- \(M_t\): interpretive structure or model through which observations, alternatives, threats, and corrections are assigned meaning;
- \(\theta_t\): environment/exogenous conditions.

\(M_t\) is analytical, not metaphysical. Depending on the domain it may be implemented as beliefs, priors, learned policies, institutional categories, norms, threat models, schemas, role expectations, or other state variables that affect interpretation.

---

## 3. Observation is not yet effective evidence

Let \(y_t\) denote an observation or event encountered by the system.

The agent may not act directly on \(y_t\). Instead:

\[
\boxed{
\hat y_t=\Phi(y_t;M_t,R_t,H_t)
}
\]

where \(\hat y_t\) is the observation as interpreted.

Action may then depend on the interpreted observation:

\[
\boxed{
a_t=\pi(X_t,R_t,H_t,M_t,\hat y_t,\theta_t)
}
\]

followed by exchange:

\[
e_t=\mathcal E(X_t,R_t,a_t,\theta_t,\xi_t).
\]

This yields a candidate interpretive-action loop:

\[
\boxed{
M_t
\rightarrow
\Phi_t(y_t)
\rightarrow
a_t
\rightarrow
e_t
\rightarrow
(X_{t+1},R_{t+1},H_{t+1})
\rightarrow
M_{t+1}.
}
\]

The important point is that the interpretive structure may both shape action and itself be modified by the relational consequences of action.

---

## 4. Interpretive update

A generic update is:

\[
\boxed{
M_{t+1}=F_M(M_t,R_t,H_t,e_t,y_t,\theta_t).
}
\]

This permits several cases:

1. **ordinary learning** — evidence revises the model;
2. **relational learning** — what happens in the relation changes how later evidence is interpreted;
3. **self-sealing interpretation** — observations are repeatedly translated into support for the current frame;
4. **corrective opening** — anomalies remain able to alter the frame itself.

The theory should not assume in advance that update is Bayesian, rational, conscious, or verbally accessible.

---

## 5. The self-confirming loop

A frame may become self-reinforcing without deception or malicious intent.

The generic structure is:

\[
\boxed{
M_t
\rightarrow
\text{interpretation}
\rightarrow
\text{action}
\rightarrow
\text{world partly reshaped}
\rightarrow
\text{new observations}
\rightarrow
M_{t+1}.
}
\]

The risk is deeper than selective attention.

The frame may influence **what an observation is allowed to mean** before conscious judgment occurs.

Thus a system can remain sincere while becoming epistemically self-sealing.

A useful diagnostic question is:

> **Where in this system can an observation acquire the meaning “our frame is wrong”?**

If no live pathway exists, access to more data alone may not restore truth-responsiveness.

---

## 6. Correction accessibility

Define, provisionally, a correction set:

\[
\boxed{
\mathcal C_t(M)
=
\{y:\ y\text{ could be received as legitimate evidence against }M\}.
}
\]

This object is conceptual and requires domain-specific operationalization.

A truth-responsive interpretive structure requires at minimum:

\[
\mathcal C_t(M)\neq\varnothing.
\]

A strongly self-sealing structure approaches:

\[
\boxed{
\mathcal C_t(M)\rightarrow\varnothing.
}
\]

This need not mean that contradictory observations disappear. They may remain physically available while becoming semantically neutralized, discredited, reclassified, or rendered too costly to express.

---

## 7. Corrigibility as a relational achievement

Relations can alter the effective accessibility of correction.

A punitive history may produce:

\[
\text{correction attempt}
\rightarrow
\text{punishment / humiliation / abandonment / status loss}
\rightarrow
\text{reduced future anomaly expression}
\]

so that:

\[
\boxed{
\mathcal C_{t+1}^{\mathrm{accessible}}\downarrow.
}
\]

Conversely, if disagreement is truthfully received and the relation survives, then:

\[
\text{correction}
\rightarrow
\text{survivable disagreement}
\rightarrow
\text{greater future anomaly expression}
\]

and potentially:

\[
\boxed{
\mathcal C_{t+1}^{\mathrm{accessible}}\uparrow.
}
\]

This yields the candidate proposition:

\[
\boxed{
\textbf{Corrigibility can be an earned relational state.}
}
\]

A system cannot establish realized corrigibility merely by declaring itself open to correction.

\[
\boxed{
\text{declared corrigibility}\neq\text{earned corrigibility}.
}
\]

The test is what happens when correction becomes costly.

---

## 8. History can alter what counts as possible

Relational history may also affect perceived actionability.

Distinguish:

\[
A_F=\text{physically feasible actions}
\]

\[
A_R=\text{reachable actions}
\]

and provisionally:

\[
\boxed{
A_P=\text{actions represented by the system as live possibilities}.
}
\]

An action may belong to \(A_F\cap A_R\) while being absent from \(A_P\).

Likewise, a dangerous action may appear uniquely necessary if alternatives are no longer represented as viable or legitimate.

This gives a second pathway from history to future viability:

\[
\boxed{
H_t
\rightarrow
M_t
\rightarrow
A_{P,t}
\rightarrow
a_t
\rightarrow
\mathfrak V_{t+1}.
}
\]

RVT may therefore need to distinguish **actual viable possibility** from **recognized viable possibility** in domains where participant interpretation affects action selection.

---

## 9. Scars as active history

The phrase “we survived, but we carry the scars” suggests a useful RVT distinction.

A scar is not only a record that something happened.

It is:

\[
\boxed{
\text{past interaction incorporated into present structure}.
}
\]

History matters when yesterday changes the structure through which tomorrow becomes possible.

Some scars may be physical, institutional, relational, or interpretive.

Thus:

\[
H_t\rightarrow X_t,
\qquad
H_t\rightarrow R_t,
\qquad
H_t\rightarrow M_t.
\]

A historically adaptive interpretive structure may later become viability-reducing in a changed environment:

\[
\boxed{
\text{historically adaptive}\centernot\Rightarrow\text{currently viability-enhancing}.
}
\]

This should be tested, not assumed, in any domain.

---

## 10. Triangulation and redundant traces

A working methodological intuition is that real structures often leave multiple traces.

However, apparent redundancy is weak if every trace passes through the same interpretive decoder.

Suppose reality produces observations:

\[
y_t^{(1)},y_t^{(2)},\ldots,y_t^{(n)}.
\]

If each is processed through the same frame:

\[
\Phi(y^{(1)}),\Phi(y^{(2)}),\ldots,\Phi(y^{(n)}),
\]

then multiple observations may still collapse into one interpretive pathway.

Hence:

\[
\boxed{
\textbf{Reality may be redundant, but interpretation can collapse the redundancy.}
}
\]

Useful triangulation therefore requires at least partial independence among observational or interpretive pathways:

\[
\Phi_1(y^{(1)}),\Phi_2(y^{(2)}),\ldots,\Phi_k(y^{(k)}).
\]

Possible sources of independence include different observers, methods, scales, time periods, disciplines, causal consequences, or measurement systems.

Divergence among channels should not automatically be averaged away; it may reveal that one interpretive map is malformed.

---

## 11. The pasta story as an epistemic example

A simple personal example motivated this mechanism.

A person repeatedly experienced stomach pain after eating pasta and came to assume that pasta simply caused stomach pain for everyone. Later observations were interpreted through that frame:

- stomach pain after pasta confirmed the model;
- hearing that someone “ate too much” and had stomach pain could be interpreted as confirming the model;
- continued pasta consumption could be explained by the fact that pasta was delicious enough to justify the expected pain.

Nothing malicious was required.

The interpretive frame assigned meaning to observations in a way that repeatedly returned support to itself.

The important lesson is not medical. The example does **not** establish a causal diagnosis.

Its epistemic value is this:

\[
\boxed{
\textbf{An observer can sincerely inhabit a false model so completely that ordinary evidence is translated into confirmation.}
}
\]

A later contrast case — eating a different kind of pasta while expecting pain and repeatedly not experiencing it — functions as a prediction-error pathway that can begin to revise the prior model.

This is a candidate example of why correction may require not only more observations, but observations that can reach the model through a pathway the model cannot already neutralize.

---

## 12. Candidate RVT proposition

The strongest current formulation is:

> **Relational history can reshape future viability partly by altering the interpretive structures through which participants perceive evidence, alternatives, threats, and possibilities.**

A corresponding danger case is:

\[
\boxed{
\textbf{A relation becomes epistemically self-sealing when its history progressively destroys or neutralizes the pathways by which reality could correct the frame governing the relation.}
}
\]

A candidate healthy counterpart is:

\[
\boxed{
\textbf{A viable relation preserves or expands pathways through which reality can revise the relation's own interpretation of itself.}
}
\]

This should not yet be treated as a universal criterion of viability. Some viable systems may not contain agents, interpretation, or corrigibility in any meaningful sense. The proposition applies only where an interpretive layer is causally relevant.

---

## 13. Relation to RVT core

This mechanism fits the existing RVT structure:

\[
R_t
\rightarrow
e_t
\rightarrow
(X_{t+1},H_{t+1})
\rightarrow
R_{t+1}
\rightarrow
\mathfrak V_{t+1}
\]

by adding an interpretive pathway:

\[
\boxed{
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
}
\]

This is a proposed mechanism inside RVT, not a replacement for RVT and not a claim that all RVT applications require \(M_t\).

---

## 14. Falsification / shrinkage conditions

This mechanism should be weakened or rejected where:

1. \(M_t\) adds no predictive or causal value beyond ordinary state variables;
2. apparent interpretive effects are fully explained by fixed individual traits unrelated to relational history;
3. interventions on relational history do not change later interpretation, correction accessibility, or action selection;
4. the proposed correction-set language cannot be operationalized in a domain without becoming metaphorical;
5. alternative established frameworks explain the same effects more cleanly with no useful gain from an RVT decomposition.

The burden is therefore not to show that “frames matter,” but to show a specifically relational pathway:

\[
\boxed{
\text{relational exchange/history}
\rightarrow
\text{changed interpretive structure}
\rightarrow
\text{changed future action/viability}.
}
\]

---

## 15. Compact formulations to preserve

> **Relations can change not only the terrain, but what participants can see of the terrain.**

> **Reality may be redundant, but interpretation can collapse the redundancy.**

> **Corrigibility can be an earned relational state.**

> **A relation becomes epistemically dangerous when its own history progressively removes the routes by which reality could tell it that its frame is wrong.**

> **History matters when what happened yesterday changes the structure through which tomorrow becomes possible.**

---

## 16. Next test

Before incorporation into the RVT candidate theory, stress-test the mechanism against heterogeneous cases without forcing structural identity:

- the pasta normalized-anomaly example;
- a case where scarcity or disruption leaves persistent interpretive priors after the original conditions end;
- an institution where costly dissent reduces future anomaly expression;
- a relation where correction-survivability increases future truth access;
- an AI-human interaction where model authority alters independent verification.

The mechanism survives only if these cases share more than metaphor and if the relational-history pathway can be operationalized independently of the desired conclusion.
