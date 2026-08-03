# Regulated-Transport Native Model — Stage 1

This package implements only the native two-compartment transport model frozen in the CVT Foundations simulation specification.

Stage 1 scope:
- native equations and forcing schedules;
- auditable mass accounting;
- numerical bounds and solver diagnostics;
- smoke scenarios and stability checks.

Excluded:
- CVT gate calculation;
- aggregation or predictive-model fitting;
- claims about CVT validation.

Run tests:

```bash
python -m pytest -q
```

Run smoke report:

```bash
python -m src.smoke --output results/smoke_summary.csv
```
