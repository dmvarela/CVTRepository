# Regulated-Transport Validation Package

This package implements the native two-compartment transport model and the pre-outcome measurement work frozen by the CVT Foundations validation protocol.

Current completed scope:

- Stage 1 native equations, forcing schedules, accounting, and smoke runs;
- Stage 1.5 cross-solver and randomized numerical verification;
- Stage 2 candidate `B,Q,C,S` proxy construction;
- Stage 2.5 sham-adjusted micro-probe qualification.

Still excluded:

- final aggregator fitting;
- comparison against domain-native predictive baselines;
- use of the untouched test partition;
- claims of empirical or general CVT validation.

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
