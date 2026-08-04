# CVT Regulated-Transport Validation — Stage 3 Model-Comparison Preregistration

**Date:** 2026-08-04  
**Status:** frozen pre-fit comparison design; no candidate model has been fitted  
**Parent artifacts:** regulated-transport validation protocol, frozen simulation specification, Stage 1/1.5 numerical verification, Stage 2 proxy audit, Stage 2.5 sham-adjusted probe qualification  
**Primary outcome:** hosted transformation  
**Final test partition:** unopened

## 1. Question

Does the pre-outcome four-condition representation

```text
B = bounded coupling
Q = preserved organization
C = sham-adjusted local marginal productive response
S = currently available restorative reserve
```

provide useful out-of-sample prediction or diagnosis of hosted transformation beyond simpler forcing, transport, and domain-native state models?

This stage preregisters the contest before model fitting. It does not presume that all four conditions are necessary, sufficient, non-compensable, or best represented by one aggregation rule.

## 2. Epistemic status

This experiment can provide evidence about one normalized simulated regulated-transport host. It cannot establish a universal CVT law or empirical membrane validity.

Three distinct possible achievements are separated:

1. **incremental prediction:** the four-condition representation improves prediction over simpler forcing and transport baselines;
2. **predictive compression:** a four-variable CVT model approaches the performance of a much larger native-state model with materially fewer inputs;
3. **structural diagnosis:** counterexamples and failure modes are organized in a way that remains interpretable across forcing regimes.

None of these is equivalent to proving necessity or sufficiency.

## 3. Frozen partitions and access rules

The original partition sizes remain:

```text
training   = 12,000 runs
validation =  4,000 runs
final test =  4,000 runs
```

### 3.1 Training subdivision

Before fitting, the 12,000 training rows are deterministically divided by row identifier hash into:

```text
fit subset         = 9,000 rows
calibration subset = 3,000 rows
```

The fit subset is the only source for feature transformation parameters, coefficient fitting, threshold search, and hyperparameter selection. Five-fold cross-validation within the fit subset is stratified jointly by hosted outcome and forcing family.

The calibration subset is used only to map locked model scores to probabilities. It cannot select features, aggregation families, thresholds, or hyperparameters.

### 3.2 Validation use

The 4,000-row validation partition is opened only after every candidate has been fitted and calibrated from training data. It is used once to:

- compare the frozen candidates;
- choose one primary CVT candidate;
- choose one primary native/baseline comparator;
- examine preregistered counterexamples;
- lock the final comparison before test opening.

No feature, proxy, model family, or hyperparameter may be changed in response to validation results without starting a new experiment version.

### 3.3 Final test composition

The 4,000-row test partition contains four prespecified blocks of 1,000 rows each:

1. **in-distribution replication:** independent draws from the training design envelope;
2. **repeated-pulse shift:** repeated-pulse schedules held out from primary fitting;
3. **excessive-forcing shift:** forcing above the ordinary safe-routing region;
4. **experienced-but-exhausted hosts:** high history `H` with low initial reserve `S(0)/S_max`.

The block labels and counts may be known. Test outcomes, candidate predictions, and performance summaries remain unopened until the model-lock conditions in Section 18 are satisfied.

## 4. Outcomes

### 4.1 Primary binary outcome

```text
Y_hosted = 1
```

only when both conditions hold:

1. productive uptake reaches the frozen intervention target;
2. every frozen viability condition holds through the full follow-up horizon, including terminal reserve.

The outcome is computed by the native simulator and does not use `B,Q,C,S`.

### 4.2 Secondary outcomes

The following are diagnostic and cannot replace the primary selection outcome:

- target reached;
- viable through follow-up;
- productive uptake at intervention end;
- peak damage;
- minimum integrity;
- peak free internal load;
- terminal reserve;
- reason for non-hosting.

## 5. Evaluable population and invalid measurements

The primary head-to-head comparison uses the common-complete subset on which the frozen primary capture probe is valid.

An invalid capture probe is not imputed as zero or clipped into validity. The invalid fraction is reported for every partition.

Rules:

- if the invalid fraction is at most `1%`, primary comparisons use the common-complete subset and baselines are additionally reported on the full partition;
- if the invalid fraction exceeds `1%` in training or validation, Stage 3 fitting stops and the measurement protocol must be revised before the final test is touched;
- if the invalid fraction exceeds `1%` only in the final test, the locked comparison is reported as transportability-limited and no confirmatory success claim is allowed.

Numerical-invalid or accounting-invalid simulator runs are excluded before partitioning and their frequency is reported.

## 6. Frozen primary CVT inputs

The primary gate vector is

```text
G = [G_B, G_Q, G_C, G_S].
```

Definitions:

