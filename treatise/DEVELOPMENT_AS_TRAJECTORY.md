# Development as Trajectory: Propagating Viability in a Moving Capability Landscape

**Status:** exploratory architecture / proposed mechanism

This note records a rotation in the development-economics object. It does **not** claim that the full model is established, that reaction-diffusion dynamics are literally the economy, or that the proposed bridges among Papers F and E are already theorems.

The central shift is:

> **Development is not primarily a state an economy reaches. It is an ongoing trajectory through a changing productive capability landscape.**

Equivalently, the question is not only:

> What does a developed economy have?

but:

> **What is a developing economy able to keep doing?**

This rotation makes several previously separate pieces line up: the playing field, capability formation, graduation, dynamic unsupported viability, propagation/healing fronts, supersession, and reproductive closure.

---

## 1. From development level to developmental dynamics

A conventional snapshot can describe output, income, productivity, industrial composition, or accumulated capability at time `t`.

But if the productive possibility set itself changes through time, then no current snapshot can by itself establish that development is complete.

Let `X_t` denote the productive capability landscape relevant at time `t`.

In general,

`X_t != X_(t+1)`.

New technologies appear, old technologies become obsolete, standards change, supply networks move, relative prices change, and new constraints emerge.

Therefore even if an economy were fully viable over the currently relevant landscape at `t`, that would not imply full viability over the landscape at `t+1`.

This motivates a distinction:

- **development level:** current position or extent of productive viability;
- **developmental dynamics:** whether the system is propagating, regenerating, recombining, and preserving productive viability through change.

Candidate principle:

> **“Developed” is at most a description of the current position of a system that must continue developing.**

---

## 2. A moving viable region

Let

`u(x,t) in [0,1]`

measure the degree to which productive capability position `x` is embedded in a self-maintaining productive configuration at time `t`.

Define a provisional domestically viable region

`H_t = {x in X_t : u(x,t) >= theta and the configuration is dynamically self-maintaining}`.

The self-maintenance clause is essential.

Being active is not enough.

Being profitable today is not enough.

Crossing a graduation threshold once is not enough.

The productive relation must continue to reproduce the conditions of its unsupported viability.

A schematic dynamic-viability requirement is

`F_0(H_t) subseteq H_(t+1)`.

The object of development is therefore not merely the existence of `H_t`, but the trajectory

`H_t -> H_(t+1) -> H_(t+2) -> ...`.

Relevant questions become:

- Does the viable region expand?
- Does it retreat?
- Does it regenerate after shocks?
- Does obsolete capability de-accrete while successor capability forms?
- Does capability recombine into new productive configurations?
- Does the system preserve the capacity to produce further viable relations?

---

## 3. The playing field supplies a local directional bias

Paper F's emerging playing-field layer distinguishes two institutional credibilities:

- `sigma`: credibility that the promised learning/support window will be honored while the public rule says it should be;
- `chi`: credibility that scheduled graduation/withdrawal cannot be overturned by incumbent-specific political capture.

Let

`G(sigma)`

be the optimized value of the graduation route, and

`D(chi)`

be the optimized value of the political-dependence route.

Define the local developmental advantage

`Delta = G(sigma) - D(chi)`.

Then:

- `Delta > 0`: graduation is locally favored;
- `Delta = 0`: the two routes are locally balanced;
- `Delta < 0`: political dependence remains locally more attractive.

The playing field therefore does not by itself cause development. It **tilts the local transition landscape**.

This preserves the distinction:

> **Time under protection is not learning. Credible withdrawal does not force learning; it removes political dependence as a substitute for learning.**

And:

> **Stable rules, contestable positions.**

---

## 4. Healing-front mathematics as a candidate propagation model

### Epistemic status

The bistable reaction-diffusion equation below is **inherited mathematics**. Its use as a development model is a **proposed mechanism / cross-domain structural mapping**, not an established economic theorem.

Consider the Nagumo-type equation

`du/dt = D_theta nabla^2 u + r u(1-u)(u-a)`.

Here:

