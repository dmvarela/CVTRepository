# CVT Foundations — Variable and Proxy Table, Pass 01

**Date:** 2026-07-29  
**Manuscript:** `research-hub/cvt-foundations/main.tex`  
**Review issue:** #6 — Stress-test CVT Foundations  
**Review branch:** `review/cvt-foundations-operationalization-2026-07-29`  
**Status:** operationalization review; does not modify the canonical manuscript.

## Purpose

This artifact asks whether the principal CVT variables can be observed, estimated, perturbed, and falsified. It separates three layers that the manuscript sometimes blends:

1. **the conceptual condition** — bounded coupling, preserved distinction, receptive basin, or restorative reserve;
2. **the mathematical representation** — a normalized gate, threshold, product, or differential equation;
3. **the observable proxy** — a domain-specific measurement that can be collected independently of the theory.

A gate is not automatically an observable. Every application must state how the gate is measured, how it is normalized, how its threshold is chosen, and how uncertainty is propagated.

## Core four-condition table

| CVT condition | Current symbol | Operational question | Candidate observable proxies | Failure signature | Main identification risk | Falsifying or constraining case |
|---|---|---|---|---|---|---|
| Bounded coupling | `B`, `G_bound`, permeability `Pi`, raw exchange `J_raw` | Is exchange present but limited relative to the receiver’s safe handling range? | boundary flux; input rate divided by rated handling capacity; saturation fraction; control effort required to maintain constraints; time above safe flux limit | isolation at too little coupling; overload, saturation, or constraint escape at too much coupling | “Bounded” is scale- and timescale-dependent; safe capacity may itself change with state | a system repeatedly hosts transformation under effectively unbounded input without adaptive boundary regulation or loss of viability |
| Preserved distinction | `D` in the invariant, `G_distinction` | Do the interacting systems remain functionally and structurally distinguishable during exchange? | membrane/interface integrity; separability of subsystem state variables; persistence of independent constraints or control channels; recoverability of component identity after coupling; role or agency preservation in nonphysical systems | merger, homogenization, role collapse, loss of independent control, inability to attribute states to the original subsystems | distinction can be confused with isolation; there is no universal scalar measure of identity preservation | a hosted transformation in which subsystem distinction collapses completely yet no relevant function, control capacity, or identity condition is lost |
| Receptive basin | `R`, `G_receptivity`, `rho` | Does delivered input enter a state trajectory that productively incorporates it rather than converting it into load or damage? | uptake efficiency `J_eff/J_raw`; fraction of input converted into target state change; probability of capture into an admissible attractor; retention after a defined delay; inverse rejection, spillover, or waste fraction | high delivered exchange with low uptake; rising rejection, spillover, oscillation, or damage; failure to enter or remain in the target basin | receptivity is currently both a gate and a product of other gates, creating possible circularity | increased input produces proportionate productive uptake across the full tested range with no receptivity loss or damage increase |
| Restorative reserve | `M`, `G_restoration`, `R_P` | How much recoverable headroom remains after exchange-induced strain? | distance from critical constraint; spare actuator/control authority; recoverable energy or material margin; repair capacity; recovery half-life after a standardized perturbation; area under the viable-response curve before failure | slower recovery, hysteresis, accumulated unrepaired damage, exhaustion of control authority, failure after repeated otherwise-tolerable loads | the manuscript currently conflates memory, maturity, learned recovery, and spare reserve in one variable `M` | transformation completes and remains stable despite zero measurable recovery capacity, no spare margin, and repeated perturbation |

## Derived-variable table

| Variable | Current manuscript meaning | Minimum measurement requirement | Review finding |
|---|---|---|---|
| `G_i(t)` | normalized viability gate in `[0,1]` | explicit raw measurement, normalization map, uncertainty interval, and threshold rationale | usable only after domain-specific calibration; the normalized score must not be assigned by intuition alone |
| `Theta_i` | viability threshold for gate `i` | independently justified critical value or empirically estimated change point | thresholds should be preregistered or estimated out of sample to avoid moving them after observing failure |
| `Phi_i = [Theta_i-G_i]_+` | one-sided violation | reliable gate and threshold estimates | mathematically clear, but its empirical meaning inherits every uncertainty in `G_i` and `Theta_i` |
| `L_i` | direct load on gate `i` | measured forcing with stated units and temporal aggregation | should remain dimensional until a documented normalization is applied |
| `kappa_ij` | cascade coupling between violated gates | lagged response or intervention data capable of distinguishing cross-gate effects | cannot be inferred from simultaneous decline alone; common-cause stress is an alternative explanation |
| `M` | memory, maturity, or restorative reserve | separate measurements for learned recovery history and present spare capacity | **must be split**; a history variable and a remaining-reserve variable are not interchangeable |
| `J_raw = Pi Delta` | exchange delivered across the boundary | measured permeability/capacity and driving gradient, or direct flux measurement | likely one of the most operationally tractable quantities in membrane and engineering domains |
| `rho` | receptivity | an uptake or productive-conversion measure independent of the gates used to predict it | should initially be measured as an outcome such as `J_eff/J_raw`, not defined solely as a product of gates |
| `J_eff = rho J_raw` | productively received exchange | independent target-conversion or retained-uptake measure | central, testable CVT distinction; avoid making the equation true only by defining `rho = J_eff/J_raw` and then treating it as explanatory |
| `D(t)` | accumulated damage | domain-specific damage index with observable repair and degradation components | symbol conflicts conceptually with `D` used for preserved distinction in the four-condition invariant; rename one of them |
| `R_risk` | domain-specific risk pressure | separately measured hazard term | too open-ended for a general equation unless each application specifies its contents before fitting |
| `X(t)` | transformation variable | independently defined target-state variable | appropriate only when “substantial transformation” and `X_crit` are fixed before evaluation |
| `R_host` | current capacity to receive the transition | independently estimated host margin | current formula may double-count factors because `rho` is itself defined from gates and is then multiplied by additional gates |
| `R_P` | reserve used in the Minimum Viable Host condition | measured spare capacity with units or transparent normalization | the proposed linear threshold is a simulation hypothesis, not yet a general law |
| `V = product_i G_i` | total viability | independently observed viability outcome against which candidate aggregators can be compared | product form expresses non-compensability but must compete empirically with minimum, soft-min, log-barrier, and viability-set intersection models |