- `G_B`: the frozen two-sided scheduled-forcing score calculated from the prescribed schedule and intact-interface approximation;
- `G_Q`: initial integrity `Q(0)`;
- `G_C`: the Stage 2.5 primary sham-adjusted probe score;
- `G_S`: initial reserve fraction `S(0)/S_max`.

All are pre-outcome quantities.

### 6.1 Sensitivity gate vectors

After the primary validation table is complete, two prespecified sensitivity reruns are allowed without changing any other model setting:

1. replace `G_C` with the frozen 2.5x-dose sham-adjusted probe;
2. replace `G_C` with the direct structural composite retained from Stage 2.

The direct composite is never allowed to become the primary `C` measurement because it algebraically reuses `Q` and `S`.

## 7. Schedule descriptors for baseline models

The following quantities are computed from the prescribed schedule without realized trajectories:

```text
forcing_family
peak_source_concentration
peak_permeability
active_duration
pulse_count
scheduled_peak_intact_flux
scheduled_intact_dose
```

where

```text
scheduled_peak_intact_flux
= max_t Pi(t) * max(0, c_B(t) - c_A(0))
```

and `scheduled_intact_dose` is the intervention-window integral of the same intact-interface expression.

Forcing family is one-hot encoded with `constant` as the reference category. No realized flux, productive uptake, damage, reserve loss, or follow-up state may enter a pre-outcome predictor.

## 8. Domain-native pre-outcome features

### 8.1 Initial-state features

```text
c_A(0)
P(0)/P_cap
U(0)/U_max
D(0)
S(0)/S_max
Q(0)
H
```

### 8.2 Mechanistic-margin features

```text
productive_headroom = 1 - P(0)/P_cap
buffer_headroom     = 1 - U(0)/U_max
damage_margin       = D_max - D(0)
integrity_margin    = Q(0) - Q_min
reserve_fraction    = S(0)/S_max
free_load_margin    = c_max - c_A(0)
```

### 8.3 Full native parameter features

The full-native baseline may use all prespecified run parameters available before simulation:

```text
P_cap, U_max, S_max,
k_p, k_b, k_rel, k_e,
r_S, k_rep, r_Q,
c_safe, U_safe, c_Q, J_safe,
K_S, K_Q, S_export, K_rep, K_QS,
k_d1, k_d2, k_d3,
a_p, a_e, a_b, a_r,
b_D, b_L,
H
```

The two mechanism switches remain fixed at their primary values and are not predictive features in the primary dataset.

## 9. Preregistered CVT candidates

Every score is oriented so that a larger value represents greater predicted hosting viability. A fitted negative orientation is an explicit theory-facing failure and may not be hidden by relabeling.

### CVT-1: product

```text
Z_product = G_B * G_Q * G_C * G_S
```

### CVT-2: minimum

```text
Z_min = min(G_B, G_Q, G_C, G_S)
```

### CVT-3: equal-weight geometric mean

```text
Z_geo = (G_B * G_Q * G_C * G_S)^(1/4)
```

`CVT-1` and `CVT-3` have identical rankings. They are retained only to test calibration-shape sensitivity and cannot be counted as independent conceptual confirmations.

### CVT-4: soft minimum

```text
Z_softmin(tau)
= -tau * log(mean(exp(-G_i/tau))).
```

Candidate `tau` values are frozen at:

```text
0.02, 0.05, 0.10, 0.20, 0.50
```

Selection occurs by five-fold fit-subset cross-validated Brier score.

### CVT-5: direct-constraint margin

For gate thresholds `theta_i`, define

```text
Z_constraint = min_i(G_i - theta_i).
```

Each threshold candidate is one of the fit-subset empirical gate quantiles:

```text
10%, 20%, ..., 90%.
```

All `9^4 = 6,561` combinations are evaluated by five-fold fit-subset cross-validation. Thresholds are selected before calibration and before validation opening.

### CVT-6: monotone main-effects model

```text
logit(p) = alpha + beta_B G_B + beta_Q G_Q + beta_C G_C + beta_S G_S
```

with

```text
beta_i >= 0.
```

L2 penalty candidates are:

```text
lambda = 0, 1e-4, 1e-3, 1e-2, 1e-1, 1
```

selected by five-fold fit-subset Brier score.

### CVT-7: monotone pairwise model

This secondary flexible model adds the six pairwise products `G_i G_j`, with all main and interaction coefficients constrained nonnegative. It uses the same penalty grid.

It tests whether the four-variable decomposition is useful when one fixed aggregator is too restrictive. It cannot establish support for strict non-compensability.

## 10. Preregistered baselines

### BL-0: prevalence-only

A constant probability equal to the hosted prevalence in the fit subset, recalibrated only if the calibration procedure changes it.

### BL-1: forcing-only

Uses only the schedule descriptors in Section 7.

### BL-2: transport-only

Uses the schedule descriptors plus initial `c_A(0)`.

