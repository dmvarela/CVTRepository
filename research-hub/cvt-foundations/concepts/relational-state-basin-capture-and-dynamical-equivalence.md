# Relational State, Basin Capture, and Dynamical Equivalence

**Status:** Exploratory working note for Paper E  
**Date:** 2026-08-25  
**Context:** Builds from Paper D (*Maintenance Is Not Recovery*), the fusion-control work on ignition versus sustained-burn basin capture, and the emerging Paper E question: **is the represented present state a sufficient statistic for history?**

## 1. Core distinction: inherited stock versus inherited relation

Let

\[
s_t=(x_t,\theta_t),
\]

where:

- \(x_t\) is an observable or summary stock/capacity;
- \(\theta_t\) is an inherited relational configuration that conditions how present actions become effective.

Conceptually,

\[
\boxed{\text{system state}=(\text{elements},\text{relations})}.
\]

A richer network version would replace scalar \(\theta\) with a relational matrix \(\Theta=[\theta_{ij}]\), but the scalar case is useful for identifying the minimal mechanism.

The point is not that \(\theta\) is merely “whatever \(x\) forgot.” A stronger interpretation is:

> **\(\theta_t\) represents the historically produced relational configuration through which future action becomes productive, feasible, or self-maintaining.**

History may therefore matter not only because it changes what survives, but because it changes **how what survives is related**.

---

## 2. First negative result: relational inheritance can cancel too

A naive relational term is not automatically behaviorally relevant.

Suppose both candidate paths \(a\in\{P,E\}\) evolve according to

\[
z^a_{t+1}=\alpha z^a_t+b_a+q\theta_n.
\]

If the same inherited relational contribution \(q\theta_n\) enters both paths symmetrically, it cancels from the comparison \(J^P-J^E\), just as common inherited stock can cancel in Paper D.

Thus:

\[
\boxed{\text{relational inheritance alone is not enough}.}
\]

For relation to alter the choice margin, it must differentially affect what alternative actions can produce.

A minimal non-cancelling specification is

\[
d(x_n,\theta_n)=\bar d+D x_n+H\theta_n,
\qquad H>0.
\]

Then the finite-task preference gap takes the form

\[
J_T^P-J_T^E
=S_T(\delta)
\left[
\beta_T(\delta)(\bar d+D x_n+H\theta_n)-\Delta\pi
\right].
\]

Define

\[
c(\delta)=\frac{\Delta\pi}{\beta_T(\delta)}-\bar d.
\]

Then \(P\) is preferred iff

\[
D x+H\theta>c(\delta).
\]

The decision boundary is therefore

\[
\boxed{D x+H\theta=c(\delta)}.
\]

Paper D has a scalar boundary \(x_c\). Paper E naturally opens a two-dimensional \((x,\theta)\) geometry.

---

## 3. Same stock, different future

Solve the boundary for relational state:

\[
\theta_c(x)=\frac{c-Dx}{H}.
\]

At a fixed observed stock \(x=\bar x\), two systems can satisfy

\[
\theta_L\le \theta_c(\bar x),
\qquad
\theta_H>\theta_c(\bar x).
\]

Then

\[
(\bar x,\theta_L)
\]

and

\[
(\bar x,\theta_H)
\]

have identical measured stock but lie on opposite sides of the decision boundary.

Hence:

\[
\boxed{x_A=x_B\not\Rightarrow\text{dynamic equivalence}.}
\]

This is the first formal sense in which an observed present state can fail to summarize what history has left behind.

---

## 4. Minimal basin model

Let

\[
s=\begin{pmatrix}x\\\theta\end{pmatrix},
\]

and suppose repeated path \(a\in\{P,E\}\) induces the stable affine map

\[
F_a(s)=\mu s+(1-\mu)s_a^*,
\qquad 0\le\mu<1.
\]

Let

\[
L(s)=Dx+H\theta-c.
\]

Choose \(P\) when \(L(s)>0\), and \(E\) otherwise. Assume

\[
L(s_E^*)<0<L(s_P^*).
\]

