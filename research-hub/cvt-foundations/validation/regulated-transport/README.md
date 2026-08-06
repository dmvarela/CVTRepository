# Regulated-Transport Validation Package

This package implements the native two-compartment transport model, pre-outcome measurements, frozen development evidence, and the locked Stage 3.2 validation comparison for the CVT Foundations validation protocol.

Current completed scope:

- Stage 1 native equations, forcing schedules, accounting, and smoke runs;
- Stage 1.5 cross-solver and randomized numerical verification;
- Stage 2 candidate `B,Q,C,S` proxy construction;
- Stage 2.5 sham-adjusted micro-probe qualification;
- Stage 3 pre-fit model-comparison preregistration;
- Stage 3.1 deterministic training/validation generation and integrity review;
- Stage 3.2 fit/calibration/validation comparison under the frozen rules.

Still excluded:

- generation or use of the untouched final test partition;
- post-validation alteration of the locked primary winners;
- claims of empirical or general CVT validation.

The frozen Stage 3 design is recorded in:

```text
reviews/2026-08-04-stage3-model-comparison-preregistration.md
validation/regulated-transport/config/stage3_model_comparison.json
```

The Stage 3.1 generation design and review are recorded in:

```text
validation/regulated-transport/config/stage31_design.json
reviews/2026-08-04-stage3-1-data-integrity-report.md
validation/regulated-transport/results/stage3_1/
```

The Stage 3.2 comparison and locked results are recorded in:

```text
reviews/2026-08-05-stage3-2-validation-model-comparison.md
validation/regulated-transport/config/stage32_portable_seal.json
validation/regulated-transport/results/stage3_2/
```

Run tests:

```bash
python -m pytest -q
```

Run smoke report:

```bash
python -m src.smoke --output results/smoke_summary.csv
```

Run Stage 1.5 verification:

```bash
python -m src.verify_stage15
```

Run the Stage 2 proxy audit:

```bash
python -m src.proxy_verify
```

Run the Stage 2.5 micro-probe qualification:

```bash
python -m src.probe_qualify --output results/stage2_5
```

Generate Stage 3.1 development evidence:

```bash
python -m src.stage31_dataset --output results/stage3_1 --workers 1
```

Run the Stage 3.2 comparison from the frozen Stage 3.1 artifact:

```bash
python -m src.stage32_runner \
  --data results/stage3_1 \
  --output results/stage3_2 \
  --seal config/stage32_portable_seal.json \
  --bootstrap-resamples 2000
python -m src.stage32_finalize --output results/stage3_2
```

Stage 3.2 locked `CVT-2-minimum` as the primary CVT candidate and `BL-6-full-native-gradient-boosting` as the primary baseline. The current four-proxy operationalization did not meet the preregistered thresholds for incremental predictive value, predictive compression, or high-confidence safety-screen utility.

The final test remains ungenerated and unopened. The next bounded action is Stage 3.2.5: materialize reproducible locked scorers, correctly refit the prespecified capture-proxy sensitivity alternatives on training/calibration data only, audit the unopened final-test generator, and decide whether to authorize the single confirmatory run.