- `u = 0` and `u = 1` are alternative locally stable states;
- `a in (0,1)` is the unstable threshold separating their basins;
- `D_theta` is an effective propagation/coupling parameter;
- `r` controls local transition speed.

A candidate mapping from the playing-field advantage into the local basin threshold is

`a(Delta) = 1 / (1 + exp(kappa Delta))`,

so that

`a'(Delta) < 0`,

and

`a(0) = 1/2`.

Thus:

- `Delta > 0 -> a < 1/2`;
- `Delta = 0 -> a = 1/2`;
- `Delta < 0 -> a > 1/2`.

For the standard homogeneous bistable front, inherited mathematics gives front speed

`v_D = sqrt(D_theta r / 2) (1 - 2a)`.

Under the illustrative logistic mapping above,

`1 - 2a = tanh(kappa Delta / 2)`,

so

`v_D = sqrt(D_theta r / 2) tanh[(kappa/2)(G(sigma)-D(chi))]`.

This candidate bridge says that developmental propagation depends jointly on:

1. the **local incentive landscape**, through `G(sigma)-D(chi)`; and
2. the **ability of productive capability to propagate**, through `D_theta`.

The interpretation is deliberately broad. `D_theta` could summarize effective transmission through supplier relations, labor mobility, knowledge diffusion, infrastructure, finance, standards, logistics, or other productive couplings. A literal spatial interpretation is not required.

Candidate implication:

> **Successful firms are not the same thing as developmental propagation.**

A graduated firm can remain an island if its success does not improve the conditions under which neighboring productive relations can form, graduate, or remain viable.

---

## 5. Front pinning and incomplete development

If productive conditions are heterogeneous, the developmental front need not move smoothly.

A region may have `Delta_i > 0` while an adjacent capability position has weak infrastructure, missing suppliers, insufficient financing, poor market access, low institutional credibility, or other conditions that make `Delta_j < 0` or sharply reduce effective coupling.

Then the front may stall.

This motivates **front pinning** as a candidate representation of incomplete propagation:

> Development can succeed locally without becoming systemically reproductive.

This is a possible formal route into questions often associated with productive islands, incomplete structural transformation, and middle-income traps.

It remains an empirical and theoretical hypothesis to test, not an established identification of those phenomena.

---

## 6. Development versus convergence

Let `X_D(t)` denote a scalarized domestic developmental front and let

`v_D = dX_D/dt`.

Let `X_F(t)` denote the relevant external/world productive frontier and let

`v_F = dX_F/dt`.

Define the frontier gap

`g(t) = X_F(t) - X_D(t)`.

Then

`dg/dt = v_F - v_D`.

This produces a clean distinction:

- `v_D < 0`: developmental retreat;
- `0 < v_D < v_F`: **development with divergence**;
- `v_D = v_F`: development sufficient to maintain relative position;
- `v_D > v_F`: convergence.

Therefore:

> **Development != convergence.**

An economy can genuinely improve and still fall further behind a faster-moving frontier.

Likewise, a high-income or frontier-adjacent economy is not finished developing. If its regenerative and propagation dynamics slow below the external frontier, relative erosion can begin while current living standards remain high.

---

## 7. Supersession is part of development, not its negation

If an old productive activity exits the viable set, that is not by itself developmental failure.

Suppose

`x_old notin H_(t+1)`.

If capability accumulated around `x_old` is retained, recombined, or redeployed into successor relations `x_new`, while the viable region continues to advance, then the disappearance of `x_old` can be a case of **successful supersession**.

The dangerous case is destructive de-accretion:

`old configuration disappears -> no viable successor configuration forms`.

Development therefore cannot mean preserving every accumulated productive form.

Candidate principle:

> **Preserve and regenerate the capacity to produce what comes next.**

This is the economy-wide version of the playing-field intuition:

> **The field remains; the players change.**

---

## 8. Propagation is not enough: viability behind the front

A moving front can create a false appearance of durable development if the newly transformed region later collapses.

Therefore front advance must be paired with a post-transition self-maintenance condition.

Schematic requirement:

`front advance + F_0(V) subseteq V -> durable propagation`.

