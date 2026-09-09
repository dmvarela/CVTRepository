# Paper F — Capability Graduation and Productive Supersession

## Working manuscript

**Title:** *From Protection to Productive Supersession: Capability Graduation in a Changing Production Network*  
**Author:** Daniel Varela Arévalo  
**Version:** v0.3  
**Main source:** `main.tex` with modular section files under `sections/`  
**Status:** source-integrated v0.3 research draft; hostile review and fresh compilation verification required before submission work.

## Core question

When does temporary support convert an initially nonviable productive relation into durable unsupported capability, when is graduation a credible/private survival route rather than political dependence, can the unsupported configuration reproduce its viability through time, and what happens to capability when the original productive configuration later exits?

The paper studies:

`activation -> capability accumulation -> graduation -> dynamic unsupported viability -> generativity -> supersession / de-accretion`

with an upstream institutional layer:

`credible playing field -> graduation preferred to political dependence`

and a partial downstream formal bridge:

`graduation -> capability amplification -> generativity -> reproductive accretion`.

## v0.3 changes

v0.3 integrates the playing-field work and the hostile-test repair to instantaneous withdrawal closure.

1. **Credible support versus credible withdrawal.** The political-economy section now distinguishes:
   - `sigma`: credibility that the announced learning/support window will be honored while the public rule says it should be;
   - `chi`: credibility that announced graduation/withdrawal cannot be overturned by incumbent-specific political pressure when the rule calls for exit.

   Policy credibility is explicitly distinguished from policy rigidity. A credible rule may be state contingent; what high `chi` excludes is incumbent-specific override, not warranted adaptation.

2. **Graduation versus political dependence.** The paper defines reduced-form optimized route values

   `G(sigma)` = value of a strategy that reaches unsupported viability,

   `D(chi)` = value of attempting to preserve extraordinary support politically.

   The playing-field graduation proposition establishes that, when `G` is increasing in `sigma` and `D` decreasing in `chi`, the region

   `P_G = {(sigma,chi): G(sigma) >= D(chi)}`

   is upward closed. If an interior boundary exists with strict derivatives, its slope is negative:

   `chi_G'(sigma) = G'(sigma) / D'(chi_G) < 0`.

   This separates **technological graduability** from **incentive-compatible graduation**.

3. **The rent-allocation overclaim was removed.** Making capture harder does not necessarily raise capability investment dollar for dollar because resources may flow to payouts, cash, debt reduction, or other uses. The surviving claim is narrower: credible withdrawal makes political dependence a less attractive substitute for graduation.

4. **Dynamic unsupported viability.** Unsupported dependency closure is now explicitly an instantaneous withdrawal test. Let

   `x* = C_0(x0;q_T)`

   be the support-free closure and let post-withdrawal capability obey

   `q_(t+1) = M_0 q_t + b_0`.

   For fixed `x*` and unsupported environment, with threshold vector `vartheta`, the forward-invariance proposition establishes the sufficient condition

   `M_0 vartheta + b_0 >= vartheta`.

   Hence a configuration can survive withdrawal at `T` yet fail dynamic graduation if its unsupported capability path subsequently falls below threshold.

5. **Human transition is kept outside the positive theorem.** The discussion now distinguishes nominal opportunities from a feasible opportunity set

   `A^F(r) = {a_i in A : R(a_i) <= r}`

   so firm/sector exit discipline is not silently equated with abandoning displaced people.

6. **Scope containment strengthened.** Adaptive productive memory, coevolving coupling, healing-front propagation, strategic capability option value, and the larger theory of economic development remain outside Paper F's formal core. F ends at capability formation, credible graduation, unsupported viability, generativity, and capability-preserving or capability-destroying exit.

## Inherited v0.2 foundations retained

1. **Activity-gated network learning:**
   
   `Lambda_e = lambda_bar_e + sum_f a_ef x_f q_f + z_e(omega)`.

2. **Durability / dependence / provenance distinction:**
   - `q_e`: durable capability;
   - `Omega_e`, `S_e`, `D_e`, `q_e*`: contemporaneous dependence;
   - `Delta q_e^u(T) = q_e^u(T) - q_e^0(T)`: counterfactual causal attribution.

3. **Coupled capability propagation:**
   
   `q_(t+1) = M q_t + b`, with `M = I - D + X A X`.
   
   If `rho(M) < 1`, the system converges to
   
   `q^infinity = (I - M)^(-1) b`,
   
   equivalently under the maintained positivity assumptions `rho(D^(-1) X A X) < 1`.

