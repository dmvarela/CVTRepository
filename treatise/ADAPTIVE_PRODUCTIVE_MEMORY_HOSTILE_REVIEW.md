# Hostile Review Record — Adaptive Productive Memory

**Status:** adversarial research record / adjudication note

This note preserves the main failures identified in an external hostile review of `ADAPTIVE_PRODUCTIVE_MEMORY.md` and the current adjudication after rechecking the structure. It is not itself a theorem or literature review.

The purpose is methodological: preserve what broke, what survived, and what changed so later drafts do not quietly reintroduce discarded claims.

---

## 1. Main mathematical failures identified

### 1.1 Bistability was not implied by `Q <-> W`

The earlier note left the successful-interaction function insufficiently specified while discussing multiple regimes and hysteresis.

Under a symmetric two-node reduction with linear capability aggregation, a success term of the form

`F = w q`

produces an equilibrium condition no richer than a quadratic in `w`; the hostile review found no admissible hysteresis structure in that benchmark.

A synergistic specification

`F = w q^2`

can instead yield a cubic equilibrium equation and admissible three-root configurations.

### Adjudication

**Accepted, with interpretation repaired.**

The relevant economic mechanism should not be "insert a superlinear term." A full bilateral relation can instead use

`F^+_ij = w_ij q_i q_j`,

so the symmetric reduction naturally becomes `w q^2`. The substantive hypothesis is bilateral complementarity: successful productive interaction may require capability on both sides.

The resulting rule is:

> **Bistability is not generic. It must be derived from an explicitly specified interaction technology.**

---

### 1.2 `H_ij = partial gamma_j / partial x_i` was ill-defined

Paper F uses binary activation variables `x_i in {0,1}`. Ordinary partial derivatives with respect to binary variables are not defined, and a smooth Jacobian is especially suspect near threshold activation.

The proposed objects

`H`, `H^2`, `H^3`, ...

and the later bridge

`K = R H`

therefore did not yet have a defensible mathematical interpretation.

### Adjudication

**Accepted. The construction is withdrawn.**

A safer local object is the finite difference

`Delta_i gamma_j(x) = gamma_j(x^(i->1)) - gamma_j(x^(i->0))`.

More importantly, generativity should be represented directly as a discrete cascade using Paper F's activation / unsupported-closure machinery.

Candidate bridge:

`graduation event -> discrete change in neighboring viability -> activation/viability cascade -> resulting configuration -> Paper E reproductive-closure test`.

No spectral-radius claim for `K` should be made unless a mathematically valid continuous or discrete operator is later derived.

---

## 2. Pathway law repaired

The original law

`dw_ij/dt = eta F_ij(1-w_ij) - rho w_ij`

was already recognized as insufficient because zero-strength paths cannot bootstrap if flow itself requires an existing path.

The three-term exploration/reinforcement/decay law solved that bootstrapping problem, but subsequent discussion exposed another missing mechanism: failed traversal can actively damage a relationship rather than merely fail to reinforce it.

The current candidate is therefore

`dw_ij/dt = a_ij(1-w_ij) + eta^+_ij F^+_ij(1-w_ij) - eta^-_ij F^-_ij w_ij - rho_ij w_ij`.

Interpretation:

- exploration creates or seeds pathways;
- successful use strengthens them;
- failed use damages them;
- non-use allows decay.

Exploration must also be scarce. A latent feasible-opportunity graph and/or a search budget such as

`sum_j a_ij <= B_i`

prevents every conceivable edge from being continuously seeded.

---

## 3. Productive memory versus development

The hostile review correctly emphasized that a dense, highly reinforced network can still be stagnant.

### Adjudication

**Accepted, but this was already an internal correction before the review.**

A fixed finite `(Q,W)` system can settle. Therefore adaptive productive memory is not the full development theory.

The broader architecture requires at least:

`memory + exploration + novelty + supersession + adaptation to a changing frontier`.

This distinction should remain explicit in every future formulation.

---

## 4. Falsification claim refined

The hostile review proposed that if pathways with different histories behave identically after controlling for current `w`, pathway memory would be falsified.

### Adjudication

**Rejected as stated.**

The present concept of memory is state-based. The claim is

`past trajectory -> current state (Q_t,W_t) -> future dynamics`.

It does not require hidden historical dependence after the current state is fully controlled.

A sharper falsification target is whether exogenous successful traversal changes the future pathway state at all. If credible exogenous variation in successful use leaves future relationship persistence, terms, reliability, cost, or accessibility unchanged, the reinforcement mechanism is unsupported.

Likewise, the proposed failure-damage mechanism should be rejected if failed traversal does not worsen future interaction conditions in settings where such an effect should be observable.

Selection remains a central identification problem: capable firms may self-select into stronger relationships.

---

## 5. Economic and literature boundaries

The review emphasized that the broad ingredients have close antecedents in established areas including:

- adaptive/co-evolutionary networks;
- relationship-specific capital and relational contracting;
- reputation and trade-credit mechanisms;
- evolutionary economic geography and relatedness dynamics;
- endogenous production-network formation;
- path dependence and learning-by-doing.

### Adjudication

**Accepted as a warning, not yet as a completed literature finding.**

No novelty claim should be made until those literatures are systematically audited.

The likely research seam is narrower:

> **How does a successful graduation event change the viability of other productive relations, and when does that discrete generative cascade produce a configuration that becomes reproductively closed?**

That seam potentially connects Paper F's graduation/closure machinery to Paper E's reproductive-accretion machinery.

---

## 6. Current smallest model worth retaining

The smallest retained adaptive-memory module is:

`dq_i/dt = -delta_i q_i + x_i[lambda_i^0 + beta_i sum_j w_ji phi(q_j)]`

with a bilateral successful-interaction function such as

`F^+_ij = w_ij q_i q_j`

(or a bounded/saturating analogue), and pathway dynamics

`dw_ij/dt = a_ij(1-w_ij) + eta^+_ij F^+_ij(1-w_ij) - eta^-_ij F^-_ij w_ij - rho_ij w_ij`.

Required restrictions:

- exploration constrained to feasible/adjacent opportunities;
- finite search/coordination budget where appropriate;
- no claim that more `W` is automatically better;
- no generic bistability claim;
- no `K=RH` or `H^k` spectral claim.

---

## 7. Three immediate adversarial tests

1. **Dense but stagnant network:** can the framework correctly classify a highly connected, high-capability, low-novelty economy as mature/stagnant rather than automatically developmental?
2. **Exogenous link-formation shock:** after an externally created linkage opportunity, do successfully traversed new paths become measurably easier/more persistent than comparable untraversed possibilities after selection is addressed?
3. **Sparse generativity:** can a sparse network produce deep generative cascades, demonstrating that density is neither necessary nor sufficient for development?

---

## 8. Current bridge candidate

The prior smooth-matrix bridge is withdrawn.

The replacement candidate is discrete:

`Paper F graduation`

`-> finite change in neighboring graduation/viability conditions`

`-> iterative activation / support-free viability cascade`

`-> newly viable productive configuration`

`-> Paper E reproductive-closure / robustness test`.

This bridge is currently an **open formal program**.

---

## 9. What the hostile review improved

The review forced the architecture to distinguish:

`productive memory != development`

`reinforcement != exploration`

`successful traversal != absence of failure`

`bilateral complementarity != generic feedback`

`generativity != powers of an ill-defined derivative matrix`.

The result is smaller but more defensible.

Methodological rule to preserve:

> **If adversarial review removes a claim, record the removal. Do not let later synthesis quietly resurrect it.**
