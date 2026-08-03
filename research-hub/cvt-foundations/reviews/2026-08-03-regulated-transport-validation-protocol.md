# CVT Foundations — Regulated-Transport Validation Protocol

**Date:** 2026-08-03  
**Status:** preregistration-style design artifact; not empirical confirmation  
**Canonical manuscript:** `research-hub/cvt-foundations/main.tex`  
**Purpose:** specify the first bounded, reproducible test of whether the `B,Q,C,S` decomposition adds predictive or explanatory value beyond simpler transport and state-constraint models.

## 1. Validation question

For a scoped regulated-transport system, does an independently measured decomposition into:

- bounded coupling (`B`),
- preserved identity-defining organization (`Q`),
- pre-existing capture readiness (`C`), and
- available restorative reserve (`S`)

improve out-of-sample prediction or diagnosis of hosted transformation relative to simpler domain-native baselines?

The protocol does **not** presume that all four conditions are universally necessary, that their conjunction is sufficient, or that any one scalar aggregator is correct.

## 2. Minimal experimental host

Use a two-compartment regulated-transport simulation as the first reproducible host.

### 2.1 Host

The declared host is receiving compartment `A`, including:

- an internal target species or state variable `x_A(t)`;
- a finite capture or binding capacity;
- a buffer or temporary holding pool;
- a damage state;
- a restorative-resource pool;
- an interface whose permeability can be externally controlled.

Compartment `B` is the source environment. It is not part of the host for the primary analysis.

### 2.2 Boundary and transported quantity

The boundary is interface `Gamma` between `B` and `A`. The transported quantity is a conserved scalar species or normalized load.

The raw delivered flux is:

```text
J_raw(t) = Pi_Gamma(t) * [c_B(t) - c_A(t)]
```

under a declared sign convention and nonnegative inward-flow restriction for the initial experiment.

### 2.3 Transformation target

The transformation is successful uptake into a designated productive internal pool `P_A(t)`.

A run reaches the transformation target when:

```text
P_A(t1) - P_A(t0) >= X_crit
```

within the intervention window.

### 2.4 Hosted outcome

A transformation is hosted only when both conditions hold:

1. the productive-uptake target is reached; and
2. the host remains inside the independently declared viable set throughout the intervention and follow-up horizon.

The viable set must be defined before fitting CVT variables and should include limits on:

- damage;
- identity or interface integrity;
- internal overload;
- minimum restorative reserve;
- irreversible loss of control authority.

The follow-up horizon must be long enough for delayed reserve exhaustion or damage to appear.

## 3. Accounting architecture

Every unit delivered across the interface must be assigned to one of the following channels over the same accounting window:

```text
Delivered load
= productive uptake
+ safe rejection/export
+ temporary buffer accumulation
+ harmful retained load
+ numerical/accounting residual.
```

The residual must be reported and bounded by a preregistered tolerance.

### Required observables

- `J_raw`: delivered flux;
- `J_eff`: productive uptake rate or amount;
- `J_reject`: safe rejection/export;
- `J_buffer`: change in temporary buffered load;
- `J_harm`: harmful retained or unprocessed load;
- `D`: accumulated damage;
- `S_raw`: restorative-resource level;
- `Q_raw`: interface/host-organization integrity;
- recovery time after forcing ends.

Observed uptake efficiency may be computed only when numerator and denominator are commensurate:

```text
rho_obs = J_eff / J_raw.
```

It is an outcome and must not be reused to define `C`.

## 4. Independent operationalization of B, Q, C, and S

All proxies must be computed from information available before, or independently of, the target outcome for the evaluated run.

### 4.1 Bounded coupling — B

Raw observable: forcing relative to a preregistered admissible handling band.

Candidate inputs:

- current permeability;
- concentration gradient;
- recent delivered-load rate;
- independently calibrated lower and upper handling limits.

`B` must be two-sided: both starvation and overload receive low scores.

### 4.2 Preserved identity-defining organization — Q

Raw observable: integrity of the interface and internal organization required for the declared host to remain the same analytical host.

Candidate inputs:

- interface-integrity state;
- retained compartment distinction;
- continued availability of the capture and export pathways;
- controller/actuator availability.

