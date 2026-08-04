# CVT Regulated-Transport Validation — Stage 2.5 Micro-Probe Qualification

**Date:** 2026-08-04  
**Status:** development-only measurement qualification; not predictive validation  
**Parent artifacts:** Stage 2 proxy verification and the frozen regulated-transport protocol  
**Test partition:** unopened

## 1. Question

Can a low-amplitude perturbation provide a reproducible, local, pre-outcome measurement of the host's capacity to route newly delivered load into productive uptake?

The qualification criteria were:

1. the probe must not reuse the evaluated run's outcome;
2. delivered probe load must exceed a fixed numerical floor;
3. the response must be small relative to host capacities;
4. rankings should be stable under a moderate dose change;
5. the measurement should respond monotonically to independently varied productive headroom, integrity, and reserve in the frozen native model;
6. deterministic repeats, solver changes, and tighter tolerances should not materially alter the value;
7. amplitude, pulse duration, and readout horizon must be fixed before aggregator fitting.

## 2. Defect in the Stage 2 probe

The Stage 2 probe used

```text
productive uptake during probe / delivered probe load
```

from the actual initial state. This numerator included productive conversion of free and buffered material already present before the probe arrived.

Across 300 development cases under the selected low-dose specification:

- the unadjusted ratio exceeded `1` in `99.33%` of cases;
- its median was `13.86`;
- the implementation clipped the result to `[0,1]`.

The clipped quantity therefore appeared bounded while concealing that it was not an attributable capture fraction. The Stage 2 `g_c_probe` values must not be used in later model comparison.

This is a measurement repair, not a revision made after seeing predictive performance. No outcome model has yet been fitted and the untouched test partition remains closed.

## 3. Paired sham repair

The repaired probe uses two discarded simulations from the identical initial state:

1. a small pulse run;
2. a zero-input sham run over the same readout horizon.

Define

```text
Delta P_marginal
= Delta P_probe - Delta P_sham
```

and

```text
C_probe
= Delta P_marginal / M_delivered_probe.
```

The sham subtraction removes productive conversion that would have occurred without the probe. The evaluated run is then started from the original unchanged state; neither probe trajectory is carried forward.

A measurement is invalid rather than assigned zero when

```text
M_delivered_probe < 1e-4 * P_cap.
```

This prevents insufficient numerical signal from being interpreted as absent capture readiness.

## 4. Candidate sweep

Twelve candidates were examined on 50 seeded development cases:

- source concentration `c_B = 2.0`;
- permeability in `{0.05, 0.10, 0.25}`;
- pulse duration in `{0.05, 0.10}`;
- readout horizon in `{0.5, 1.0}`.

All candidates passed the delivered-load floor in this development subset. For a fixed pulse duration and readout horizon, changing permeability produced nearly identical marginal-response distributions. This supports operation in a local dose regime.

The readout horizon was not ignorable. Comparing `0.5` with `1.0` time unit gave:

```text
Spearman rho = 0.9770
median C_probe(1.0) / C_probe(0.5) = 1.5990.
```

Rankings were similar, but magnitudes changed because delivered material continued to be routed after the pulse ended. The readout horizon is therefore part of the measurement definition, not a numerical nuisance.

## 5. Frozen probe specifications

### Primary probe

```text
c_B = 2.0
permeability = 0.10
pulse duration = 0.05
readout horizon = 1.0
delivered floor = 1e-4 * P_cap
```

### Sensitivity probe

```text
c_B = 2.0
permeability = 0.25
pulse duration = 0.05
readout horizon = 1.0
delivered floor = 1e-4 * P_cap
```

The sensitivity probe delivers approximately `2.5x` the primary dose while remaining small relative to productive capacity.

## 6. Development qualification results

On 300 seeded development cases:

- primary valid fraction: `1.000`;
- sensitivity valid fraction: `1.000`;
- smallest primary delivered-load margin over the floor: `2.04x`;
- primary versus sensitivity rank agreement: `rho = 0.9999987`;
- maximum absolute score difference: `5.63e-5`;
- no sham-adjusted ratio was negative or above `1`.

For the primary probe:

```text
median marginal response = 0.14244
interquartile range      = 0.08266
95th percentile dose     = 0.001198 * P_cap
```

The 95th-percentile incremental state differences between probe and sham were:

```text
productive pool / P_cap  = 2.79e-4
damage                    = 4.59e-5
reserve / S_max           = 3.89e-5
integrity                  = 1.65e-6.
```

The selected probe is therefore local relative to the declared host scales in this development sample.

## 7. Directional response tests

Thirty additional development cases were subjected to isolated six-level sweeps.

The primary marginal response was strictly increasing in every case when independently increasing:

- initial integrity `Q(0)`;
- current reserve `S(0)`;
- productive capacity headroom.

This confirms internal directional consistency with the frozen native equations. It does not independently prove that these relationships hold in another domain, because the native model itself contains these mechanisms.

Two descriptive findings clarify what the probe measures:

- increasing pre-existing free internal load generally reduced marginal response;
- increasing initial buffered load generally increased marginal response.

The probe is therefore not a pure static binding-capacity measure. It is a **local marginal routing response** of the whole current host state, including congestion and buffered material.

## 8. Numerical repeatability

Across 20 development cases:

```text
exact repeat maximum difference       = 0
LSODA versus BDF maximum difference   = 6.60e-6
tighter-tolerance maximum difference  = 1.46e-6.
```

These differences are small relative to the observed score range.

## 9. Measurement decision

The primary Stage 2 capture proxy is replaced by the sham-adjusted marginal probe.

The old unadjusted ratio is retained only as an audit field named `probe_raw_ratio`; it is not a candidate gate and must not be clipped into apparent validity.

The direct structural composite remains a sensitivity measurement only because it algebraically reuses `Q` and `S`.

For this simulation, the operational meaning of `C` is now:

> the host's pre-outcome marginal productive response per unit of a frozen, low-dose delivered perturbation, measured relative to a zero-input sham over a fixed readout horizon.

This is narrower and more defensible than claiming to have measured a universal latent property called capture readiness.

## 10. Limits

- Sham subtraction removes baseline conversion but cannot label individual transported units as a tracer would.
- Nonlinear perturbation could, in principle, mobilize pre-existing load; dose invariance reduces but does not eliminate this concern.
- The strong monotonicity results partly reflect the chosen native equations.
- The readout horizon materially affects scale and must remain frozen.
- Qualification occurred only on development simulations, not empirical membrane data.
- No predictive aggregator has been fitted and no test outcome has been examined.

## 11. Next bounded action

Freeze the corrected development dataset and perform **Stage 3 preregistered model-comparison design** before fitting:

- declare the exact training and validation feature sets;
- declare the CVT candidates and domain-native baselines;
- define normalization and threshold fitting using training data only;
- define validation-only model selection;
- define performance, calibration, complexity, and false-safe criteria;
- preserve the final test partition unopened.

The next artifact should be a model-comparison preregistration, not model results.
