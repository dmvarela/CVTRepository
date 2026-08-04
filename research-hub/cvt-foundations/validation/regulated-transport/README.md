# Regulated-Transport Validation Package

This package implements the native two-compartment transport model, pre-outcome measurements, and the frozen development evidence for the CVT Foundations validation protocol.

Current completed scope:

- Stage 1 native equations, forcing schedules, accounting, and smoke runs;
- Stage 1.5 cross-solver and randomized numerical verification;
- Stage 2 candidate `B,Q,C,S` proxy construction;
- Stage 2.5 sham-adjusted micro-probe qualification;
- Stage 3 pre-fit model-comparison preregistration;
- Stage 3.1 deterministic training/validation generation and integrity review.

Still excluded:

- fitting or calibrating any candidate model;
- validation-based model selection;
- generation or use of the untouched final test partition;
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

Use `--quick` for a small implementation check. The Stage 3.1 generator accepts only `training` and `validation`; the final test partition is inaccessible in this stage. Full deterministic CSVs are ignored by Git, while their SHA-256 manifests and integrity summaries are committed.

Stage 3.1 ended with `fitting_ready = true`. The next bounded action is Stage 3.2: fit and calibrate the preregistered candidates on training data, then open validation once under the frozen selection rules. The final test remains unopened.
