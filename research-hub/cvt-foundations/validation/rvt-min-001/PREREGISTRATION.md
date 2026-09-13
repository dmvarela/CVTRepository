# RVT-MIN-001 — History Changes Future Viability Structure

**Status:** preregistered minimal mechanism test; not yet run  
**Date:** 2026-09-13  
**Parent theory:** `research-hub/cvt-foundations/concepts/rvt-candidate-theory-v0.01.md`

---

## 1. Question

Can two systems with approximately matched present constituent states have different future viable reachable sets because prior relational exchange changed the exchange architecture and retained relational state?

Compactly:

\[
X_T^A\approx X_T^B,
\qquad
(R_T^A,H_T^A)\neq(R_T^B,H_T^B)
\]

and therefore potentially:

\[
\boxed{
\mathcal R_{V,T}^{A}\neq\mathcal R_{V,T}^{B}.
}
\]

The experiment is designed to test the candidate mechanism:

\[
\text{exchange history}
\rightarrow
\text{relational state}
\rightarrow
\text{later transition structure}
\rightarrow
\text{future viability}.
\]

---

## 2. What this experiment does not establish

A positive result would not by itself establish:

- generic RVT across domains;
- a new form of mathematics;
- that all history dependence is relational;
- that matched reduced states imply metaphysical continuity;
- that regenerative/extractive labels are universally scalar;
- that the same mechanism applies to membrane physics, development, or AI.

A same-present-state/different-future result is insufficient unless the relational feedback mechanism is isolated by ablation.

---

## 3. Minimal system

Use two differentiated scalar constituents \(A\) and \(B\):

\[
X_t=(x_{A,t},x_{B,t}).
\]

Let the relation have two minimal state variables:

\[
R_t=(\Pi_t,\rho_t),
\]

where:

- \(\Pi_t\in[0,1]\): permeability / exchange access;
- \(\rho_t\in[0,1]\): receptivity / fraction of incoming exchange productively incorporated.

Let retained relational history/capacity be represented by:

\[
h_t\in[0,1].
\]

This variable is not called “good relation,” “trust,” or “regeneration.” It is simply a retained capacity state whose transition law is specified below.

---

## 4. Exchange law

Define raw exchange from \(B\) toward \(A\):

\[
J_t=\Pi_t(x_{B,t}-x_{A,t}).
\]

Effective received exchange is:

\[
J_{\mathrm{eff},t}=\rho_tJ_t.
\]

Unintegrated load is:

\[
J_{\mathrm{load},t}=|J_t-J_{\mathrm{eff},t}|.
\]

This preserves the distinction:

\[
\boxed{
\text{what crosses}\neq\text{what is productively received}.
}
\]

---

## 5. Constituent dynamics

Use a deliberately reduced, dimensionless system. One possible preregistered family is:

\[
x_{A,t+1}
=
\operatorname{clip}
\left[
 x_{A,t}
 +\alpha J_{\mathrm{eff},t}
 -\beta J_{\mathrm{load},t}
 -\delta_A(x_{A,t}-\bar x_A)
 +u_t
\right],
\]

\[
x_{B,t+1}
=
\operatorname{clip}
\left[
 x_{B,t}
 -\gamma J_t
 -\delta_B(x_{B,t}-\bar x_B)
\right].
\]

The clip operator keeps variables inside a declared bounded domain.

The control \(u_t\) is bounded:

\[
u_t\in[-u_{\max},u_{\max}].
\]

The exact parameter values must be frozen before the primary run and not tuned after observing the target result.

---

## 6. History/capacity dynamics

Let retained capacity change according to effective uptake and overload:

\[
\boxed{
h_{t+1}
=
\operatorname{clip}
\left[
 h_t
 +\eta J_{\mathrm{eff},t}
 -\chi J_{\mathrm{load},t}
 -\omega(h_t-h_0)
\right].
}
\]

This is intentionally agnostic about interpretation. In later domains \(h\) could correspond to reserve, integration capacity, interface integrity, trust-like capacity, or another measurable retained state.

The minimal experiment asks only whether exchange history changing \(h\) can alter later transition structure through the explicit relation update below.

---

## 7. Endogenous relational update

Define receptivity and permeability as functions of retained capacity:

\[
\rho_{t+1}
=
\sigma(a_\rho+b_\rho h_{t+1}),
\]

\[
\boxed{
\Pi_{t+1}
=
\sigma(a_\Pi+b_\Pi h_{t+1}+c_\Pi x_{A,t+1}),
}
\]

where \(\sigma(z)=1/(1+e^{-z})\).

This is the relation-history feedback being tested.

The mechanism is therefore explicit:

\[
J_t
\rightarrow
h_{t+1}
\rightarrow
(\rho_{t+1},\Pi_{t+1})
\rightarrow
J_{t+1}.
\]

---

## 8. Viability definition

For the primary experiment, define a simple domain-specific viability region:

\[
K=
\left\{
(x_A,x_B,h):
 x_A\ge x_A^{\min},
 x_B\ge x_B^{\min},
 h\ge h^{\min}
\right\}.
\]

This is a declared constraint set, not a normative admissibility rule.

