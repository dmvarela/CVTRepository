# CVT Regulated-Transport Validation — Stage 3.2 Model-Comparison Report

**Date:** 2026-08-05  
**Status:** validation opened once; primary winners locked; final test not generated or opened  
**Parent artifact:** Stage 3 model-comparison preregistration  
**Evidence source:** frozen Stage 3.1 artifact from workflow run `30966929493`

## 1. Scope

Stage 3.2 fitted every preregistered CVT candidate and native baseline using only the frozen 9,000-row fit subset, calibrated them using only the frozen 3,000-row calibration subset, and then evaluated the locked field once on the 4,000-row validation partition.

The final test partition was neither generated nor opened. The validation result does not establish empirical validity outside the declared simulated transport world.

## 2. Evidence seal and execution

The original Stage 3.1 byte hashes were machine-specific. Before model fitting, a preserved runner artifact was checked against a portable seal requiring:

- exact design-hash sequences;
- exact row identities and forcing assignments;
- exact row-level outcomes and failure labels;
- gate agreement to five decimal places;
- exact hosted, target-reaching, viability, and failure-reason counts;
- complete solver, accounting, bound, monotonicity, and probe validity.

Every check passed for both training and validation. The model comparison then used the exact preserved artifact bytes:

```text
training.csv   173206e583dfd8aacfecca20385cac693f52c81407fade603a82f46eab315a4f
validation.csv e7e49a9bfa99d61664f850fa2e78c86e31c580d4fcfcfff786a3ff360660aad4
```

The frozen direct-constraint grid contained 6,561 candidates. It was evaluated in bounded-memory blocks without changing the grid or update rule. The full comparison used 2,000 paired, outcome-and-family-stratified bootstrap resamples.

## 3. Validation performance

| Model | Inputs | Brier | 95% bootstrap interval | AUROC | Average precision |
|---|---:|---:|---:|---:|---:|
| `CVT-2-minimum` — locked CVT winner | 4 | 0.027566 | [0.026783, 0.028257] | 0.8046 | 0.1481 |
| `CVT-7-monotone-pairwise` — lowest raw CVT Brier | 4 | 0.026981 | [0.025892, 0.027903] | 0.8489 | 0.1885 |
| `BL-2-transport-only` — best simple baseline | 10 | 0.028988 | [0.028825, 0.029145] | 0.7228 | 0.0563 |
| `BL-5-full-native-logistic` | 44 | 0.023776 | [0.022119, 0.025365] | 0.9481 | 0.3289 |
| `BL-6-full-native-gradient-boosting` — locked baseline winner | 44 | 0.019194 | [0.017318, 0.021078] | 0.9726 | 0.5544 |

The pairwise CVT model had the lowest raw Brier among CVT candidates. Its advantage over the minimum model was:

```text
CVT-7 minus CVT-2 Brier = -0.000586
95% interval            = [-0.001139, -0.000075]
```

The preregistration nevertheless treats any absolute validation difference below `0.002` as a selection tie. With no estimable high-confidence false-safe comparison, the simpler candidate wins the tie. The locked CVT winner is therefore `CVT-2-minimum`.

This tie-break does not determine the scientific decision. Even the raw-best pairwise candidate remained below the preregistered practical thresholds described below.

## 4. Preregistered decisions

### 4.1 Incremental predictive value

Against the best simple baseline, `BL-2-transport-only`, the locked CVT winner achieved:

```text
absolute Brier improvement  = 0.001421
relative improvement        = 4.90%
CVT-minus-baseline interval = [-0.002219, -0.000701]
```

The improvement was stable in the paired bootstrap, but the frozen criterion required an absolute improvement of at least `0.005`. Therefore:

```text
incremental predictive value = FAIL
```

The raw-best pairwise CVT candidate improved Brier by `0.002007`, also below the `0.005` threshold.

### 4.2 Predictive compression

Relative to the best full-native model, `BL-6-full-native-gradient-boosting`, the locked CVT winner used only 4 versus 44 pre-outcome inputs:

```text
input fraction                 = 0.0909
CVT Brier disadvantage         = 0.008372
95% interval for disadvantage = [0.006441, 0.010222]
```

