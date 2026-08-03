# Stage 1 Native Model Implementation Report

**Date:** 2026-08-03  
**Scope:** native equations, accounting, bounds, forcing schedules, smoke runs, and numerical checks only.  
**Excluded:** CVT gate construction, aggregators, predictive comparison, or validation claims.

## Implementation

The package implements the frozen six-state host:

```text
[c_A, P, U, D, S, Q]
```

with fixed run-level history `H`, prescribed source/permeability schedules, productive capture, buffering, safe rejection, damage, reserve consumption/replenishment, and integrity loss/recovery.

Hard bounds are enforced through tangent-cone derivative guards and reported projection counts. The primary implementation uses `scipy.integrate.solve_ivp` with `LSODA`, `rtol=1e-7`, and `atol=1e-9`.

## Accounting failure discovered during implementation

The first implementation integrated `J_raw` and `J_reject` from the sampled output grid using the trapezoid rule. A constant-forcing run produced an accounting residual of approximately `1.6504e-2` against a frozen tolerance of approximately `2.6767e-5`.

The trajectories appeared plausible, but the run was invalid under the preregistered accounting rule.

The accounting layer was therefore changed to integrate channel rates against the solver's dense solution using adaptive quadrature, with the intervention discontinuity supplied explicitly. After this repair, smoke-run residuals were approximately `1e-7` to `3e-6`, all within tolerance.

This repair changes numerical accounting only; it does not change the native state equations or CVT claims.

## Tests

Six tests pass:

1. zero forcing preserves transported mass and produces no productive growth;
2. mass accounting closes under forcing;
3. all hard-bounded states remain within bounds;
4. cumulative productive uptake is monotone;
5. deterministic runs reproduce exactly;
6. output-grid refinement leaves terminal states stable.

Local result:

```text
6 passed
```

## Smoke scenarios

Ten smoke scenarios were run: zero forcing; low, moderate, and high constant forcing; short pulse; repeated pulse; ramp; shock plus tail; high forcing without the direct-flux damage term; and high forcing without integrity modulation of raw flux.

All integrations succeeded and all accounting checks passed.

The smoke runs already generate multiple failure modes: insufficient uptake, target-reaching but nonviable runs, integrity collapse, damage saturation, and sensitivity to alternative native mechanisms. These are diagnostics only, not validation results.

## Important implementation observation

Some severe scenarios require many bound interventions because damage reaches its hard upper bound. Projection frequency is preserved in output rather than hidden. Before large scenario generation, Stage 1.5 should inspect whether the projected system or an explicit bounded reparameterization is preferable.

## Next bounded action

Review and merge this Stage 1 package. After merge, perform Stage 1.5 numerical/adversarial verification before any gate fitting:

- compare `LSODA` with `BDF` on a stratified subset;
- examine projection-heavy trajectories;
- verify accounting across all forcing families and parameter corners;
- add randomized property tests;
- create the frozen parameter and scenario tables;
- do not compute `B,Q,C,S` yet.
