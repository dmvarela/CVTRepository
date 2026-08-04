# CVT Regulated-Transport Validation — Stage 3.1 Development-Data Integrity Report

**Date:** 2026-08-04  
**Status:** training and validation evidence generated; no candidate model fitted  
**Final test partition:** not generated and unopened  
**Parent artifact:** Stage 3 model-comparison preregistration

## 1. Scope

Stage 3.1 generated only the preregistered training and validation partitions, computed the frozen pre-outcome measurements and native outcomes, and reviewed numerical, measurement, balance, and partition integrity before any model fitting.

The generator has no Stage 3.1 code path for the final test partition. A request to generate `test` raises an error. No CVT candidate, baseline, calibration model, or validation-based selector was fitted.

## 2. Evidence generated

```text
training rows    = 12,000
validation rows  =  4,000
fit rows         =  9,000
calibration rows =  3,000
```

Training and validation were generated from independent Latin-hypercube designs with fixed partition seeds. Forcing family and forcing stratum were balanced jointly across twelve cells.

The large deterministic CSV evidence files are not committed to Git because of size. Their file, design-hash, and row-digest SHA-256 values are preserved in committed manifests:

```text
training.csv SHA-256   = 31a23de52adf5914929c5c56f3dd7ff6ded03ac9daf42e96f9269006371b512b
validation.csv SHA-256 = b2b70e5bb8624ee5300c37d8750ace3b63e3cb5e3f727c15f6abc164da38467f
```

## 3. Integrity results

```text
solver success                = 100.000%
accounting validity           = 100.000%
hard-bound validity           = 100.000%
productive-pool monotonicity  = 100.000%
training/validation overlap   = 0
```

The maximum conservation residual used `57.867%` of its allowed tolerance. Bounded accounting refinement was required for `0.0625%` of runs. Numerical solver retry was required for `0%` of runs.

The preregistered 1% cross-solver audits found:

```text
training audited rows             = 120
training maximum terminal delta   = 2.169e-06
training hosted mismatches        = 0
validation audited rows           = 40
validation maximum terminal delta = 5.278e-07
validation hosted mismatches      = 0
```

## 4. Probe validity

```text
primary invalid — training       = 0.000%
primary invalid — validation     = 0.000%
sensitivity invalid — training   = 0.000%
sensitivity invalid — validation = 0.000%
```

The 1% measurement stop rule was not triggered.

Primary and 2.5×-dose capture probes were evaluated with one shared zero-input sham in a combined augmented integration. This preserves the Stage 2.5 causal subtraction while reducing duplicate numerical work.

## 5. Outcome balance

```text
hosted prevalence — training   = 3.175%
hosted prevalence — validation = 3.025%
minority count — training      = 381
minority count — validation    = 121
```

The preregistered minimum class-count conditions were satisfied. Outcome imbalance remains substantial and must be handled through the frozen stratification, calibration, and probability metrics rather than by changing the data after inspection.

One cell—low-forcing short pulses—contained no hosted cases in either development partition. This is preserved as a property of the generated native system, not repaired by resampling. The preregistered fitting stratification is by hosted outcome and forcing family, not by family-by-stratum cell.

## 6. Repairs made before model fitting

### 6.1 Joint rather than marginal balance

An early quick generator balanced forcing family and forcing stratum separately. That does not guarantee balance in their joint cells. The production generator now assigns the twelve family-by-stratum combinations directly before shuffling. This repair was made before the full evidence was generated.

### 6.2 Bounded accounting refinement

One low-dose quick run produced a whole-window quadrature residual just above the frozen tolerance even though the native trajectory was stable. Reintegrating the same rate functions across bounded subintervals and every forcing breakpoint closed the identity. The production accounting layer therefore retains the fast whole-window pass but automatically performs a stricter bounded refinement when needed. It does not change the native equations or outcome.

### 6.3 Checkpointed generation

Rows were generated in deterministic 500-row chunks. Completed chunks are resumable and reassembled in partition order. This prevents a partial long run from being silently replaced, skipped, or regenerated under changed settings.

## 7. Decision

```text
fitting_ready = true
```

Stage 3.1 authorizes Stage 3.2. Stage 3.2 may fit and calibrate the preregistered candidates using training data and then open validation exactly once under the frozen rules. It may not generate or inspect the final test partition.

## 8. Epistemic boundary

These files are simulated development evidence, not empirical membrane observations and not validation of CVT in other domains. The result of Stage 3.1 is narrower:

> the preregistered model contest now has a deterministic, auditable training-and-validation evidence base that passed its declared integrity gates before interpretation began.