### BL-3: mechanistic margins

Uses the schedule descriptors and the six mechanistic-margin features in Section 8.2.

### BL-4: raw initial state

Uses the schedule descriptors and all initial-state features in Section 8.1.

### BL-5: full native logistic

Uses the schedule descriptors, initial-state features, and all full native parameters in Section 8.3.

### BL-6: full native gradient boosting

A nonlinear stress-test baseline uses the same inputs as `BL-5` and no realized trajectory variables.

Frozen tuning grid:

```text
max_leaf_nodes  = 7, 15, 31
learning_rate   = 0.03, 0.10
max_iter        = 100, 300
min_samples_leaf = 20, 50
```

The boosting baseline is eligible to demonstrate that the native state contains nonlinear predictive information not retained by CVT. It is not eligible for a parsimony advantage.

## 11. Preprocessing

All preprocessing is fitted on the 9,000-row fit subset only.

Rules:

- gate scores remain on their frozen `[0,1]` scale;
- strictly positive kinetic, capacity, and cost parameters are natural-log transformed and then standardized;
- other continuous baseline features are standardized to fit-subset mean zero and unit variance;
- one-hot family indicators are not standardized;
- a zero-variance feature is dropped and recorded;
- no outcome-dependent discretization, normalization, or feature construction is allowed;
- no post-outcome trajectory summary is allowed;
- no missing probe value is imputed.

## 12. Fitting and probability calibration

### 12.1 Fit-subset tuning

Hyperparameters and direct-constraint thresholds are selected only by five-fold cross-validation within the 9,000-row fit subset.

Primary tuning score:

```text
mean cross-validated Brier score.
```

Tie rule:

- differences below `0.0005` are treated as a tuning tie;
- the lower-complexity setting is selected;
- if complexity is equal, the stronger regularization or smoother setting is selected.

### 12.2 Base fitting

After tuning, each candidate is refitted on the full 9,000-row fit subset.

- scalar CVT scores are not allowed an additional feature search;
- logistic baselines use L2 regularization with the same frozen penalty grid as `CVT-6`;
- class weights remain uniform;
- no oversampling or outcome rebalancing is used.

### 12.3 Calibration subset

Every candidate receives one probability-calibration step on the 3,000-row calibration subset.

- scalar scores use a two-parameter logistic map `logit(p)=a+bZ` with `b>=0`;
- fitted logistic models use Platt recalibration on their predicted log odds;
- gradient boosting uses Platt recalibration on clipped predicted log odds;
- calibration uses a fixed weak L2 penalty `1e-6` for numerical stability;
- isotonic regression is not allowed in the primary analysis.

The calibration subset cannot alter model selection or hyperparameters.

## 13. Validation metrics

### 13.1 Primary metric

```text
Brier score for Y_hosted.
```

### 13.2 Secondary predictive metrics

- log loss;
- AUROC;
- area under the precision-recall curve;
- calibration intercept;
- calibration slope;
- expected calibration error using ten equal-count bins.

### 13.3 High-confidence false-safe metrics

Define a high-confidence safe prediction as

```text
predicted probability >= 0.80.
```

Report:

```text
false-safe rate = P(Y_hosted=0 | p>=0.80)
coverage        = P(p>=0.80)
```

A false-safe rate is marked statistically uninformative when fewer than 50 rows satisfy the high-confidence condition.

Failure reasons among false-safe cases are reported separately:

- target not reached;
- damage violation;
- integrity violation;
- free-load violation;
- buffer violation;
- terminal-reserve violation;
- multiple violations.

The same quantities are also reported at the ordinary `0.50` threshold, but the `0.80` results are primary for safety interpretation.

## 14. Uncertainty and paired comparison

Use 2,000 paired bootstrap resamples for validation and final-test comparisons.

Resampling is stratified by:

- hosted outcome;
- forcing family for training-like validation;
- test block for final testing.

The same bootstrap indices are used for every model in a paired comparison.

Report percentile 95% confidence intervals for metrics and metric differences. Confidence intervals are descriptive evidence; no isolated `p` value determines the scientific conclusion.

## 15. Validation selection rules

The best CVT candidate and best baseline candidate are selected separately.

Primary ordering:

1. lowest validation Brier score;
2. when the absolute Brier difference is below `0.002` or its paired 95% interval includes zero, treat the candidates as tied;
3. among tied candidates, prefer the lower high-confidence false-safe rate when both have at least 50 high-confidence predictions;
4. if still tied, prefer fewer fitted parameters;
5. if still tied, prefer the structurally simpler model.

The winning test comparison is therefore fixed as:

```text
best locked CVT candidate
versus
best locked baseline candidate.
```

All other candidates remain in the final table as secondary prespecified comparisons. Test performance cannot be used to select a different winner.

## 16. Complexity accounting

For every candidate report:

