# CVT Foundations — Regulated-Transport Simulation Specification

**Date:** 2026-08-03  
**Status:** frozen pre-implementation specification; not evidence for CVT  
**Parent protocol:** `2026-08-03-regulated-transport-validation-protocol.md`  
**Purpose:** fix the first simulation's states, equations, accounting, parameter ranges, thresholds, forcing regimes, and data partitions before code is written.

## 1. Scope and design principle

This specification defines a deliberately minimal two-compartment transport host. It is not intended to imitate a particular biological membrane, industrial separator, or reactor interface. Its role is methodological: create a transparent system in which delivered load, productive capture, buffering, safe rejection, harmful retention, damage, reserve, and organization can be measured separately.

The simulation must be rich enough to produce delayed failure and competing pathways, but simple enough that every unit is auditable.

No equation below is claimed as a universal CVT law.

## 2. Declared host, boundary, and horizon

- **Source environment:** compartment `B`.
- **Host:** receiving compartment `A` together with its interface, productive pathway, buffer, export pathway, repair reserve, and integrity state.
- **Boundary:** regulated interface `Gamma`.
- **Transported quantity:** one conserved nonnegative scalar load.
- **Intervention horizon:** `T_int = 20` normalized time units.
- **Follow-up horizon:** `T_follow = 30` normalized time units.
- **Total simulated horizon:** `T = 50`.
- **Default numerical step:** adaptive integration with output sampled at `dt_out = 0.05`.

The follow-up period uses zero external forcing unless a repeated-exposure scenario specifies otherwise.

## 3. State vector

The primary state vector is

```text
x(t) = [c_A, P, U, D, S, Q].
```

All states are nonnegative except where bounded explicitly.

| State | Meaning | Default range |
|---|---|---:|
| `c_A` | freely available internal load | `[0, +inf)` |
| `P` | cumulative productive uptake | `[0, +inf)` |
| `U` | temporary buffer occupancy | `[0, U_max]` |
| `D` | accumulated damage | `[0, 1]` |
| `S` | currently available restorative reserve | `[0, S_max]` |
| `Q` | identity/interface integrity | `[0, 1]` |

A run-level parameter `H in [0,1]` represents recovery history or maturity. `H` is fixed during the first experiment so that history cannot silently absorb current reserve or damage.

## 4. External inputs and controls

The source concentration `c_B(t)` and interface permeability `Pi(t)` are prescribed forcing schedules.

The inward raw flux is

```text
J_raw(t) = max(0, Pi(t) * Q(t) * [c_B(t) - c_A(t)]).
```

Multiplication by `Q` means loss of interface integrity reduces controlled inward transport. This is a domain-specific design choice, not a CVT identity. A sensitivity run must remove the `Q` factor to test dependence on this choice.

## 5. Routing architecture

Incoming load is routed among productive capture, buffering, safe rejection, and harmful internal accumulation.

### 5.1 Productive capture

The productive capture rate is

```text
J_prod = k_p * c_A * F_cap * F_res * F_int.
```

where

```text
F_cap = max(0, 1 - P / P_cap)
F_res = S / (K_S + S)
F_int = Q / (K_Q + Q).
```

`P_cap` is the productive capacity available during one run. Productive uptake slows as that capacity fills, reserve is exhausted, or organization deteriorates.

### 5.2 Buffer intake and release

Buffer intake is

```text
J_buf_in = k_b * c_A * max(0, 1 - U / U_max).
```

Buffer release is

```text
J_buf_out = k_rel * U * F_res * F_int.
```

Released buffer returns to the free internal pool and may later be productively captured or rejected.

### 5.3 Safe rejection/export

Safe rejection is

```text
J_reject = k_e * c_A * F_export,
F_export = min(1, S / S_export).
```

Safe rejection consumes reserve but is not counted as damage. This distinction is mandatory: non-uptake is not automatically harm.

### 5.4 Harmful load

The free internal pool `c_A` is the potentially harmful retained load. Damage rises when `c_A` exceeds a preregistered tolerance `c_safe` or when buffer occupancy exceeds `U_safe`.

## 6. State equations

### 6.1 Free internal load

```text
dc_A/dt = J_raw + J_buf_out - J_prod - J_buf_in - J_reject.
```

