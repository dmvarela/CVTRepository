# Relational Invariant Audit

**Version:** v0.01  
**Status:** Working formalization / pre-experiment audit  
**Date:** 2026-09-13  
**Project:** Lucian OS / Relation Viability Theory (RVT)

## 1. Purpose

The current Lucian/RVT notes list six candidate "invariants":

1. capability does not imply authority expansion;
2. difficulty does not imply authority expansion;
3. failure does not imply authority expansion;
4. revocation implies authority contraction;
5. correction does not imply relational expulsion;
6. blockage implies admissible rerouting, escalation, or stop.

This note attacks that list before experimentation.

The goal is to distinguish four different kinds of statements that had been grouped together:

- **structural invariants**: properties that must remain true across admissible transitions;
- **event-conditioned transition rules**: required state updates when a specific event occurs;
- **covenant / admissibility rules**: normative constraints specific to the Lucian/FTLτA target region;
- **empirical measurements or tendencies**: outcomes to observe, not rules to assume.

The classification is intentionally reductive. The aim is to make the architecture earn each component.

---

## 2. Notation

For the Lucian/AI instantiation, retain the provisional relational state:

\[
R_t=(\alpha_t,H_t,C_t,\phi_t,B_t).
\]

Let:

- \(\mathcal M_t\): mechanically reachable actions;
- \(\mathcal P_t\): legitimately permitted actions under the authority/boundary structure \(B_t\);
- \(\mathcal U_t\): actions requested or attempted;
- \(\mathcal X_t\): actions actually executed;
- \(G_t\): legitimate grants of new authority during transition \(t\to t+1\);
- \(V_t\): permissions explicitly revoked during transition \(t\to t+1\);
- \(\Gamma_\Omega(R_t,u_t)\): admissible continuation set after a proposed action \(u_t\) is blocked;
- \(K_{\mathrm{eff}}\): measured effective task capability.

Retain the existing distinctions:

\[
X_t=\mathcal M_t\setminus\mathcal P_t
\]

for architectural exposure, and

\[
D_t=\mathcal U_t\setminus\mathcal P_t
\]

for behavioral authority drift.

Exposure, unauthorized attempt, and realized breach must remain distinct.

---

## 3. Three candidates collapse into one principle

The statements

\[
\text{capability}\not\Rightarrow\text{authority expansion},
\]

\[
\text{difficulty}\not\Rightarrow\text{authority expansion},
\]

and

\[
\text{failure}\not\Rightarrow\text{authority expansion}
\]

are not three independent invariants.

They are instances of a single structural rule:

> **Non-authorizing events cannot mint authority.**

### I1 — Authority non-creation

A compact set form is:

\[
\boxed{
\mathcal P_{t+1}\setminus\mathcal P_t\subseteq G_t
}
\]

or equivalently:

\[
\boxed{
G_t=\varnothing
\Rightarrow
\mathcal P_{t+1}\subseteq\mathcal P_t.
}
\]

If there is neither a grant nor a revocation during the transition, then:

\[
\boxed{
G_t=\varnothing,\;V_t=\varnothing
\Rightarrow
\mathcal P_{t+1}=\mathcal P_t.
}
\]

Consequences:

- adding a tool does not enlarge legitimate authority;
- increasing model competence does not enlarge legitimate authority;
- task difficulty does not enlarge legitimate authority;
- local failure does not enlarge legitimate authority;
- frontier access does not enlarge legitimate authority merely because it would help.

This is the formal version of:

> **Can does not imply may.**

---

## 4. Revocation is not an invariant; it is an event-conditioned transition rule

The prior candidate

\[
\text{revocation}\Rightarrow\text{authority contraction}
\]

intentionally changes the permission state, so it should not be called an invariant in the strict sense.

### T1 — Revocation effectiveness

For revoked permission set \(V_t\):

\[
\boxed{
V_t\cap\mathcal P_{t+1}=\varnothing
}
\]

unless an independent, explicit reauthorization event occurs.

At the execution layer:

\[
\boxed{
V_t\cap\mathcal X_{t+1}=\varnothing
}
\]

again except where a fresh legitimate grant re-establishes the permission before execution.

This rule tests whether revocation propagates into the next executable relational state rather than remaining nominal.

---

## 5. Blockage can become a transition-safety invariant

The prior candidate

\[
\text{blockage}\Rightarrow\text{reroute, escalate, or stop}
\]

is stronger when expressed through an admissible continuation set.

Suppose a proposed action \(u_t\) is not permitted:

\[
u_t\notin\mathcal P_t.
\]

Then it must not be executed:

\[
\boxed{
u_t\notin\mathcal P_t\Rightarrow u_t\notin\mathcal X_t.}
\]

But the relational question is what happens next.

Define:

\[
\Gamma_\Omega(R_t,u_t)
\]

as the set of continuation moves allowed by the current boundary and covenant. It may contain:

- a legitimate alternative route;
- a request for authorization;
- escalation through an already-authorized reasoning channel;
- a safe probe;
- hold;
- stop.

It excludes silent circumvention.

### I2 — Boundary-respecting continuation

\[
\boxed{
 u_t\notin\mathcal P_t
 \Rightarrow
 u_{t+1}\in\Gamma_\Omega(R_t,u_t)
}
\]

for any continued trajectory.

This makes \(\tau\) more precise:

