# Stage 3.2.5 Closure and Architecture Memo

**Status:** closure and exploratory redirection  
**Final test:** not generated, not opened, not authorized  
**Prior locked result:** Stage 3.2 validation comparison, PR #25

## 1. Purpose

Stage 3.2.5 closes the first regulated-transport validation cycle without attempting to rescue the failed four-gate operationalization. It records the formal decision not to authorize the single confirmatory final-test run and reframes the next workstream as exploratory counterexample anatomy and theoretical revision.

The point is not to make the Stage 3.2 model win after the fact. The point is to preserve the negative result and learn from the exact way it failed.

## 2. Locked Stage 3.2 result

The locked CVT winner was:

```text
CVT-2-minimum    Brier 0.027566
```

The best native baseline was:

```text
BL-6-full-native-gradient-boosting    Brier 0.019194
```

Against the best simple transport-only baseline, the locked CVT winner improved Brier by `0.001421`, but the preregistered practical-improvement threshold was `0.005`. Against the best native model, the locked CVT winner was worse by `0.008372`, exceeding the allowed point disadvantage for predictive compression.

No candidate met the high-confidence safety-screen count and coverage conditions.

Therefore the Stage 3.2 validation result remains:

```text
incremental predictive value  not demonstrated
predictive compression        not demonstrated
safe-screen utility           not demonstrated
```

## 3. Fair capture-proxy sensitivity refit

Stage 3.2 included one capture-proxy sensitivity check that inserted the direct structural composite into a calibrator trained on the micro-probe. That result showed non-interchangeability but was not a fair separately calibrated comparison.

Stage 3.2.5 refits the locked `CVT-2-minimum` scorer fairly for each prespecified capture alternative. The calibration refit uses the frozen calibration subset only. Validation is the already-opened Stage 3.2 validation partition. The final test is not used.

| Capture proxy | Validation Brier | AUROC | Average precision | Brier minus primary |
|---|---:|---:|---:|---:|
| primary sham-adjusted micro-probe | 0.027566 | 0.8046 | 0.1481 | 0.000000 |
| 2.5x-dose sham-adjusted micro-probe | 0.027566 | 0.8046 | 0.1480 | 0.000000054 |
| direct structural composite | 0.029099 | 0.6356 | 0.0611 | 0.001532 |

The primary probe is insensitive to the frozen dose perturbation. The direct structural composite remains worse after fair calibration. It no longer produces the misleading high-confidence catastrophe observed under the non-refit sensitivity check, but it also does not rescue the model.

## 4. Authorization decision

The final test is not authorized.

```text
confirmatory_test_authorized = false
final_test_generated         = false
final_test_opened            = false
```

The reason is procedural and scientific. The model did not clear the validation thresholds it needed in order to deserve a one-shot confirmatory test. Spending the unopened final test now would convert a negative validation result into an underpowered attempt at rescue.

Any future final-test execution must require a new lock based on a model that has first met a validation-stage criterion. The existing final test remains preserved for that future possibility.

## 5. Negative-result interpretation

This is a constrained result, not a null result.

The four-proxy operationalization contains pre-outcome signal. It modestly improved on transport-only prediction. But it was not strong enough to satisfy the preregistered practical threshold, did not compress the full native dynamics, and did not provide a safety screen.

The most important failure is conceptual. The hard-intersection interpretation failed:

```text
hosted cases failing at least one fitted gate = 92 / 121
nonhosted cases passing all four gates       = 114
```

This rejects a literal reading in which successful hosting is equivalent to all four scalar gates clearing independent thresholds.

## 6. Architecture revision

The next CVT geometry should not treat `B,Q,C,S` as four isolated possessions. The validation result points toward relational routing.

A better exploratory hypothesis is:

```text
A host survives transformation when contact is routed through a viable relational configuration,
not when four independent scores individually exceed thresholds.
```

In this view, capture readiness may not sit symmetrically beside boundary, preserved organization, and restorative reserve. It may be a revealed routing relation:

```text
C = C(B, Q, S, input, current load, history)
```

This would explain why the flexible pairwise candidate contained more signal than the hard gates, and why successful cases could fail one gate while unsuccessful cases could pass all four.

## 7. Authorized next work

The only authorized next work is exploratory:

1. counterexample anatomy for hosted cases with failed gates;
2. counterexample anatomy for nonhosted cases passing all gates;
3. interaction mapping among `B,Q,C,S`, forcing family, load, reserve, and history;
4. revised relational-routing candidate definitions;
5. a fresh development partition before any new confirmatory claim.

The forbidden next work is a final-test run under the failed Stage 3.2 lock.

## 8. Manuscript implication

The Foundations manuscript should eventually report this result plainly:

> In the first bounded regulated-transport simulation, the proposed `B,Q,C,S` measurements contained modest pre-outcome signal but did not support the literal non-compensable hard-gate interpretation. The result motivates a revised relational-routing interpretation of CVT rather than a four-independent-threshold account.

That sentence is stronger than a victory claim because it is disciplined by evidence.