The frozen compression rule required a point disadvantage no greater than `0.005` and an interval upper bound no greater than `0.010`. Both the point criterion and, narrowly, the interval criterion failed. Therefore:

```text
predictive compression = FAIL
```

The raw-best pairwise CVT candidate was `0.007786` worse than gradient boosting, with interval `[0.005843, 0.009681]`; it also failed the point criterion.

The four-gate representation did approximately track a substantial part of the native signal, but it did not compress the best nonlinear native predictor closely enough under the declared standard.

## 5. Safety-screening result

No candidate qualified as a useful high-confidence safe screen on validation.

- The locked CVT winner made **zero** predictions at or above `0.80` and zero at or above `0.50`.
- The full-native gradient booster made 12 predictions at or above `0.80`, only `0.3%` coverage—far below the required 5% and 50-case minimum.
- No model met the combined count, coverage, and false-safe conditions.

This means that neither CVT nor the stronger native models may be described as a validated high-confidence safety screen from these results.

## 6. Hard-gate counterexamples

The fitted direct-constraint thresholds were:

```text
B >= 0.673592
Q >= 0.675647
C >= 0.268373
S >= 0.146056
```

They did not behave as necessary-and-sufficient gates:

```text
hosted cases failing at least one gate = 92 / 121 = 76.0%
nonhosted cases passing every gate      = 114
precision among all-gates-pass cases    = 20.3%
```

Among hosted cases below a threshold, the capture proxy failed most frequently:

```text
B failures = 30
Q failures = 34
C failures = 71
S failures = 7
```

The result rejects a literal hard-intersection reading in this simulated world. Compensation and pathway interaction are common enough that a failed single gate does not imply failure, while passing all fitted thresholds does not imply hosting.

## 7. Structural diagnostic

The flexible monotone pairwise model placed its largest positive terms on capture readiness, preserved organization, and interactions involving capture:

```text
C main effect = 4.101
Q main effect = 1.797
B x C         = 3.207
Q x C         = 3.334
C x S         = 1.434
```

The isolated main effects for `B` and `S` were driven to zero while some of their interactions remained positive.

This is consistent with a relational rather than purely additive geometry. It is not independent confirmation of a universal CVT law: the native equations themselves contain multiplicative organization and reserve terms, so the simulated world was capable of producing such interactions.

## 8. Capture-proxy sensitivity

Replacing the primary micro-probe with the frozen 2.5-times-dose probe changed the selected model's Brier by only:

```text
5.49e-8
```

The primary probe result is therefore insensitive to the declared dose perturbation.

Substituting the direct structural composite without refitting produced very poor performance (`Brier = 0.2043`) and a 93.3% false-safe rate among its high-confidence predictions. That number must be interpreted narrowly: the current sensitivity code inserted a differently scaled construct into a calibrator trained on the micro-probe. It establishes that the two measures are not interchangeable; it is not a fair estimate of how a separately fitted direct-composite model would perform.

A training/calibration-only refit of the prespecified alternative proxy is required as a secondary correction. It may not alter the locked primary winner or use final-test information.

## 9. Decision

Under the frozen Stage 3 criteria:

```text
incremental value      = not demonstrated
predictive compression = not demonstrated
safe-screen utility    = not demonstrated
```

The more precise conclusion is:

> The current four-proxy CVT operationalization contains real pre-outcome signal and modestly improves on forcing/transport-only prediction, but it does not meet the preregistered practical-improvement threshold and does not retain enough of the nonlinear native model's predictive information to qualify as compression.

This is a valid negative result for the present operationalization, not a disproof of every possible CVT formulation and not empirical validation or invalidation in external domains.

## 10. Next bounded action

Before any final-test execution, Stage 3.2.5 must:

1. materialize a reproducible scorer package for the locked `CVT-2-minimum` and `BL-6` baseline rather than relying only on metadata;
2. refit and recalibrate the prespecified capture-proxy sensitivity alternatives using training and calibration data only, without reopening model selection;
3. audit the final-test generator and lock manifest without generating the test partition;
4. decide explicitly whether to authorize the single confirmatory final-test run.

The current lock correctly records:

```text
final_test_opened = false
confirmatory_test_authorized = false
```