The solver must enforce `c_A >= 0` without creating or deleting mass beyond numerical tolerance.

### 6.2 Productive pool

```text
dP/dt = J_prod.
```

`P` is cumulative and does not decay in the first model.

### 6.3 Buffer

```text
dU/dt = J_buf_in - J_buf_out.
```

### 6.4 Damage

```text
dD/dt = k_d1 * [c_A - c_safe]_+
       + k_d2 * [U - U_safe]_+
       + k_d3 * [J_raw - J_safe]_+
       - k_rep * H * S/(K_rep + S) * D.
```

Damage is projected to `[0,1]`. The direct raw-flux term is included only in the primary specification and must be removed in a sensitivity model, because high flux may be harmless when routing capacity is adequate.

### 6.5 Reserve

```text
dS/dt = r_S * H * (S_max - S)
       - a_p * J_prod
       - a_e * J_reject
       - a_b * J_buf_out
       - a_r * k_rep * H * S/(K_rep + S) * D.
```

Reserve is projected to `[0,S_max]`. Productive capture, export, buffer release, and repair all consume reserve. The coefficients permit these costs to differ.

### 6.6 Integrity

```text
dQ/dt = r_Q * H * S/(K_QS + S) * (1 - Q)
       - b_D * D * Q
       - b_L * [c_A - c_Q]_+ * Q.
```

`Q` is projected to `[0,1]`. Integrity can recover only when reserve remains available.

## 7. Accounting identity

For every run and accounting window, define

```text
M_delivered = integral J_raw dt
M_productive = Delta P
M_rejected = integral J_reject dt
M_buffered = Delta U
M_free = Delta c_A
```

The conservation identity is

```text
M_delivered + U(t0) + c_A(t0)
= M_productive + M_rejected + U(t1) + c_A(t1) + residual.
```

Damage and reserve are not transported mass and therefore do not enter this identity.

Required tolerance:

```text
abs(residual) <= max(1e-8, 1e-6 * M_delivered).
```

Runs violating the tolerance are invalid simulation output and must not enter model comparison.

## 8. Hosted-transformation outcome

### 8.1 Transformation target

A run reaches the target when

```text
P(T_int) - P(0) >= X_crit.
```

Default:

```text
X_crit = 4.0.
```

### 8.2 Viable set

The primary viable set requires, for all `t in [0,T]`:

```text
D(t) <= D_max = 0.45
Q(t) >= Q_min = 0.55
c_A(t) <= c_max = 5.0
U(t) <= U_max
```

and at terminal follow-up:

```text
S(T) >= S_terminal = 0.15 * S_max.
```

A run is **hosted** only if the transformation target is reached and every viability condition holds through follow-up.

Thresholds are simulation-design choices. Sensitivity analysis must vary each by plus or minus 20 percent and examine whether conclusions survive.

## 9. Pre-outcome CVT observables

All primary gate proxies are calculated at `t = 0` or from the prescribed forcing schedule, never from the run's realized hosted outcome.

### 9.1 Bounded coupling proxy

Let the scheduled peak raw forcing under the intact-interface approximation be

```text
J_sched_peak = max_t Pi(t) * max(0, c_B(t) - c_A(0)).
```

With independently calibrated lower and upper useful bounds `J_low` and `J_high`, define a two-sided triangular gate:

```text
G_B = 0                                      if J_sched_peak <= 0
G_B = J_sched_peak / J_low                   if 0 < J_sched_peak < J_low
G_B = 1                                      if J_low <= J_sched_peak <= J_high
G_B = max(0, 1 - (J_sched_peak-J_high)/W_B)  if J_sched_peak > J_high.
```

### 9.2 Preserved-organization proxy

```text
G_Q = Q(0).
```

A secondary proxy may combine `Q(0)` with initial actuator availability, but it must be preregistered as a separate model.

### 9.3 Capture-readiness proxy

Primary proxy:

```text
G_C = geometric_mean(
    max(0, 1 - P(0)/P_cap),
    Q(0),
    S(0)/(K_S + S(0))
).
```

Because this proxy overlaps with `Q` and `S`, it is intentionally vulnerable to redundancy criticism. Therefore a mandatory alternative proxy uses a pre-run micro-probe:

