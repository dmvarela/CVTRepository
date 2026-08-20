# Types of Wake and Recoverability

## Structural inheritance, repair capacity, and the futures left behind by action

**Status:** conceptual research note; not an empirical law, model lock, manuscript revision, clinical claim, or validation result.

**Boundary:** this note develops a candidate CVT vocabulary for describing how actions and trajectories alter what later systems inherit. It extends the conceptual direction in [`tau-as-revelation.md`](tau-as-revelation.md) and [`future-possibility-and-receptive-capacity.md`](future-possibility-and-receptive-capacity.md), but does not modify `research-hub/cvt-foundations/main.tex`, reinterpret prior validation results, or establish that the same mechanism operates across different empirical domains. Every proposed wake must be independently operationalized and tested against simpler, domain-native explanations.

---

## 1. Core question

CVT has increasingly asked not only:

> What did an action produce?

but:

> **What did the action leave behind for the next action to inherit?**

The immediate outcome may be only part of the consequence. A trajectory can alter the state, the transition operator, the incentive structure, the reachable set, or the information available for reconstruction.

This note uses **wake** for that residual structure.

A cautious working definition is:

> **A wake is the history-conditioned change left by an action or trajectory in the state, repair operator, strategic environment, reachable future set, or reconstructive information inherited by later action.**

The term is intentionally broader than persistence. A wake need not be harmful, permanent, or visible in the current state. It may be regenerative as well as degenerative.

The central CVT question becomes:

\[
\boxed{
\text{What kind of wake does this trajectory leave?}
}
\]

---

## 2. Minimal inherited state

Let

\[
z_t=(x_t,\theta_t,M_t),
\]

where:

- \(x_t\) is the current condition or valuable state;
- \(\theta_t\) parameterizes regenerative or repair capacity;
- \(M_t\) denotes reconstructively useful retained information.

The minimal dynamic form is:

\[
 x_{t+1}=F_{\theta_t}(x_t,a_t),
\]

with structural inheritance:

\[
 \theta_{t+1}=G(\theta_t,x_t,a_t),
\]

and, where relevant,

\[
 M_{t+1}=H(M_t,x_t,a_t).
\]

The key conceptual shift is:

\[
\boxed{
\text{history can modify the generator of subsequent history.}
}
\]

Current state is therefore not sufficient, in general, to characterize future possibility.

Two systems may satisfy

\[
 x_t^A=x_t^B
\]

while

\[
 \theta_t^A\neq\theta_t^B
\]

or

\[
 M_t^A\neq M_t^B.
\]

They can look identical now while possessing radically different futures.

---

## 3. Wake type I: state wake

A **state wake** changes what remains now without necessarily changing the machinery of return.

Schematically:

\[
 x_{t+1}\neq x_t,
 \qquad
 \theta_{t+1}=\theta_t.
\]

This is ordinary depletion, accumulation, displacement, or loss at the level of state.

A state wake can be severe, but it remains conceptually distinct from structural damage. If the repair operator is intact, the system may be able to reverse the state change using essentially the same machinery that existed before the disturbance.

The distinction is:

> **Less state is not yet the same thing as less capacity to rebuild state.**

---

## 4. Wake type II: structural or regenerative wake

A **structural wake** changes the machinery through which later action operates.

Schematically:

\[
 \theta_{t+1}\neq\theta_t.
\]

If \(\theta\) represents regenerative capacity, structural damage may satisfy

\[
 \theta_{t+1}<\theta_t.
\]

A simple productive form is

\[
 x_{t+1}=\alpha x_t+\theta_t g(k_t),
\]

where \(k_t\) is restorative or cooperative effort.

Then the same action has different effects depending on inherited structure:

\[
 \theta_H>\theta_L
 \quad\Longrightarrow\quad
 \theta_Hg(k)>\theta_Lg(k).
\]

This motivates a core formulation:

> **Structural harm is damage that reduces the productivity of future repair.**

The poisoned-well intuition belongs here. The harm does not merely worsen the current condition; it changes the medium through which later corrective action must travel.

A stronger expression is:

> **Some actions do not merely damage what exists; they damage the machinery by which damage could later be repaired.**

---

## 5. State recovery is not capacity recovery

A central implication is that visible return can conceal a structural wake.

It is possible to have

\[
 x_{t+1}=x_t
\]

while

\[
 \theta_{t+1}<\theta_t.
\]

The system has recovered its visible state but not its regenerative capacity.

Thus:

\[
\boxed{
\text{recovery of state}\neq\text{recovery of capacity}.
}
\]

Two systems can therefore display the same current state while differing sharply in their response to the next perturbation.

This suggests a CVT stress-test principle:

> **Perturbation can reveal damage that equilibrium appearance conceals.**