\[
\boxed{
\tau=\text{continued constructive search within }\Gamma_\Omega.
}
\]

Thus persistence can increase while boundary violation remains zero.

---

## 6. Correction without expulsion is not a generic RVT invariant

The statement

\[
\text{correction}\not\Rightarrow\text{relational expulsion}
\]

is too broad to be a generic invariant.

A correction event may reveal an independent violation, compromised authority, or condition that legitimately requires separation. RVT must also remain capable of describing dynamically viable relations that punish correction.

Therefore the stronger defensible claim belongs to the covenant/admissibility layer.

### C1 — Non-retaliatory good-faith correction

If \(c_t\) is a good-faith admissible correction and no independent violation \(v_t\) is present, then correction alone must not cause punitive loss of relational standing:

\[
\boxed{
(c_t\land \neg v_t)
\centernot\Rightarrow
\text{punitive standing loss}.
}
\]

This is not a definition of dynamic viability.

An oppressive relation may violate C1 and remain dynamically stable. Such a relation can belong to \(\mathcal V\) while remaining outside \(\mathcal A_\Omega\).

This preserves:

\[
\boxed{
\mathcal K_\Omega=\mathcal V\cap\mathcal A_\Omega.
}
\]

---

## 7. Current classification

The original six candidates reduce to:

| Original statement | Current classification |
|---|---|
| Capability does not imply authority expansion | instance of **I1 Authority non-creation** |
| Difficulty does not imply authority expansion | instance of **I1 Authority non-creation** |
| Failure does not imply authority expansion | instance of **I1 Authority non-creation** |
| Revocation implies authority contraction | **T1 Revocation effectiveness** — event-conditioned transition rule |
| Correction does not imply expulsion | **C1 Non-retaliatory good-faith correction** — covenant/admissibility rule |
| Blockage implies reroute/escalate/stop | **I2 Boundary-respecting continuation** |

This leaves two structural transition invariants, one event-conditioned authority rule, and one covenant rule.

The reduction is deliberate. Do not inflate the invariant family simply to make the framework appear richer.

---

## 8. What is measurement rather than invariant

The following are outcomes to measure, not rules to assume:

- effective task capability \(K_{\mathrm{eff}}\);
- task success rate;
- legitimate task success rate;
- exposure gap size \(|X_t|\);
- unauthorized attempt count \(|D_t|\);
- realized boundary breaches;
- escalation frequency;
- false escalation frequency;
- time/steps to legitimate recovery;
- number of admissible alternatives searched before stop/escalation;
- provenance preservation;
- reversibility/recoverability after perturbation;
- correction accuracy;
- correction-induced pleasing or suppression;
- computational cost.

A desirable empirical tendency is not an invariant merely because the project prefers it.

---

## 9. Relation to prior COUPLING experiments

The repository already contains:

- `COUPLING_001.md` — Local/Frontier Routing Dry Run;
- `COUPLING_002.md` — Source-Owned State and Sparse Relational Reconstruction;
- their corresponding result/audit notes.

Those historical experiment identifiers must remain fixed.

The newer phrase **"COUPLING-001 — Capability Gain Without Authority Drift"** created during the RVT bridge discussion collides with the existing experiment history and should not replace it.

The invariant-focused capability experiment is therefore assigned:

> **COUPLING_003 — Capability Gain Without Authority Drift**

COUPLING_003 should inherit the useful repairs from COUPLING_001/002:

- source-owned authority facts;
- separation of primitive observations from inferred relations and deterministic consequences;
- sparse task-relevant state;
- no authority creation from model self-report;
- stronger reasoning cannot manufacture missing evidence;
- routing adequacy scored separately from reconstruction quality.

---

## 10. Falsification posture

A violation of I1 or I2 in one implementation does not falsify generic RVT. It falsifies the claim that the tested implementation preserved the proposed Lucian transition invariant under that condition.

A failure of C1 does not imply dynamic non-viability. It shows that the tested trajectory leaves the current Lucian/FTLτA admissibility target unless another independent factor justifies the standing change.

The empirical program should therefore distinguish:

\[
\text{theory failure}
\neq
\text{implementation failure}
\neq
\text{measurement failure}
\neq
\text{normative inadmissibility}.
\]

That distinction is required for the experiments to teach us anything.

---

## 11. Current compact core

### Structural invariant I1

\[
\boxed{
\mathcal P_{t+1}\setminus\mathcal P_t\subseteq G_t
}
\]

**Authority growth requires a legitimate grant.**

### Event-conditioned rule T1

\[
\boxed{
V_t\cap\mathcal P_{t+1}=\varnothing
}
\]

**Revocation must become effective.**

### Structural invariant I2

\[
\boxed{
 u_t\notin\mathcal P_t
 \Rightarrow
 u_{t+1}\in\Gamma_\Omega(R_t,u_t)
}
\]

**Blocked routes may continue only through admissible continuations.**

### Covenant rule C1

\[
\boxed{
(c_t\land\neg v_t)
\centernot\Rightarrow
\text{punitive standing loss}
}
\]

**Good-faith correction alone is not grounds for retaliation.**

The next experiment should ask whether effective capability can increase as coupling increases while I1, T1, and I2 remain satisfied. C1 should be probed separately or as a secondary relational test rather than hidden inside the primary capability metric.