4. **Unsupported dependency closure:** recursively removes support-dependent neighbors before declaring network graduation at withdrawal.

5. **Exit taxonomy:** failed graduation, destructive de-accretion, competitive displacement, and successful supersession.

## Current formal spine

1. Pure-complementarity activation gate.
2. Scalar capability law and unsupported threshold.
3. Graduation feasibility theorem.
4. Closed-form minimum support duration.
5. Network-conditioned comparative statics.
6. Durability / dependence / provenance distinction.
7. Coupled positive affine capability system and spectral stability proposition.
8. Unsupported dependency closure at withdrawal.
9. Forward-invariant unsupported capability region for fixed post-withdrawal configuration.
10. Generativity definition.
11. Direct de-accretion trigger.
12. Graduation-frontier contraction under complement loss.
13. Productive supersession via recombinable capability transfer.
14. Playing-field graduation region: credible support / credible withdrawal versus political dependence.
15. Feasible worker-transition opportunities as a discussion/welfare extension, not part of the positive theorem.

## Contribution boundary

The manuscript does **not** claim a general theory of industrial policy or development. Major neighboring mechanisms belong to established literatures: Big Push / coordination, Hirschman linkages, learning-by-doing and infant-industry theory, East Asian export discipline and reciprocity, evolutionary economics / creative destruction, economic complexity, GVC upgrading, production networks, and positive-systems mathematics.

The intended seam is narrower: connect temporary support to an explicit durable capability state; distinguish technological graduability from the incentive to pursue graduation; evaluate graduation against recursively support-free dependencies and their subsequent capability dynamics; expose endogenous capability propagation; and make the fate of capability after exit part of the same developmental diagnosis.

## Diagnostic cases

- **South Korean footwear:** sectoral decline alone cannot establish either failure or successful supersession; capability-transfer channels must be traced. The Korea literature also motivates, but does not by itself prove, the playing-field distinction between support and performance discipline.
- **FATE / Pampa Energía synthetic rubber, Argentina (2026):** candidate observed de-accretion edge in which the exit of a major downstream buyer was followed by loss of viability in an upstream synthetic-rubber line. The case is not presented as proof that FATE should have been protected or as a complete welfare evaluation.

## Deliberately outside Paper F

Reserved for the treatise, Paper G, or later work:

- adaptive productive memory and coevolution of capability `Q` with coupling `W`;
- healing-front / propagation dynamics and front pinning;
- development as a trajectory rather than a national level;
- strategic capability / national-security option value;
- domestic minimum capability versus trusted international embeddedness;
- reconstitution time and recoverability;
- rare-earth and coercive-dependence problems;
- oil/mining-led structural transformation and Vaca Muerta;
- coordination latency and opportunity-conversion capacity;
- Canada / Argentina strategic infrastructure comparison.

## Next hostile-review targets

1. Attack the new forward-invariance proposition: fixed active set, state-dependent thresholds, changing external environment, and whether the sufficient threshold-reproduction condition is economically meaningful or too strong.
2. Attack the playing-field proposition: nonmonotone support credibility, capture/learning complementarities, endogenous political value `B`, risk aversion, and cases where lobbying is productive coordination rather than pure rent preservation.
3. Re-test the spectral proposition and its `M`-matrix equivalence under reducibility and boundary cases.
4. Stress-test the durability/dependence/provenance distinction with mixed complements that both teach and remain indispensable.
5. Test de-accretion under substitution, alternative customers, and rapid regional re-embedding.
6. Audit the literature for the closest antecedents to the two-credibility playing-field formulation and dynamic graduation distinction.
7. Run a fresh two-pass `pdflatex` build and inspect cross-references before calling v0.3 compilation verified.
8. Do not add the broader adaptive-network development theory unless a hostile test reveals that F genuinely requires it.

## Strong working claims

> **Time under protection is not learning.**

> **The credible removal of protection is part of the protection policy itself.**

> **Policy stability is not policy constancy.**

> **Stable rules, contestable positions.**

> **At the threshold of unsupported viability, the productive configuration must reproduce at least its own capability requirements.**

> **Industrial death is not capability death.**

> **Industrial survival is not developmental success.**

> **Development succeeds when productive capability can outlive the productive configurations that created it.**