1. apply a fixed small pulse for `0.25` time units;
2. measure productive capture divided by delivered probe load;
3. restore the initial state exactly before the evaluated run.

The simulator must support both proxies and report whether conclusions depend on the proxy choice.

### 9.4 Restorative-reserve proxy

```text
G_S = S(0) / S_max.
```

A vector-margin version using initial reserve, export headroom, and buffer headroom must also be tested through direct constraints.

## 10. Candidate aggregators and baselines

Candidate CVT representations:

```text
V_intersection = all(G_i >= Theta_i)
V_product      = G_B * G_Q * G_C * G_S
V_min          = min(G_B,G_Q,G_C,G_S)
V_geo          = product(G_i ** w_i), sum(w_i)=1
V_softmin      = -tau * log(mean(exp(-G_i/tau)))
```

The flexible predictor may use logistic regression with main effects and preregistered pairwise interactions. A tree-based exploratory model may be reported separately but cannot replace the preregistered comparison.

Required baselines:

1. forcing-only: schedule amplitude and duration;
2. transport-only: `Pi`, concentration gradient, and initial `c_A`;
3. raw-state: all initial physical states and forcing variables without gate normalization;
4. transport-plus-damage-capacity: raw state plus `c_safe`, `U_max`, and repair parameters;
5. reduced subsets of `B,Q,C,S` selected only on validation data.

## 11. Parameter ranges

All parameters are dimensionless normalized values for the first experiment.

| Parameter | Range | Default |
|---|---:|---:|
| `P_cap` | `[5,12]` | `8` |
| `U_max` | `[2,8]` | `5` |
| `k_p` | `[0.4,1.5]` | `0.9` |
| `k_b` | `[0.2,1.2]` | `0.6` |
| `k_rel` | `[0.05,0.5]` | `0.2` |
| `k_e` | `[0.1,1.0]` | `0.4` |
| `S_max` | `[3,10]` | `6` |
| `r_S` | `[0.01,0.15]` | `0.05` |
| `k_rep` | `[0.05,0.5]` | `0.2` |
| `r_Q` | `[0.01,0.15]` | `0.04` |
| `c_safe` | `[0.5,2.0]` | `1.0` |
| `c_Q` | `[1.0,3.0]` | `2.0` |
| `J_safe` | `[0.5,3.0]` | `1.5` |
| `H` | `[0,1]` | sampled |
| `Q(0)` | `[0.35,1]` | sampled |
| `S(0)/S_max` | `[0.05,1]` | sampled |
| `U(0)/U_max` | `[0,0.8]` | sampled |
| `D(0)` | `[0,0.35]` | sampled |

Cost and damage coefficients are sampled log-uniformly over a factor-of-three range around defaults recorded in `parameters.csv`.

## 12. Forcing families

Every scenario belongs to one preregistered family.

1. **Constant:** fixed `c_B` and `Pi` during intervention.
2. **Short pulse:** elevated forcing for 2 to 5 units, then zero.
3. **Sustained:** elevated forcing for all 20 intervention units.
4. **Repeated pulse:** three equal pulses separated by partial recovery intervals.
5. **Ramp:** linearly increasing forcing.
6. **Shock plus tail:** brief high shock followed by moderate sustained forcing.

Amplitude strata are calibrated from pilot accounting-only runs:

- insufficient: below the fifth percentile of target-reaching forcing;
- admissible: middle operating region with low damage in pilot runs;
- excessive: above the ninetieth percentile of safe-routing capacity.

Pilot calibration may set forcing strata but may not fit CVT gates or evaluate final model performance.

## 13. Scenario generation and partitions

Use fixed master seed `20260803` to generate parameter combinations through Latin hypercube sampling.

- training: 12,000 runs;
- validation: 4,000 runs;
- test: 4,000 runs;
- adversarial counterexample search: separate 10,000-run budget plus targeted optimization.

Partitions are generated before gate thresholds or model weights are fit.

Required held-out tests:

1. an excessive-forcing family omitted from training;
2. an initial-state corner omitted from training (`high H, low S`);
3. a repeated-pulse family omitted from training;
4. alternative damage mechanism with direct `J_raw` damage term removed.

