# Stage 1.5 Numerical and Adversarial Verification

**Date:** 2026-08-04  
**Scope:** native regulated-transport model only; no CVT gates, aggregators, or predictive comparison.

## Result

The native simulator passed the Stage 1.5 numerical verification after one accounting repair.

### Cross-solver agreement

Six representative scenarios were run with both LSODA and BDF. All twelve runs passed accounting. The largest scaled trajectory difference was `2.16e-6`; the largest scaled terminal-state difference was `4.83e-7`. These values are well below the preregistered review thresholds of `1e-4` and `1e-5`.

Projection-heavy runs showed different raw projection counts across solvers, but nearly identical state trajectories. Projection count is therefore retained as a solver-evaluation diagnostic, not interpreted as a physical quantity.

### Randomized property verification

Using seed `20260804`, 120 parameter/initial-state/forcing combinations were sampled across constant, pulse, repeated-pulse, ramp, and shock-tail families.

- successful integrations: 120/120;
- accounting closure: 120/120;
- hard-bound validity: 120/120;
- monotone cumulative productive uptake: 120/120;
- largest accounting residual as a fraction of tolerance: `0.234`;
- runs with at least one projection: 15/120;
- runs with more than 500 projection interventions: 11/120.

## Accounting defect found and repaired

The first randomized pass exposed two pulse-family runs that failed conservation despite passing all trajectory checks. Their forcing durations did not coincide with the intervention endpoint supplied to adaptive quadrature. Accounting therefore crossed unreported discontinuities.

The forcing schedules now expose their exact breakpoints, and channel accounting supplies every breakpoint to adaptive quadrature. After the repair, all 120 randomized runs passed the frozen accounting tolerance.

This is a numerical-accounting repair only. It does not alter the state equations, outcome definition, or any CVT claim.

## Projection-heavy trajectories

Hard-bound interventions occur primarily when damage reaches its upper bound. Cross-solver state agreement indicates that these trajectories are numerically reproducible, but the raw projection count depends on solver evaluation patterns. Accordingly:

1. projection count remains visible but is not treated as a physical outcome;
2. later reporting should add sampled time-at-bound and first-bound-contact measures;
3. projection-heavy cases must remain in adversarial and sensitivity sets;
4. no gate may use projection count as an input.

The current tangent-cone implementation is acceptable for proceeding to proxy verification, but an explicit bounded reparameterization remains a later sensitivity option.

## Frozen artifacts

- `parameters.csv` records the Stage 1.5 ranges and defaults;
- `scenarios.csv` records the representative solver-comparison cases;
- `src/verify_stage15.py` reproduces cross-solver and randomized checks;
- `tests/test_stage15.py` adds discontinuity-accounting, solver-agreement, and randomized property tests;
- `results/stage15/` preserves the verification outputs.

## Decision

The native system is numerically stable and auditable enough to proceed to **Stage 2: proxy verification**.

Stage 2 may construct candidate measurements for `B,Q,C,S`, including the micro-probe capture-readiness alternative, but must not yet fit final aggregators or inspect the untouched final test set.