Because \(L\) is affine,

\[
L(F_a(s))=\mu L(s)+(1-\mu)L(s_a^*).
\]

Therefore each side of the boundary is forward invariant under its associated path. The two basins are

\[
\mathcal B_E=\{(x,\theta):Dx+H\theta\le c\},
\]

\[
\mathcal B_P=\{(x,\theta):Dx+H\theta>c\}.
\]

The separatrix is

\[
\Sigma:\quad Dx+H\theta=c.
\]

This produces the key Paper E picture: **same observed \(x\), different inherited \(\theta\), different basin membership, different long-run future.**

---

## 5. Fusion correction: threshold crossing is not basin capture

The fusion-control work already established a structural warning:

\[
\boxed{\text{threshold crossing}\neq\text{basin capture}.}
\]

In fusion, transient ignition does not imply a self-maintaining burn. The trajectory must enter and remain inside a viable burn basin, with sufficient restoring dynamics and robustness to perturbation.

The relational-development analogue is not merely “can the system reach the high state?” but:

\[
\boxed{
\text{reach}
\rightarrow
\text{cross}
\rightarrow
\text{capture}
\rightarrow
\text{reside}
\rightarrow
\text{recover from perturbation}
}.
\]

Reachability alone is therefore too weak.

Two systems may visit the same observable state yet differ in whether that state is self-maintaining under their inherited relational configuration.

---

## 6. Stock restoration is not basin restoration

Suppose a high-capacity system begins at

\[
s_P^*=(x_P^*,\theta_P^*).
\]

A shock damages both stock and relation, producing

\[
(x_L,\theta_L).
\]

A reconstruction policy then restores only the measured stock:

\[
x_L\rightarrow x_P^*,
\qquad
\theta_L\rightarrow\theta_L.
\]

The reconstructed state is

\[
s_R=(x_P^*,\theta_L).
\]

Measured restoration gives

\[
x_R=x_P^*.
\]

But if

\[
\theta_L\le\theta_c(x_P^*)
=\frac{c-Dx_P^*}{H},
\]

then

\[
s_R\in\mathcal B_E.
\]

Thus:

\[
\boxed{\text{stock restoration}\not\Rightarrow\text{basin restoration}.}
\]

A compact formulation is:

> **The water level is back. The well is not.**

In industrial language:

> **You can rebuild the plant and still fail to rebuild the industry.**

The missing object may be the supplier, customer, financing, standards, logistics, credibility, or coordination structure carried by \(\theta\).

---

## 7. \(\tau\) as relational construction time

Suppose physical capacity can be restored quickly, but relational state rebuilds only through repeated successful interaction:

\[
\theta_{n+1}
=\mu\theta_n+(1-\mu)\theta_P^*.
\]

Then

\[
\theta_n
=\theta_P^*-
\mu^n(\theta_P^*-\theta_0).
\]

If stock is held at \(\bar x\), basin entry requires

\[
\theta_n>\theta_c(\bar x).
\]

Hence a minimum relational recovery duration exists:

\[
\tau_{\min}
=
\min\left\{
n:
\mu^n<
\frac{\theta_P^*-\theta_c(\bar x)}
{\theta_P^*-\theta_0}
\right\}.
\]

This gives mathematical content to the claim:

\[
\boxed{\text{some states cannot be jumped to; they must be traversed}.}
\]

The path is partly constitutive of the destination because the path constructs one of the state variables.

---

## 8. Temporary activation versus genuine capture

Define the current cooperation margin

\[
q(s)=\beta(\bar d+D x+H\theta)-\Delta\pi.
\]

If the dynamics compress to a scalar law, repeated \(P\) may satisfy

\[
q_{t+1}=\mu_P q_t+(1-\mu_P)q_P^*,
\]

with \(q_P^*>0\).

Starting from \(q_0<0\), external support may temporarily force the system to follow \(P\). During support,

\[
q_n=q_P^*+\mu_P^n(q_0-q_P^*).
\]

Capture occurs only when

\[
q_n>0,
\]

so that support can be withdrawn without immediate reversion to \(E\).

