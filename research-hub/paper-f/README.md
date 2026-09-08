# Paper F — Capability Graduation and Productive Supersession

## Working manuscript

**Title:** *From Protection to Productive Supersession: Capability Graduation in a Changing Production Network*  
**Author:** Daniel Varela Arévalo  
**Version:** v0.2  
**Main source:** `main.tex` with modular section files under `sections/`  
**Status:** compilation-verified v0.2 research draft; awaiting hostile review; not submission-ready.

## Core question

When does temporary support convert an initially nonviable productive relation into durable unsupported capability, how does capability propagate through a productive network, and what happens to capability when the original productive configuration later exits?

The paper studies:

`activation -> capability accumulation -> graduation -> generativity -> supersession / de-accretion`

with a partial formal bridge:

`graduation -> capability amplification -> generativity -> reproductive accretion`.

## v0.2 changes

v0.2 integrates the first hostile review of the full manuscript.

1. **Activity-gated network learning.** The neighbor contribution to capability conversion is now
   
   `Lambda_e = lambda_bar_e + sum_f a_ef x_f q_f + z_e(omega)`,
   
   so inactive relations do not continue to generate contemporaneous learning merely because they retain historical capability stocks.

2. **Durability / dependence / provenance distinction.** The draft now separates:
   - `q_e`: durable capability that persists after the generating relation disappears;
   - `Omega_e`, `S_e`, `D_e`, `q_e*`: contemporaneous productive dependence;
   - `Delta q_e^u(T) = q_e^u(T) - q_e^0(T)`: a counterfactual empirical attribution object for how much capability support caused.

   Network graduation is a present support-free viability test, not a requirement that capability have arisen without support.

3. **Coupled capability propagation.** For a fixed active configuration,
   
   `q_(t+1) = M q_t + b`, with `M = I - D + X A X`.
   
   Proposition 3 establishes that if `rho(M) < 1`, then the system converges to the unique finite state
   
   `q^infinity = (I - M)^(-1) b`.
   
   By the standard nonsingular M-matrix criterion this is equivalent to `rho(D^(-1) X A X) < 1`.

4. **Revised F -> E handoff.** The bridge is no longer described as wholly open. Paper F and Paper E already share a positive-systems / spectral architecture, while the substantive map from capability states to reproductive-reinforcement weights remains open.

5. **FATE / Pampa evidence strengthened.** The case now treats the FATE board communiqué and the Pampa company statement as primary statements reproduced contemporaneously by news outlets, while keeping the case explicitly diagnostic rather than a complete causal or welfare estimate.

## Current formal spine

1. Pure-complementarity activation gate.
2. Scalar capability law and unsupported threshold.
3. Graduation feasibility theorem.
4. Closed-form minimum support duration.
5. Network-conditioned comparative statics.
6. Durability / dependence / provenance distinction.
7. Coupled positive affine capability system and spectral stability proposition.
8. Unsupported dependency closure.
9. Direct de-accretion trigger.
10. Graduation-frontier contraction under complement loss.
11. Productive supersession via recombinable capability transfer.

## Contribution boundary

The manuscript does **not** claim a general theory of industrial policy or development. Major neighboring mechanisms belong to established literatures: Big Push / coordination, Hirschman linkages, learning-by-doing and infant-industry theory, East Asian export discipline, evolutionary economics / creative destruction, economic complexity, GVC upgrading, production networks, and positive-systems mathematics.

The intended seam is narrower: connect temporary support to an explicit durable capability state, evaluate graduation against recursively support-free dependencies, expose the implications of endogenous capability propagation, and make the fate of capability after exit part of the same developmental diagnosis.

## Diagnostic cases

- **South Korean footwear:** sectoral decline alone cannot establish either failure or successful supersession; capability-transfer channels must be traced.
- **FATE / Pampa Energía synthetic rubber, Argentina (2026):** candidate observed de-accretion edge in which the exit of a major downstream buyer was followed by loss of viability in an upstream synthetic-rubber line. The case is not presented as proof that FATE should have been protected or as a complete welfare evaluation.

## Deliberately outside Paper F

Reserved for Paper G or later work:

- strategic capability / national-security option value;
- domestic minimum capability versus trusted international embeddedness;
- reconstitution time and recoverability;
- rare-earth and coercive-dependence problems;
- oil/mining-led structural transformation and Vaca Muerta;
- coordination latency and opportunity-conversion capacity;
- Canada / Argentina strategic infrastructure comparison.

## Next hostile-review targets

1. Try to break Proposition 3, especially the equivalence between `rho(M) < 1` and `rho(D^(-1) X A X) < 1`, reducibility, boundary cases, and the interpretation of `rho(M) >= 1`.
2. Stress-test the durability/dependence/provenance distinction with counterexamples in which a complement partly teaches and partly remains indispensable.
3. Stress-test unsupported dependency closure under multiple activation fixed points and withdrawal timing.
4. Test de-accretion under substitution, alternative customers, and rapid regional re-embedding.
5. Audit the literature for the closest antecedents on capability transfer, redeployment, industry exit, supplier-customer collapse, related diversification, and positive production networks.
6. Replace reproduced company statements with archival first-party URLs or filings if obtainable before submission.
7. Do not add Paper G scope to F unless a hostile test reveals a genuine missing assumption.

## Strong working claims

> **Time under protection is not learning.**

> **Industrial death is not capability death.**

> **Industrial survival is not developmental success.**

> **Stable rules, contestable positions.**

> **Development succeeds when productive capability can outlive the productive configurations that created it.**