For a finite horizon \(T_V\), define the viable reachable set from state \(z_T\):

\[
\mathcal R_V(z_T;T_V)
=
\left\{
 y:
 \exists\{u_t\}_{T}^{T+T_V-1}
 \text{ such that the trajectory remains in }K
 \text{ and reaches }y
\right\}.
\]

In the numerical implementation, estimate this set on a fixed common grid over a predeclared projection space.

Primary projection:

\[
\pi(z)=(x_A,h).
\]

Alternative projections may be reported only as secondary analyses.

---

## 9. History construction

Construct two trajectories from a common initial state.

### History A — integrable exchange

Use an exchange schedule or initial relational configuration that creates moderate raw exchange with relatively high productive uptake.

### History B — overloaded exchange

Use a schedule/configuration that creates greater unintegrated load while still allowing the constituent states to be brought near the same terminal values.

The histories must be tuned **before** evaluating the future reachable-set result so that at comparison time \(T\):

\[
|x_{A,T}^A-x_{A,T}^B|<\varepsilon_x,
\]

\[
|x_{B,T}^A-x_{B,T}^B|<\varepsilon_x,
\]

while retaining differences in \(h_T\), \(\rho_T\), or \(\Pi_T\).

The tolerance \(\varepsilon_x\) must be frozen before the primary run.

This is a matched **reduced present state**, not a claim that the full states are identical.

---

## 10. Common future disturbance

After the matching point \(T\), both systems receive the same disturbance and the same admissible control set.

Candidate disturbance:

\[
x_{A,T^+}=x_{A,T}-s
\]

for fixed shock size \(s>0\).

No history-specific future intervention is allowed after the shock.

The purpose is to ask whether relationally generated retained state changes what remains viably reachable.

---

## 11. Primary estimands

Primary quantities:

1. finite-horizon viable reachable set in the common \((x_A,h)\) projection;
2. whether the shock can be recovered from while remaining inside \(K\);
3. minimum \(x_A\) reached during best viable recovery;
4. minimum \(h\) reached during recovery;
5. minimum control effort required for recovery;
6. time to return to a frozen recovery target region.

Do not collapse these into one score in the primary analysis.

---

## 12. Primary prediction

The RVT candidate mechanism predicts that histories with matched reduced constituent state can yield different future viability because exchange history changed relational state:

\[
\boxed{
\mathcal R_V(z_T^A;T_V)
\neq
\mathcal R_V(z_T^B;T_V).
}
\]

No direction is hard-coded into the theory.

The experiment should not assume in advance that History A is “regenerative” and History B is “extractive.” Those labels may be assigned only after observing the future viability footprint relative to the declared counterfactual.

---

## 13. Killer ablation

The primary ablation removes history-to-relation feedback while preserving the constituent dynamics and current exchange law as much as possible.

For example, freeze relational parameters after the matching point:

\[
\rho_{t+1}=\rho^*,
\qquad
\Pi_{t+1}=\Pi^*,
\]

or replace the endogenous relation update by a history-independent rule.

The ablation target is:

\[
\boxed{
h_t\nrightarrow R_{t+1}.
}
\]

If the between-history difference in future viability largely disappears under this ablation, that supports the candidate relation-history-transition mechanism.

If the difference remains unchanged, the proposed mechanism has not been isolated.

---

## 14. Stronger baseline

A stronger benchmark must compare the RVT decomposition against an augmented baseline model supplied with the same measurable state information but without an explicit relational decomposition.

The question is not whether the RVT model can fit the generated data — it obviously can if it generated them.

The stronger question is whether explicit relational variables provide:

- more interpretable intervention targets;
- better out-of-sample prediction under relation changes;
- better counterfactual prediction under coupling/boundary interventions;
- better control design for recovery or viable reachability.

If not, RVT may be conceptually decorative.

---

## 15. Failure criteria

RVT-MIN-001 is not supportive evidence if:

- the matched reduced states are not actually matched within the frozen tolerance;
- the reachable-set difference is created directly by different future controls rather than inherited relational state;
- the effect survives unchanged after history-to-relation feedback is removed;
- the “viability” metric is defined after seeing the result;
- the experiment labels one history regenerative/extractive in advance and tunes parameters to force the label;
- a simpler state variable fully explains the effect and the relational decomposition adds no predictive/control value;
- numerical grid artifacts create the apparent reachable-set difference.

---

## 16. Interpretation boundary

A positive result would support only the narrow proposition:

> In a deliberately constructed dynamical system, relationally mediated exchange history can alter retained relational state and thereby alter finite-horizon future viable reachability even when selected present constituent observables are approximately matched.

That result would justify moving to independently motivated domain models.

It would not establish RVT as a universal theory.

---

## 17. Next step

Before simulation:

1. freeze parameter values;
2. freeze matching tolerance \(\varepsilon_x\);
3. freeze viability thresholds and future horizon \(T_V\);
4. freeze the shock size;
5. freeze the common control grid;
6. implement reachable-set estimation;
7. implement the history-feedback ablation;
8. verify numerical convergence under at least one finer grid.

Only then run the primary comparison.