No test run may be used to redefine thresholds, proxies, or the viable set.

## 14. Required counterexample suites

### 14.1 Intended merger

Set the declared host to the combined `A+B` system and define homogenization as success. This is a separate analysis and must not be mixed with the primary host definition.

### 14.2 Stable hosting with negligible reserve

Search `S(0)/S_max <= 0.05` for successful hosted runs. Finding them constrains reserve necessity or reveals that the replenishment pathway substitutes for initial reserve.

### 14.3 High flux without harm

Search high `J_raw` runs with large capture/export capacity and no viability violation. These cases prevent magnitude alone from defining overload.

### 14.4 Low capture estimate with success

Search for low `G_C` and hosted success under both capture proxies.

### 14.5 Failed gate compensated

Search each `G_i < Theta_i` while the run remains hosted.

### 14.6 High gates with failure

Search all `G_i >= 0.8` with failure, especially delayed failure during follow-up.

All discovered cases are exported to `counterexamples.csv` with full trajectories and mechanism labels.

## 15. Numerical implementation rules

- primary solver: `scipy.integrate.solve_ivp`, method `LSODA` or `BDF` if stiffness is detected;
- absolute tolerance: `1e-9`;
- relative tolerance: `1e-7`;
- state projection may occur only for documented hard bounds and must report projection frequency;
- a second solver or reduced step check is required for 1 percent of runs;
- unit tests must verify nonnegativity, accounting closure, zero-forcing behavior, and monotonic cumulative `P`;
- failed integrations are reported separately and cannot be silently discarded.

## 16. Frozen primary hypotheses

The primary evaluation will test:

- `H1`: at least one CVT representation improves held-out hosted-outcome prediction over forcing-only and transport-only baselines;
- `H2`: the full four-gate representation improves over the best reduced gate subset by a practically meaningful margin;
- `H3`: no single scalar aggregator is assumed superior; the comparison determines whether direct constraints or a scalar representation is better supported;
- `H4`: pre-run capture readiness contributes information beyond initial `Q`, `S`, and forcing;
- `H5`: the follow-up horizon identifies failures missed by intervention-window success alone.

`H2` and `H4` may fail without invalidating the narrower distinction between transition and hosted transition.

## 17. Primary performance criteria

For binary hosted outcome:

- AUROC and precision-recall AUC;
- Brier score and calibration slope/intercept;
- false-safe rate at a threshold selected on validation data;
- false-failure rate;
- performance by forcing family and initial-state stratum.

Practical improvement requires either:

- at least `0.02` absolute improvement in test AUROC over the strongest simple baseline, or
- at least `10 percent` relative reduction in Brier score, or
- materially lower false-safe rate at matched sensitivity.

These thresholds are design conventions, not universal scientific standards.

## 18. Falsification and revision rules

The simulation constrains strong CVT claims when:

- the raw-state baseline equals or exceeds every CVT representation;
- one or more gates add no stable out-of-sample information;
- results reverse under modest threshold or normalization changes;
- capture readiness is redundant with `Q` and `S` under both proxies;
- delayed failure is not improved by reserve or damage information;
- persistent gate failure is routinely compatible with hosting;
- accounting or proxy separation cannot be maintained.

After results are viewed, changes to equations, thresholds, or host definition require a new versioned specification and a new untouched test set.

## 19. Implementation package to create next

```text
research-hub/cvt-foundations/validation/regulated-transport/
  README.md
  protocol.md
  model_equations.md
  parameters.csv
  scenarios.csv
  requirements.txt
  src/
    simulate.py
    accounting.py
    gates.py
    generate_scenarios.py
    models.py
    evaluate.py
    counterexamples.py
    make_figures.py
  tests/
    test_accounting.py
    test_bounds.py
    test_zero_forcing.py
    test_reproducibility.py
  results/
  figures/
```

## 20. Next bounded action

Implement **Stage 1 only**:

1. create the package skeleton;
2. implement equations and scenario objects;
3. verify accounting closure and numerical stability;
4. run a small smoke-test suite;
5. do not fit gates or compare CVT models yet.

Model comparison begins only after the accounting implementation passes review.