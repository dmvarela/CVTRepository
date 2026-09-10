# Hostile Test — Reachable Joint Nucleation in the Generative Graduation Cascade

**Status:** adversarial test record / formal counterexample.  
**Purpose:** test whether the joint-nucleation idea adds a real object or merely hides the desired result in an exogenously chosen seed set.

---

## 1. First failure: arbitrary seed sets trivialize nucleation

The first cascade note defined a minimum catalyst set by

`kappa(T|A_0)=min |S|`

subject to

`T subseteq C_G(A_0 union S)`.

If `S` may contain the target and is simply declared graduated, this can be trivial. For a singleton target `{e}`, choosing `S={e}` already gives `kappa<=1` without explaining how `e` became graduated.

**Verdict:** reject this as a nucleation measure.

The corrected object requires a joint-formation gate `J(C|A)` that asks whether the candidate nucleus `C` can actually be reached through an admissible formation/graduation trajectory.

---

## 2. Static mutual viability is not reachability

A mutually self-supporting final state can exist even when there is no path to it from the initial state.

Consider two productive relations with capability states `q_1,q_2`, common capability threshold `theta>0`, and depreciation `delta in (0,1]`.

After extraordinary support is withdrawn, let

`q_(1,t+1)=(1-delta)q_(1,t)+delta*theta*1{q_(2,t)>=theta}`

`q_(2,t+1)=(1-delta)q_(2,t)+delta*theta*1{q_(1,t)>=theta}`.

Unsupported viability requires

`q_1>=theta` and `q_2>=theta`.

### High-capability region is self-maintaining

If both capabilities equal the threshold,

`q_1=q_2=theta`,

then

`q_(1,t+1)=theta`

and

`q_(2,t+1)=theta`.

More generally, the orthant

`V=[theta,infinity)^2`

is forward invariant: if both relations begin at or above threshold, each receives the reciprocal capability-maintenance term and remains at or above threshold.

Thus the pair is a genuine self-supporting unsupported configuration once it exists.

### But the high state is unreachable from zero without capability creation

Start instead from

`q_(1,0)=q_(2,0)=0`.

Suppose policy merely forces both activities to operate but does not itself create capability and the reciprocal learning term activates only after the partner has reached `theta`.

Then both indicators remain zero, so

`q_(1,t)=q_(2,t)=0`

for every `t`.

The self-supporting high state exists but is unreachable from the low state.

Therefore:

> **self-supporting final configuration != reachable graduation path.**

This is the exact reason the joint-formation gate must be path based.

---

## 3. A genuine coordinated push can make the nucleus reachable

Now let temporary joint support create capability while both activities are active. During the supported formation interval, suppose

`q_(i,t+1)=(1-delta)q_(i,t)+mu`,

for `i=1,2`, with

`mu/delta > theta`.

This is exactly the Paper-F-style condition that the supported capability law has a long-run level above the graduation threshold.

Starting from zero, both capability stocks cross `theta` in finite time. If support is then withdrawn simultaneously, the reciprocal unsupported dynamics above keep the pair inside

`V=[theta,infinity)^2`.

Thus the coordinated nucleus becomes reachable.

The intervention is not useful merely because it keeps firms alive. It is useful because it changes the state that governs post-withdrawal viability.

> **Joint protection is not joint graduation unless the supported interval creates the capability required for the unsupported coalition to reproduce itself.**

---

## 4. Why a single supported member can still fail

Suppose only relation 1 is pushed above `theta` while relation 2 remains below threshold.

After withdrawal, relation 1 receives no reciprocal maintenance because `q_2<theta`; relation 2 also receives no reciprocal maintenance if relation 1 falls before relation 2 crosses. The one-sided intervention can therefore decay back below threshold.

This gives a genuine coordination requirement: under this specification, the durable unsupported state requires both relations to cross the threshold before withdrawal.

The relevant object is therefore not merely a minimum seed count. It is a **minimum reachable co-graduating coalition under a specified intervention technology and timing rule**.

---

## 5. Nucleation still does not imply generativity

If the universe contains only the two mutually sustaining relations, successful coordinated graduation creates a viable nucleus but no further cascade.

Let

`C={1,2}`.

Then it is possible that

`J(C|empty)=1`

while

`N_G(C|empty)=empty`.

So:

`reachable nucleation != generative spillover`.

To obtain a genuinely generative nucleus, add relation 3 whose Paper-F gate becomes feasible only after both 1 and 2 are graduated, and relation 4 whose gate becomes feasible only after 3 graduates. Then

`{1,2} -> {3} -> {4}`

contains two distinct mechanisms:

1. coordinated formation of the nucleus;
2. sequential singleton generativity after the nucleus exists.

This separation is analytically useful.

---

## 6. Higher-order nuclei

Joint dependence need not be pairwise.

If three relations each require both of the others before the unsupported threshold can be maintained, no singleton or pair is sufficient while the triplet can be self-supporting and, with a suitable joint capability-creation path, reachable.

Thus minimal nucleating coalitions can have arbitrary order in a finite model.

A pairwise matrix is not in general sufficient to represent the formation problem if coalition effects are genuinely non-additive. Hypergraph or set-valued formulations may eventually be more natural.

---

## 7. Literature boundary exposed by the test

The pure threshold-cascade skeleton is not novel. Threshold diffusion, complex contagion, bootstrap percolation, contagious sets, and target-set selection already study binary activation processes in which multiple active neighbors can be required before a node activates, and minimum seed-set problems are well established.

The candidate economic seam must therefore lie elsewhere:

1. a node is not merely 'activated'; it must complete Paper-F-style capability accumulation and unsupported graduation;
2. the initial nucleus is not merely declared active; `J(C|A)` asks whether a coordinated economic formation path actually reaches it;
3. the post-nucleation cascade asks what further relations can graduate because the nucleus exists;
4. Paper E then independently asks whether the resulting productive structure is reproductively closed.

No novelty claim should be made until that seam is audited against the economics literature.

---

## 8. Current verdict

The original arbitrary-seed definition **breaks**.

The joint-nucleation idea **survives only after repair**.

The surviving structure is:

`self-supporting endpoint`

`!=`

`reachable joint graduation`

`!=`

`generative propagation`

`!=`

`reproductive closure`.

The strongest exact result from this hostile test is the two-node counterexample above: the unsupported high-capability region can be forward invariant while remaining unreachable from the low-capability state unless the supported formation process itself creates enough capability to cross the joint threshold.

That result ties the cascade bridge directly back to Paper F's core principle:

> **Time under protection is not learning.**