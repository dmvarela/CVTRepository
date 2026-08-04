# Regulated-Transport Validation Package

This package implements the native two-compartment transport model and the pre-outcome measurement work frozen by the CVT Foundations validation protocol.

Current completed scope:

- Stage 1 native equations, forcing schedules, accounting, and smoke runs;
- Stage 1.5 cross-solver and randomized numerical verification;
- Stage 2 candidate `B,Q,C,S` proxy construction;
- Stage 2.5 sham-adjusted micro-probe qualification;
- Stage 3 pre-fit model-comparison preregistration.

Still excluded:

- generation of the full training, validation, and unopened test partitions;
- final aggregator fitting;
- validation-based model selection;
- use of the untouched test partition;
- claims of empirical or general CVT validation.

The frozen Stage 3 design is recorded in:

```text
reviews/2026-08-04-stage3-model-comparison-preregistration.md
validation/regulated-transport/config/stage3_model_comparison.json
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
python -m src.verify_stage1_5 --output results/stage1_5
```

Run the Stage 2 proxy audit:

```bash
python -m src.proxy_verify
```

Run the Stage 2.5 micro-probe qualification:

```bash
python -m src.probe_qualify --output results/stage2_5
```

Use `--quick` for a small implementation smoke check. The full Stage 2.5 run uses development data only and does not open the final test partition.

The next implementation stage is Stage 3.1 dataset generation and integrity review. It must generate training and validation data first, preserve the final test partition unopened, and fit no candidate model until dataset manifests and checksums pass review.