Without self-maintenance, the sequence may instead be

`boom -> apparent spread -> retreat`.

This links the propagation picture directly to Paper F's emerging distinction between instantaneous withdrawal survival and dynamic unsupported viability.

---

## 9. Candidate Paper F -> Paper E bridge

The current candidate architecture is:

`credible playing field`

`-> local graduation advantage`

`-> capability formation`

`-> threshold crossing`

`-> propagation`

`-> self-maintenance behind the front`

`-> reciprocal productive coupling`

`-> reproductive closure`

`-> robustness / adaptive embeddedness`.

Paper F studies the formation/graduation side of this process.

Healing-front mathematics may provide a candidate representation of propagation between local graduation and network closure.

Paper E studies when resulting productive relations become reproductively accreted and robust. Its threshold architecture therefore belongs downstream of mere local success.

A possible schematic handoff is

`(sigma, chi) -> Delta -> a(Delta) -> v_D -> productive coupling -> reproductive closure`.

This is **not yet a theorem linking Papers F and E**. The substantive mapping from capability states and propagation into Paper E's edge weights remains open.

---

## 10. Development as a trajectory property

The rotation above yields a strong candidate proposition:

> **Development cannot in general be identified from a snapshot alone.**

Two economies can have the same current income, capability stock, or industrial composition and yet be in opposite developmental conditions if their trajectories differ.

For example, at time `t` they may satisfy

`Y_A(t) = Y_B(t)`

and perhaps even

`q_A(t) = q_B(t)`,

while

`v_D,A > v_F`

and

`v_D,B < 0`.

The present level is identical; the developmental trajectories are not.

Candidate central statement:

> **Development is a trajectory property: the ongoing propagation, regeneration, and adaptive recombination of self-maintaining productive relations through a changing capability landscape.**

Relative development adds:

> **Convergence occurs when that propagation advances faster than the relevant external frontier.**

The deeper object is therefore not merely GDP, industrial composition, or capability as a stock. It is the economy's capacity to keep generating viable successor configurations.

---

## 11. Methodological note: rotation reveals; it does not certify

This architecture emerged by rotating the object from a state representation to a process representation.

That rotation exposed structural correspondences among the playing field, graduation, healing fronts, dynamic viability, supersession, and reproductive closure.

But:

> **Rotation reveals; it does not certify.**

Each proposed bridge must still survive formal derivation, counterexamples, economic interpretation, and empirical confrontation.

The relevant workflow is:

`intuition -> structural match -> formalization -> hostile test -> repair or rejection`.

---

## 12. Immediate research questions

1. What is the smallest economically defensible state variable for `u(x,t)`?
2. Is a bistable local transition actually justified, or would monostable, excitable, threshold-network, or hybrid dynamics fit better?
3. Can `Delta = G(sigma)-D(chi)` be linked to the reaction term without arbitrary functional choices?
4. What economic objects should determine effective coupling `D_theta`?
5. Under what heterogeneity does front pinning occur?
6. Can a discrete network version reproduce the same advance/stall/retreat logic without relying on a spatial PDE?
7. What self-maintenance condition must hold behind the front?
8. How should moving-frontier speed `v_F` be measured empirically?
9. Can observed development-with-divergence episodes distinguish the model from simpler growth-gap accounts?
10. How exactly do propagated viable relations map into Paper E's reproductive edge weights?
11. Under what conditions does supersession preserve developmental velocity rather than create destructive de-accretion?
12. Which country/sector cases provide genuine adversarial tests rather than illustrative stories?

---

## Compact synthesis

The current candidate architecture is:

`stable transition rules`

`-> graduation is locally worth pursuing`

`-> productive capability crosses viability thresholds`

`-> viable relations propagate`

`-> the new state reproduces itself behind the front`

`-> obsolete configurations can be superseded without destroying developmental capacity`

`-> reproductive networks form and adapt`

while the external productive frontier continues moving.

The shortest formulation is:

> **Development is not something an economy finishes. Development is the continuing ability to generate, propagate, preserve, and recombine viable productive relations as the landscape itself changes.**