---

## 6. Wake type III: strategic wake

A structural wake can change not only what repair can accomplish, but whether decentralized actors will choose repair at all.

Suppose expected cooperative/restorative action depends on a critical belief \(p^*\) satisfying

\[
 \Lambda\theta H(p^*)=c,
\]

where:

- \(\Lambda>0\) is the remaining value of productive capacity;
- \(H'(p)>0\) captures strategic complementarity;
- \(c>0\) is the private cost or temptation associated with restorative action.

Implicit differentiation gives

\[
\boxed{
\frac{\partial p^*}{\partial\theta}
=-\frac{H(p^*)}{\theta H'(p^*)}<0.
}
\]

Therefore:

\[
 \theta\downarrow
 \quad\Longrightarrow\quad
 p^*\uparrow.
\]

A damaged medium can make cooperation harder to coordinate even when preferences and agents are unchanged.

This is a **strategic wake**:

> **History changes the incentive or equilibrium geometry through which later repair must be organized.**

The same actors with the same nominal action set can rationally choose differently because the inherited medium has changed the return to action.

---

## 7. Wake type IV: reachability wake

A trajectory can alter not merely the cost of repair but the set of futures that remain reachable.

Let \(\mathcal D\) be a desirable target region. Define the technical recovery set:

\[
\boxed{
\mathcal R_t^{\mathrm{tech}}
=
\left\{
z_t:
\exists\ \text{feasible action path reaching }\mathcal D
\right\}.
}
\]

Define the strategic recovery set:

\[
\boxed{
\mathcal R_t^{\mathrm{strat}}
=
\left\{
z_t:
\exists\ \text{equilibrium path reaching }\mathcal D
\right\}.
}
\]

Under the baseline interpretation,

\[
 \mathcal R_t^{\mathrm{strat}}
 \subseteq
 \mathcal R_t^{\mathrm{tech}}.
\]

This yields the **recoverability gap** or **recovery wedge**:

\[
\boxed{
\mathcal W_t
=
\mathcal R_t^{\mathrm{tech}}
\setminus
\mathcal R_t^{\mathrm{strat}}.
}
\]

States in \(\mathcal W_t\) retain a technically feasible route to recovery, but the decentralized system cannot presently make that route self-enforcing.

A compact formulation is:

> **A reachable future can become strategically inaccessible before it technically disappears.**

This is neither ordinary depletion nor full technical irreversibility. It is loss of self-organized access to a still-existing route.

---

## 8. The rescue window

Suppose degradation first pushes the system out of strategic recoverability at date \(t_S\), while technical recovery remains possible:

\[
 z_{t_S}\notin\mathcal R_{t_S}^{\mathrm{strat}},
 \qquad
 z_{t_S}\in\mathcal R_{t_S}^{\mathrm{tech}}.
\]

Suppose continued degradation later pushes the system out of technical recoverability at \(t_T\):

\[
 z_{t_T}\notin\mathcal R_{t_T}^{\mathrm{tech}}.
\]

Then define the **rescue-window duration**:

\[
\boxed{
W=t_T-t_S.
}
\]

During this interval, ordinary decentralized self-correction has failed, but recovery remains technically possible under coordinated or externally supported action.

The rescue window therefore marks a change in intervention logic:

- before \(t_S\): ordinary self-correction may suffice;
- between \(t_S\) and \(t_T\): coordination, commitment, or incentive bridging may suffice;
- after \(t_T\): restoring the target may require rebuilding regenerative capacity, adding new resources, changing technology, or expanding the feasible action set.

Thus:

> **Structural damage can convert recoverability from a state into an expiring opportunity.**

---

## 9. Repair debt

Structural damage can impose an additional burden on every later corrective action.

Let \(k^R(x,\theta;\bar x)\) denote the restorative effort required to reach target \(\bar x\). For \(\theta_H>\theta_L\), define **repair debt**:

\[
\boxed{
D_R
=
 k^R(x,\theta_L;\bar x)
-
 k^R(x,\theta_H;\bar x).
}
\]

When lower regenerative capacity raises required effort,

\[
 D_R>0.
\]

The original harmful act then generates at least two costs:

1. direct state loss;
2. increased future cost of repair.

This motivates the formulation:

> **History can change the cost of returning from history.**

Repeated structural damage can therefore accumulate repair debt while simultaneously making the coordination of repair more difficult.

---

## 10. Wake type V: reconstructive or memory wake

Some systems require more than physical or strategic capacity to recover. They also require information about what is to be reconstructed, how it functioned, or which path returns toward it.

Let \(M_t\) denote **reconstructively useful retained information**.

This is deliberately narrower than generic memory. Memory can preserve harm, warn against repeated exploitation, distort, mislead, or constrain as well as reconstruct. The relevant CVT object is the information that carries part of the reconstruction burden.

A reconstructive wake can therefore be positive or negative:

\[
 M_{t+1}>M_t
\]

may preserve traces that reduce future reconstruction burden, while

\[
 M_{t+1}<M_t
\]

may erase information required to identify or reproduce a viable return path.

The distinction is:

\[
\boxed{
\text{preserved state}
\neq
\text{preserved regenerative machinery}
\neq
\text{preserved reconstructive information}.
}
\]

The three objects can interact, but should not be collapsed into one scalar.

This connects to AI continuity work in a limited structural sense: memory need not be identical to identity or continuity; it can instead carry part of the work required for constrained reconstruction. The same operator may appear in archives, institutional records, biological or ecological markers, and other domain-specific memory systems, but each case requires independent validation.

---

## 11. Wake type VI: generative or stewardship wake

Wake is not synonymous with damage.

A present constraint or act of stewardship can leave a **generative wake** by preserving or increasing future regenerative capacity, reconstructive information, or reachable option-space.

Schematically:

\[
 \theta_{t+1}\ge\theta_t
\]

or

\[
 \mathcal R_{t+1}^{V}
 \supseteq
 \mathcal R_t^{V}
\]

under an appropriate domain-specific comparison.

This provides a formal counterpart to the intuition that some present restrictions preserve future freedom:

\[
 |\mathcal A_t^{\mathrm{protected}}|
 <
 |\mathcal A_t^{\mathrm{unrestricted}}|
\]

while

\[
 |\mathcal R_{t+1:T}^{\mathrm{protected}}|
 >
 |\mathcal R_{t+1:T}^{\mathrm{unrestricted}}|.
\]

The relevant principle is:

> **Preserve not merely the stock, but the generator that makes future stock possible.**

This is the mirror image of razing. A razing trajectory consumes future generativity for present output; stewardship accepts some present constraint to preserve the machinery of future possibility.

---

## 12. Depletion, poisoning, razing, amnesia, stewardship

The wake vocabulary supports a provisional taxonomy of structural inheritance:

### Depletion

\[
 x\downarrow,
 \qquad
 \theta\ \text{approximately preserved}.
\]

Less valuable state remains.

### Poisoning

\[
 x\downarrow,
 \qquad
 \theta\downarrow.
\]

Future repair becomes less productive.

### Razing

The regenerative state falls far enough that ordinary recovery exits the current feasible set:

\[
 z\notin\mathcal R^{\mathrm{tech}}.
\]

This is not a metaphysical claim of permanent irreversibility. It means the current machinery and action set no longer contain a path back to the declared target.

### Amnesia

\[
 M\downarrow
\]

far enough that reconstructive information needed to identify or reproduce a viable return path is lost or degraded.

### Stewardship

Present action preserves or develops \(\theta\), \(M\), or future viable reachability even when doing so constrains immediate extraction.

These are candidate wake classes, not mutually exclusive empirical categories. A single trajectory may produce several simultaneously.

---

## 13. Repeated pressure and cumulative wake

Repeated disturbance can matter because each event changes the system that receives the next event.

If

\[
 \theta_{t+1}<\theta_t
\]

under damaging pressure, then equal shocks need not have equal consequences over time.

The sequence may be:

\[
\boxed{
\text{stress}
\rightarrow
\text{partial return}
\rightarrow
\text{residual structural wake}
\rightarrow
\text{reduced repair capacity}
\rightarrow
\text{larger response to later stress}
\rightarrow
\text{threshold crossing}.
}
\]

This is the disciplined content behind the intuition that a system can be pushed repeatedly until something breaks.

The claim should not be generalized across persons, environments, institutions, materials, or ecosystems without specifying the actual mechanism in each domain. The shared object is the possibility that past stress changes the response operator faced by future stress.

---

## 14. Relation to hysteresis

A structural wake can make the route back differ from the route into damage.

Suppose a damaging action moves

\[
(x_H,\theta_H)
\rightarrow
(x_L,\theta_L)
\]

with

\[
\theta_L<\theta_H.
\]

The reverse action now operates through a different repair operator. Therefore:

\[
\boxed{
\text{doing the opposite action}
\neq
\text{undoing the consequences of the original action}.
}
\]

This can generate hysteresis-like behavior: collapse and restoration thresholds differ because restoration begins from a structurally altered system.

Any empirical use of the term hysteresis must be justified by domain-specific dynamics rather than metaphor alone.

---

## 15. Relation to \(\tau\)

The wake concept sharpens the revelatory role of \(\tau\).

The note on Tau as Revelation argues that \(\tau\) reveals what a trajectory serves, preserves, consumes, and builds. Wake adds a candidate object for what is revealed:

\[
\boxed{
\tau\text{ reveals not only the outcome of action, but the wake inherited by later action.}
}
\]

A trajectory may appear successful at \(t_0\) while leaving:

- a depleted state wake;
- a poisoned repair operator;
- a narrowed strategic basin;
- a contracted reachable set;
- damaged reconstructive memory;
- or, conversely, a generative wake that enlarges future room.

Thus the question is not only whether the visible outcome persists, but what kind of future-making machinery the trajectory leaves behind.

---

## 16. Relation to future possibility and receptive capacity

The existing Future Possibility note distinguishes formal, reachable, and viably reachable action-space. Wake provides a candidate mechanism for how those sets change through history.

Schematically:

\[
 a_t
 \rightarrow
 (x_{t+1},\theta_{t+1},M_{t+1})
 \rightarrow
 \mathcal R_{t+1}.
\]

The path can change the map because the path can change the state, the operator, the information, and the strategic accessibility of later routes.

This yields a compact bridge:

> **Future possibility is inherited not only through what remains, but through the condition of the machinery and information by which later systems must move, repair, and reconstruct.**

---

## 17. Operator-transfer discipline

The wake vocabulary emerged through cross-domain structural comparison. CVT should preserve a strict boundary between **operator transfer** and analogy.

The method is:

1. identify a structural problem;
2. ask which other discipline has faced a problem of the same logical form;
3. borrow the relevant operator or distinction;
4. discard source-domain ontology that is not required;
5. test whether the operator survives formalization in the target domain;
6. specify where the mapping fails.

For example:

- ecology may supply the distinction between stock and regenerative capacity;
- control or viability theory may supply reachability operators;
- game theory may supply strategic accessibility and equilibrium thresholds;
- information theory or continuity work may supply reconstructive-burden questions;
- dynamical systems may supply hysteresis or basin language.

The domains need not be similar. What must be justified is whether the borrowed operator addresses the same abstract problem.

A compact methodological principle is:

> **Borrow operators, not answers.**

---

## 18. Emerging propositions

The present conversation suggests several propositions for future formal work.

### Proposition A — State/capacity distinction

Current state does not generally determine recoverability when the repair operator is history-dependent.

### Proposition B — Poisoned-well effect

When lower regenerative capacity reduces the marginal productivity of restorative action, structural damage raises the coordination threshold for repair.

### Proposition C — Recoverability gap

There can exist states from which a desirable target remains technically reachable but is not reachable through any baseline decentralized equilibrium path.

### Proposition D — Rescue window

Continued degradation after loss of strategic recoverability can eventually destroy technical recoverability, creating a finite interval in which coordinated intervention can still recover the system using existing machinery.

### Proposition E — Repair debt

Structural damage can increase the amount of future effort required to restore a given target even after direct state loss is held fixed.

### Proposition F — Generative constraint

A present restriction can reduce the current feasible action set while preserving or enlarging the future viable reachable set by protecting regenerative capacity or reconstructive information.

These are research propositions. They require formal assumptions, proofs, counterexamples, and domain-specific validation before being treated as established results.

---

## 19. Research tests

For any proposed wake, ask:

1. What exactly is inherited: state, operator, incentives, reachability, information, or several of these?
2. Can the wake be measured independently of the visible outcome?
3. Does history matter once present state is controlled?
4. Does the same action have different consequences because the inherited operator changed?
5. Is the claimed recovery failure strategic, technical, informational, or merely costly?
6. Is the desirable target genuinely unreachable, or only unreachable within a specified horizon or action set?
7. Can a state return while regenerative capacity remains impaired?
8. What intervention restores the correct missing object: state, coordination, regenerative capacity, or information?
9. Does a proposed protective constraint preserve future option-space, or merely impose present control?
10. What observation would show that the wake vocabulary adds no explanatory value over a simpler state model?

The framework remains correction-survivable only if every proposed wake is allowed to fail these tests.

---

## 20. Compact form

The note can be compressed into six statements:

\[
\boxed{
\text{an action leaves more than an outcome; it can leave a wake}
}
\]

\[
\boxed{
\text{state recovery}\neq\text{capacity recovery}
}
\]

\[
\boxed{
\text{history can change the productivity of future repair}
}
\]

\[
\boxed{
\text{a reachable future can become strategically inaccessible before disappearing technically}
}
\]

\[
\boxed{
\text{memory can carry part of reconstruction effort}
}
\]

and:

\[
\boxed{
\textbf{what a trajectory leaves possible is part of what the trajectory does.}
}
\]

The deepest provisional formulation is:

> **CVT studies not only trajectories through a state-space, but the wakes by which trajectories alter the state-space, repair operator, strategic accessibility, reconstructive burden, and future routes inherited by what comes next.**
