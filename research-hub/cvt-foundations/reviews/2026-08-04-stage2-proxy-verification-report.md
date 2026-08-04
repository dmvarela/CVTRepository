# Stage 2 Proxy Verification Report

**Date:** 2026-08-04  
**Scope:** pre-outcome construction and redundancy testing for candidate `B,Q,C,S` measurements.  
**Excluded:** final aggregator fitting, predictive model comparison, and use of the untouched test partition.

## Implementation

The branch adds:

- a two-sided scheduled-forcing proxy for bounded coupling `B`;
- initial integrity `Q(0)` as the organization proxy;
- initial reserve fraction `S(0)/S_max` as the reserve proxy;
- two candidate capture-readiness measurements:
  1. a direct geometric mean of productive-capacity headroom, integrity, and reserve response;
  2. a fixed low-amplitude micro-probe whose productive response is measured in a separate simulation and whose state is then discarded.

The micro-probe therefore does not alter the evaluated run. No realized target, viability label, delayed outcome, or final trajectory enters proxy construction.

## Development-only audit

A deterministic development sample of 300 initial states and forcing schedules was generated with seed `20260804`. The untouched test partition was not opened.

All proxies remained in `[0,1]`, and construction was deterministic. Pairwise Spearman correlations and variance inflation factors were computed only to diagnose duplication; they were not used to fit a final model.

### Results

- maximum absolute pairwise Spearman correlation: `0.654`;
- no proxy pair reached the preregistered near-duplicate flag of `|rho| >= 0.90`;
- maximum variance inflation factor: `2.82`;
- direct-versus-probe capture Spearman correlation: `0.108`.

The direct capture proxy correlated with `Q` at `0.654` and with `S` at `0.459`. This is expected because it algebraically contains both quantities. Its acceptable VIF does not remove the conceptual duplication.

The micro-probe capture measure had much lower overlap with `Q` and `S`, but it also agreed only weakly with the direct proxy. The two measurements therefore cannot be treated as interchangeable versions of one established construct.

## Revision decision

The direct geometric-mean proxy is retained as a documented **derived composite** for sensitivity analysis, but it should not serve as the primary independent `C` gate in the four-gate comparison. Doing so would partially count `Q` and `S` twice.

The micro-probe remains the leading candidate for primary capture readiness because it is pre-outcome, state-sensitive, and does not algebraically reuse the other gates. However, its low agreement with the direct proxy creates a new evidentiary burden: Stage 2.5 must test probe amplitude, duration, delivered-load floor, repeatability, and whether the probe predicts a domain-native short-horizon capture response without becoming a disguised miniature outcome trial.

## Methodological interpretation

The result supports the manuscript's warning that normalization and aggregation cannot substitute for construct definition. Composite-indicator guidance requires explicit treatment of normalization, weighting, redundancy, and sensitivity, while transparent prediction-model reporting requires predictor definitions and validation partitions to be fixed and disclosed. These principles are used here as methodological safeguards, not as evidence for CVT.

## Next bounded action

Perform **Stage 2.5 micro-probe qualification** before fitting any aggregator:

1. sweep probe amplitude and duration on development data only;
2. require a minimum delivered-load floor and quantify numerical stability;
3. test repeated-probe reliability from identical initial states;
4. test monotonic response to isolated changes in productive headroom, integrity, and reserve;
5. compare probe response with a separately declared short-horizon capture-capacity criterion;
6. freeze one primary probe specification and one sensitivity alternative;
7. keep the untouched test partition closed.

Only after the probe is qualified should the project proceed to preregistered training/validation comparison among direct constraints, product, minimum, geometric mean, soft minimum, and domain-native baselines.