`Q` must not be defined merely as “the run succeeded.”

### 4.3 Capture readiness — C

Raw observable: a pre-forcing estimate of the receiving state’s ability to route a specified input into the productive pool without leaving the viable set.

Candidate inputs:

- free productive-binding capacity;
- available conversion sites;
- distance to a preregistered capture-saturation boundary;
- local basin or reachable-set estimate from the pre-input state;
- a short, low-amplitude probe response conducted before the evaluated forcing window.

The low-amplitude probe must be excluded from the target accounting window or explicitly accounted for.

### 4.4 Available restorative reserve — S

Raw observable: currently available recovery headroom, not historical maturity.

Candidate inputs:

- remaining repair-resource pool;
- available buffer-release capacity;
- export reserve;
- unused actuator authority;
- thermal or processing margin.

Where these margins are not empirically reducible to one latent quantity, `S` must remain a vector or direct constraint family rather than being forced into a scalar.

## 5. Separate state variables

The simulation must distinguish:

- `H`: learned history or maturity;
- `S`: currently available reserve;
- `D`: accumulated damage.

No universal law for their dynamics is assumed. The first model may use transparent domain-specific update rules, but each rule, unit, parameter, and saturation bound must be documented.

The design must permit at least:

- high `H`, low `S` — an experienced but exhausted host;
- low `H`, high `S` — an inexperienced but well-resourced host;
- similar current gate values with different damage histories.

## 6. Forcing regimes

The protocol must include randomized or systematically sampled runs across:

1. **insufficient forcing** — below the lower handling band;
2. **admissible forcing** — inside the calibrated operating band;
3. **excessive forcing** — above the upper handling band;
4. **short pulse** versus **sustained exposure**;
5. **single exposure** versus **repeated exposure**;
6. **high capture / low reserve** and **low capture / high reserve** states;
7. **intact** versus **degraded interface** states.

The forcing schedule must be generated independently of outcome labels.

## 7. Deliberate counterexamples and boundary cases

The validation must actively search for cases that would constrain CVT.

### Required cases

- **Intended merger:** loss of compartment distinction is the declared success condition; this tests whether `Q` is host-definition dependent rather than universally mandatory.
- **Negligible measured reserve with stable hosting:** tests whether `S` is essential or whether the proxy is incomplete.
- **High flux without uptake loss or damage:** tests whether overload is truly present rather than inferred from magnitude alone.
- **Low estimated capture readiness followed by stable productive uptake:** tests proxy validity and possible omitted capture pathways.
- **One failed gate compensated by another:** directly tests strict non-compensability.
- **All four gates high but hosted transformation fails:** tests insufficiency and hidden-state risk.
- **All four gates apparently low but the host succeeds:** tests normalization, host definition, and whether the decomposition adds value.

Counterexamples must be reported, not removed as outliers unless a preregistered data-quality rule applies.

## 8. Candidate models

All models must predict the same independently declared hosted outcome.

### CVT candidates

1. direct simultaneous constraints;
2. unweighted product;
3. minimum gate;
4. weighted geometric mean;
5. normalized soft minimum;
6. a flexible nonlinear predictor using `B,Q,C,S` with complexity control.

### Required baselines

1. raw-flux-only model;
2. permeability-plus-gradient transport model;
3. transport-plus-damage model;
4. domain-native state-constraint model using the raw state vector without CVT normalization;
5. reduced model selected from the smallest subset of `B,Q,C,S` that performs comparably.

The CVT decomposition earns value only if it improves prediction, calibration, interpretability, intervention response, or failure diagnosis beyond these baselines.

## 9. Data partition and anti-circularity rules

- Generate or reserve a final untouched test partition before fitting normalization maps or thresholds.
- Fit thresholds, weights, and transformation parameters only on training data.
- Use validation data for model selection.
- Report final performance once on the test partition.
- Include regime-held-out tests, such as training without excessive forcing and testing on it.
- Include initial-state-held-out tests to assess generalization across host conditions.
- Do not define a gate from any variable that is algebraically identical to the target outcome.
- Do not define the viable set using the aggregate CVT score.

## 10. Evaluation criteria