## Four immediate formal corrections

### 1. Separate memory from reserve

The manuscript lets `M` denote memory, maturity, or restorative reserve. These are different state variables.

A cleaner first formulation would use:

- `H(t)` — accumulated recovery history, learning, or maturity;
- `S(t)` — currently available restorative spare capacity.

`H` may improve recovery efficiency, while `S` is consumed by strain and replenished by repair. A mature system can still have exhausted reserve; a system with large reserve may have little learned recovery history.

### 2. Remove the symbol collision for `D`

`D` denotes preserved distinction in the invariant and accumulated damage in the dynamics. This is not merely typographic: it obscures the difference between loss of identity and material or functional injury.

Recommended notation:

- `Q` or `G_dist` for preserved distinction;
- `D` for accumulated damage.

### 3. Measure receptivity before defining it as a gate product

The most direct empirical estimate is an uptake ratio or productive-conversion measure:

`rho_obs = retained productive output / delivered input`,

with a domain-specific time window and loss accounting.

The gate product can then be tested as a predictor of observed receptivity:

`rho_hat = f(G_1, ..., G_k)`.

This avoids defining receptivity through the same gates later used to explain it.

### 4. Treat the product as one candidate aggregator

The product form captures a desired logical property: a near-zero essential gate sharply lowers total viability. It does not establish that literal multiplication is the correct empirical rule.

At minimum, compare:

- product: `product_i G_i`;
- minimum gate: `min_i G_i`;
- soft minimum;
- weighted geometric mean;
- log-barrier score;
- intersection of domain-specific viability constraints.

The strongest CVT claim may be **essential-gate non-compensability**, not the universal truth of one aggregator.

## Minimal empirical or simulation protocol

1. **Choose one bounded domain.** Begin with a membrane or engineering system where flux, uptake, damage, and recovery can be measured.
2. **Define viability independently.** Specify the outcome that counts as continued viable operation before calculating CVT gates.
3. **Measure raw and effective exchange separately.** Record delivered input, retained productive uptake, rejected load, and damage.
4. **Operationalize each gate.** Publish the raw variable, normalization rule, threshold, uncertainty, and timescale.
5. **Perturb one mechanism at a time where possible.** Change permeability, uptake capacity, repair capacity, or interface integrity while holding other conditions as stable as feasible.
6. **Compare aggregators out of sample.** Test product, minimum, soft-min, and constraint-intersection forms against observed viability.
7. **Search deliberately for counterexamples.** Include systems with high exchange and low damage, low reserve and successful transformation, or blurred distinction without functional collapse.
8. **Test delayed failure.** Evaluate viability after the transformation, not only at the moment the target state is reached.

## Domain priority

The first serious operationalization should not span physical, biological, institutional, human–AI, and theological domains simultaneously. The cleanest sequence is:

1. **membrane or controlled transport model** — establishes raw/effective exchange and boundary regulation;
2. **reproducible toy dynamical system** — compares aggregators and tests reserve/receptivity thresholds;
3. **fusion illustration** — retained only after terminology and operational limits are audited against reactor-physics literature;
4. later cross-domain studies — each with its own proxies and falsification conditions.

## Executive verdict

The manuscript contains a testable core, but operationalization reveals three load-bearing vulnerabilities:

1. memory/maturity and restorative reserve are presently conflated;
2. receptivity risks circular definition;
3. the product-gate equation expresses the intended logic but has not yet earned status as the uniquely appropriate model.

These are productive findings, not reasons to abandon the framework. They identify the exact work required to turn CVT from a persuasive structural synthesis into a theory that can lose against evidence.

## Next decision

Before revising `main.tex`, prepare a dedicated **Limitations, Falsifiability, and Scope Conditions** artifact that incorporates these findings. Only then should the Abstract and Introduction be rewritten.