Thus:

\[
\boxed{\text{temporary activation}\neq\text{endogenous capture}.}
\]

The minimum capture duration is

\[
n_{\rm cap}
=
\min\left\{
n:
\mu_P^n<
\frac{q_P^*}{q_P^*-q_0}
\right\}.
\]

If instead

\[
q_P^*\le0,
\]

then no duration of forcing alone can create a self-maintaining high basin. This distinguishes:

1. **premature withdrawal:** a viable high basin exists, but support ends before capture;
2. **host non-viability:** no amount of duration alone can generate endogenous persistence.

This is the relational analogue of the fusion project’s **Minimum Viable Host** distinction.

---

## 9. Decision sufficiency is not dynamic sufficiency

The scalar margin \(q\) may be sufficient to determine today’s action while still failing to predict tomorrow’s response.

Let

\[
s_{t+1}=M_a s_t+b_a,
\]

and write

\[
q(s)=\ell^\top s-c.
\]

A closed scalar law

\[
q_{t+1}=f_a(q_t)
\]

exists for all states only under a restrictive condition such as

\[
\ell^\top M_a=\mu_a\ell^\top.
\]

If this condition fails, there may exist \(s,s'\) such that

\[
q(s)=q(s')
\]

but

\[
q(F_a(s))\neq q(F_a(s')).
\]

Therefore:

\[
\boxed{\text{decision sufficiency}\neq\text{dynamic sufficiency}.}
\]

Two systems can make the same decision today and still belong to different predictive classes because their hidden relational composition produces different responses tomorrow.

This connects directly to the broader Paper E question:

> **Is the represented present state a sufficient statistic for history?**

---

## 10. Predictive equivalence and the deeper state object

The decomposition \((x,\theta)\) is useful but representation-dependent. A sufficiently rich state variable could absorb \(\theta\). The more invariant object is therefore predictive equivalence of histories.

Let \(h\sim h'\) iff every admissible common continuation produces the same payoff- or outcome-relevant future response.

Then the minimal dynamically sufficient state can be thought of abstractly as

\[
\boxed{s=[h]}. 
\]

A useful interpretation is:

> **Two histories are dynamically equivalent only when the future can no longer tell them apart.**

The proposed \(\theta\) can be understood as the refinement index that distinguishes predictive classes within an observed \(x\)-fiber.

Thus \(\theta\) is not necessarily a unique physical quantity. It is whatever additional inherited relational information is required so that equal current states imply equal future response under equal continuations.

---

## 11. Relational topology and possibility geometry

A scalar \(\theta\) may be only a first approximation. In a network formulation,

\[
\Theta=[\theta_{ij}],
\]

history can alter:

- **transition inheritance:** how existing states propagate;
- **action-productivity inheritance:** what an intervention produces;
- **feasibility inheritance:** which actions are credible or available at all.

For example,

\[
x_{t+1}=A(\Theta_t)x_t+B(\Theta_t)a_t,
\]

or the feasible action set may itself depend on relation:

\[
\mathcal A=\mathcal A(\Theta_t).
\]

Then relational damage can change not only productivity but the attainable future set

\[
\mathcal R_H(x,\Theta).
\]

However, equal reachable sets do not imply dynamical equivalence. Two systems may reach the same target with radically different cost, time, robustness, redundancy, or probability of successful capture.

Hence the relevant object may be a **reachability geometry**, not merely a reachable set.

---

## 12. Fusion and relational dynamics: what kind of equivalence?

The current fusion–development correspondence should **not** yet be called a diffeomorphism.

A diffeomorphism is a smooth invertible map between state spaces. To claim that two dynamical systems are actually the same dynamics under a change of coordinates requires a conjugacy.

For discrete systems

\[
x_{t+1}=F(x_t),
\qquad
y_{t+1}=G(y_t),
\]

we would seek a map \(h\) satisfying

\[
\boxed{h\circ F=G\circ h}.
\]

If \(h\) is a diffeomorphism, the systems are smoothly conjugate.

At present, the fusion and relational models exhibit candidate preserved structure:

- threshold crossing is not basin capture;
- external forcing is not endogenous persistence;
- distance from the separatrix relates to robustness;
- host viability determines whether capture is possible;
- premature withdrawal differs from structural impossibility;
- trajectories may share geometry even when their physical clocks differ.

The appropriate hierarchy to test is:

1. analogy;
2. structure-preserving morphism;
3. homeomorphism of relevant state spaces;
4. topological conjugacy;
5. orbit equivalence under time reparameterization;
6. smooth conjugacy under a diffeomorphism.

Because the relational model is switched/piecewise smooth, a global smooth conjugacy may be too strong. Piecewise smooth conjugacy, topological conjugacy, orbit equivalence, or a shared local normal form may be the correct object.

A defensible research question is therefore:

> **Do fusion burn capture and relational basin capture instantiate the same local dynamical normal form, even though their physical substrates are unrelated?**

This is stronger than metaphor but weaker than an unearned claim of physical equivalence.

---

## 13. Immediate mathematical work for Paper E

The next pressure tests are:

1. **Remove the hand-built basin assumption.** Derive whether multiple attractors and a separatrix emerge from coupled \((x,\theta)\) dynamics rather than assigning path-specific attractors by construction.
2. **Test cancellation rigorously.** Characterize exactly when relational inheritance alters welfare but not the action margin.
3. **Characterize dynamic sufficiency.** Determine conditions under which the scalar margin \(q\) is a sufficient Markov state and conditions under which the full \((x,\theta)\) state is required.
4. **Curved separatrix case.** Drop the eigenvector reduction and study the basin boundary in full state space.
5. **Capture theorem.** Distinguish transient threshold crossing, basin entry, basin capture, robust residence, and recovery after perturbation.
6. **Minimum relational recovery time.** Establish conditions under which relational rebuilding has a strictly positive lower-bound duration.
7. **Network extension.** Replace scalar \(\theta\) by \(\Theta\) and distinguish relational quantity from relational topology.
8. **Predictive-state formulation.** Define controlled predictive equivalence of histories and relate \((x,\theta)\) to the minimal sufficient state partition.
9. **Fusion comparison.** Retrieve the actual fusion equations and identify which invariants are shared: fixed points, stability type, separatrix, direction of flow, capture condition, robustness margin, and host-viability condition.
10. **Literature positioning before novelty claims.** Compare with causal states, predictive-state representations, bisimulation, hysteresis, viability theory, switched systems, path dependence, network capital, and dynamical sufficient statistics.

---

## 14. Working claims worth preserving

These are currently **working formulations**, not yet theorem claims unless supported above:

> **A system inherits not only its components, but the ways its components have learned to be together.**

> **The path is partially constitutive of the destination when the path constructs future-relevant relational state.**

> **Same observable stock does not imply same basin membership.**

> **Restoring a coordinate is not the same as restoring the dynamics that made that coordinate self-maintaining.**

> **Reachability is weaker than capture; capture is weaker than robust residence.**

> **Decision sufficiency is weaker than dynamic sufficiency.**

> **History matters to the extent that it leaves future-relevant distinctions in the present state representation.**

> **Two histories are dynamically equivalent only when the future can no longer tell them apart.**

---

## 15. Paper D / Paper E boundary

To avoid swallowing Paper D:

- **Paper D** studies inherited capacity \(x\), productive complementarity, basin formation, maintenance versus recovery, resilience/recovery margins, and finite-horizon reachability.
- **Paper E** asks whether \(x\) is sufficient, introduces relational/structural inherited state \(\theta\) or \(\Theta\), studies equal observed stock with different future dynamics, basin capture versus coordinate restoration, and the more general predictive-equivalence question.

A concise distinction is:

\[
\boxed{
\text{D: How much/productive capacity did history leave?}
}
\]

\[
\boxed{
\text{E: What did history turn the system into?}
}
\]

The fusion project provides a mathematical warning and possible dynamical morphism: **do not confuse crossing a visible threshold with being captured by a self-maintaining basin.**