For binary hosted success, report at minimum:

- discrimination;
- calibration;
- confusion matrices at preregistered thresholds;
- false-safe and false-failure rates;
- performance by forcing regime;
- uncertainty intervals from repeated seeds or bootstrap resampling.

For continuous outcomes, also report:

- productive uptake;
- peak and terminal damage;
- minimum reserve;
- time outside the viable set;
- recovery time;
- accounting residual.

Model complexity must be penalized or explicitly reported. A more complex CVT model that performs only trivially better than a simple baseline does not establish practical value.

## 11. Falsification and constraint criteria

The first validation will count against strong CVT claims when one or more of the following occur reproducibly:

1. a proposed essential condition remains persistently below its threshold while hosted transformation succeeds across relevant regimes;
2. the four-condition decomposition does not outperform simpler domain-native models out of sample;
3. capture readiness adds no information once ordinary pre-state variables are included;
4. restorative reserve adds no predictive or diagnostic value beyond existing margins;
5. the preferred aggregator changes arbitrarily across seeds or minor normalization choices;
6. apparently successful results depend on leakage from outcomes into gate construction;
7. high gate scores systematically miss delayed failures;
8. the decomposition cannot be operationalized without collapsing multiple gates into the same measurement.

A negative result constrains scope; it does not justify changing the host definition after seeing outcomes unless the change is recorded as a new protocol version.

## 12. Sensitivity and robustness

The reproducible package must vary:

- normalization ranges;
- gate thresholds;
- follow-up horizon;
- measurement noise;
- time discretization;
- initial conditions;
- forcing schedule;
- reserve and damage parameters;
- accounting-window length;
- model hyperparameters.

Report which conclusions are invariant, which are fragile, and which depend on a particular operationalization.

## 13. Minimum reproducible package

Create a future directory:

```text
research-hub/cvt-foundations/validation/regulated-transport/
```

with at least:

```text
README.md
protocol.md
model_equations.md
parameters.csv
scenarios.csv
src/
  simulate.py
  accounting.py
  gates.py
  models.py
  evaluate.py
  make_figures.py
tests/
results/
  metrics.csv
  counterexamples.csv
  sensitivity.csv
figures/
environment.yml or requirements.txt
LICENSE or reuse note
```

Every run must record:

- random seed;
- code commit;
- parameter-set identifier;
- initial and boundary conditions;
- solver and tolerances;
- forcing schedule;
- full accounting channels;
- raw observables;
- normalized gates;
- predictions and outcomes.

## 14. Staged execution plan

### Stage 1 — accounting verification

Implement the minimal simulation and prove numerical accounting closure within tolerance. No CVT model comparison yet.

### Stage 2 — proxy verification

Test whether `B,Q,C,S` are independently measurable and non-duplicative. Reject or revise proxies that reuse the outcome.

### Stage 3 — preregistered model comparison

Freeze the protocol, thresholds, partitions, and model list before running the final comparison.

### Stage 4 — adversarial counterexample search

Use grid search, random search, and targeted optimization to find failures of necessity, sufficiency, and non-compensability.

### Stage 5 — publication decision

Only after the final held-out results decide whether:

- CVT Foundations remains a conceptual framework paper;
- the membrane validation becomes a companion methods/results paper;
- specific conditions or aggregators must be narrowed or abandoned;
- venue selection is justified.

## 15. Decision rule

The first validation succeeds as science even if CVT performs poorly, provided the design is reproducible and the negative evidence is preserved.

The strongest acceptable positive conclusion is bounded:

> In this declared regulated-transport model and tested regime set, independently measured `B,Q,C,S` variables provided specified predictive or diagnostic value relative to the preregistered baselines.

It must not be generalized to biology, organizations, AI, fusion, or politics without separate domain-native validation.

## 16. Immediate next artifact

The next artifact should be a short **simulation specification** that fixes:

- the state vector;
- mass-balance equations;
- interface law;
- productive capture, buffering, rejection, damage, repair, and reserve mechanisms;
- parameter ranges;
- viable-set thresholds;
- intervention and follow-up durations;
- exact train/validation/test scenario generation.

That specification must precede code so the equations are not reverse-engineered around desired results.