- number of input variables;
- number of fitted coefficients;
- number of fitted thresholds;
- number of selected hyperparameters;
- calibrator parameter count;
- total fitted scalar count;
- training runtime and prediction runtime;
- missing/invalid measurement dependence.

For tree boosting, also report total terminal leaves.

The product, minimum, and geometric candidates each count two fitted calibration parameters. Soft minimum additionally counts selected `tau`. Direct constraints additionally count four thresholds.

## 17. Decision criteria

### 17.1 Incremental predictive value

CVT has practically meaningful incremental value over simpler forcing/transport models only when the locked best CVT candidate:

1. improves validation Brier by at least `0.005` absolute and `2%` relative against the best of `BL-0`, `BL-1`, and `BL-2`;
2. has a paired 95% Brier-difference interval excluding zero in the favorable direction;
3. does not worsen high-confidence false-safe rate by more than `0.02` absolute when both rates are estimable.

### 17.2 Predictive compression

CVT achieves predictive compression relative to the best of `BL-5` and `BL-6` only when:

1. its Brier score is no more than `0.005` worse;
2. the upper bound of the paired 95% interval for CVT-minus-native Brier is no greater than `0.010`;
3. it uses no more than one third as many pre-outcome input variables;
4. its high-confidence false-safe rate is not more than `0.02` worse.

CVT need not beat the full native model to achieve compression.

### 17.3 Safety-screening limitation

No model may be described as a useful high-confidence safe screen when:

- high-confidence coverage is below `5%`;
- fewer than 50 high-confidence predictions are available;
- false-safe rate exceeds `10%`;
- calibration slope lies outside `[0.8,1.2]` or calibration intercept outside `[-0.1,0.1]` on final test.

### 17.4 No-support outcomes

The simulation provides no predictive support for the current CVT operationalization when any of the following occurs:

- no CVT candidate materially improves on forcing-only or transport-only models;
- the orientation of a primary CVT score must be reversed to predict hosting;
- probe invalidity exceeds the frozen tolerance;
- performance depends materially on the 2.5x probe dose;
- all CVT candidates are poorly calibrated after the frozen calibration procedure;
- the full native models dominate by more than `0.010` Brier without compression equivalence;
- high-confidence false-safe performance is unacceptable.

Negative results are retained as valid outcomes of the study.

## 18. Necessity, sufficiency, and counterexample reporting

The direct-constraint thresholds define a diagnostic classification only; they do not prove causal necessity or sufficiency.

Preserve and report:

```text
necessity counterexample:
Y_hosted=1 and at least one gate is below its learned threshold

strong necessity counterexample:
Y_hosted=1 and at least one gate is more than 0.10 below threshold

sufficiency counterexample:
all gates meet thresholds but Y_hosted=0
```

Report counts, fractions, forcing families, and failure mechanisms. Counterexamples cannot be removed as outliers unless the native run itself violates frozen numerical or accounting validity rules.

A counterexample fraction of at least `5%` is treated as a substantive contradiction of the corresponding simple necessity or sufficiency interpretation in this simulated domain.

## 19. Final refit and one-way test opening

After validation selection:

1. write `model_lock.json` containing the selected CVT and baseline IDs, all hyperparameters, thresholds, preprocessing parameters, software versions, data hashes, and validation-report hash;
2. merge the validation-selection artifact before test execution;
3. concatenate training and validation partitions;
4. deterministically split the 16,000 rows by hash into 12,000 final-fit and 4,000 final-calibration rows;
5. refit the selected candidates using locked settings only;
6. recalibrate using the final-calibration rows;
7. archive model coefficients/objects and checksums;
8. execute the final-test script once.

The test script must refuse to run without the exact preregistration and model-lock hashes.

All prespecified candidates may be evaluated in the one test execution, but only the validation-selected CVT-versus-baseline pair is the primary comparison.

Any change to equations, outcomes, proxies, features, preprocessing, models, hyperparameters, or selection rules after test opening creates a new exploratory version. A new confirmatory test requires a new independent test seed.

## 20. Test reporting

Report overall test performance and each of the four test blocks separately.

The final conclusion must distinguish among:

- incremental predictive value;
- predictive compression;
- calibration and false-safe performance;
- robustness under distribution shift;
- necessity counterexamples;
- sufficiency counterexamples;
- sensitivity to the alternative probe and direct structural composite.

Do not collapse these into a single statement that CVT is “validated.”

## 21. Immediate next action

After this preregistration is reviewed and merged, implement **Stage 3.1 dataset generation and integrity checks**:

- generate training and validation only;
- preserve final-test generation code without opening outcomes;
- verify class balance, family counts, accounting, probe validity, determinism, and partition disjointness;
- write dataset manifests and checksums;
- do not fit candidate models until the generated training/validation dataset passes integrity review.
