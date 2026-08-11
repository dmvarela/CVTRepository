# Stage 5.0 Relational-Routing Preregistration

Date: 2026-08-11  
Status: protocol frozen; execution not authorized

## Decision

The regulated-transport program may proceed to a new development cycle only through a prospectively frozen relational-routing design. Stage 5.0 supplies that design. It does not generate data, fit a revised model, reopen the Stage 3 validation set, or access the final test.

The target question is narrower than the original hard-gate claim:

> Do measurements of how a receiving system routes a declared input, observed before the main outcome window, add calibrated predictive value beyond transport-only, additive, and capacity-matched native models?

This is a testable architecture-repair question. It is not a claim that relational routing is already validated, and it does not restore necessity or sufficiency to the rejected measured hard-gate geometry.

## Why this protocol follows from Stage 4

Stage 4.1 found two load-bearing contradiction classes in the already-opened validation evidence: 92 hosted cases with at least one failed gate and 114 nonhosted cases with all four gates passing. Capture-gate failure appeared in 71 of the 92 hosted contradictions; 90 of the 114 all-pass failures missed the transformation target. The native gradient booster improved most strongly on hosted rows, while rare confident nonhosted errors limited its class-level advantage.

Those findings motivate, but may not train, tune, calibrate, select, or validate, the revised architecture. Stage 5 therefore treats `C` as an input-conditioned response rather than a context-free local threshold and separates scheduled forcing, current load, declared history, reserve, damage, integrity, and recovery.

## Evidence firewall

Stage 3 training rows, Stage 3 validation rows, locked validation predictions, and Stage 4 row-level anatomy are forbidden inputs to every Stage 5 fit, tuning, calibration, selection, and validation process. Stage 4 aggregate results may be used only to motivate the frozen questions and retain continuity with previously declared thresholds.

All Stage 5 row identifiers and random seeds use new SHA-256-derived namespaces. Overlap with Stage 3 is forbidden and must be audited before fitting. Outcome-adaptive enrichment is forbidden. The held-out `repeated_pulse` family remains excluded.

The existing final-test generator is preserved unchanged. It is not a source of development examples, schedules, features, or diagnostics.

## Fresh evidence plan

The planned development evidence contains 24,000 new simulations:

| Partition | Rows | Role |
| --- | ---: | --- |
| development fit | 12,000 | candidate fitting and internal training support |
| development tune | 4,000 | hyperparameter choice |
| development calibration | 4,000 | Platt calibration only |
| development selection | 4,000 | single winner selection and gate estimation |

An independent 8,000-row fresh validation partition may be generated only after the candidate, preprocessing, calibration, thresholds, and validation code are locked. It is opened once.

The design retains balanced combinations of `constant`, `pulse`, `ramp`, and `shock_tail` forcing with low, middle, and high scheduled-dose strata. It adds three controlled precontact histories: none, a prior subthreshold exposure, and a prior exposure followed by recovery. History is fixed before the main forcing and must not reproduce reserved final-test blocks.

## Pre-outcome relational measurements

All predictors must be fixed or measurable before the primary outcome window:

1. local state and margins (`B`, `Q`, `S`, free and buffered load, damage, integrity, reserve);
2. the declared input schedule (family, peak, dose, duration, centroid, rise time, tail fraction, recovery horizon);
3. declared precontact history (history class, prior dose, elapsed recovery, precontact recovery fraction);
4. sham-adjusted counterfactual probe responses.

The probes use cloned states and never alter the evaluated trajectory. They cross two timing states with two doses and measure productive uptake, rejection, buffering, damage, integrity, and recovery responses. Before any outcome is inspected, those four probe cells are reduced to eight frozen level, dose-slope, and timing-contrast summaries. Together with the reference-coded state, schedule, and history terms, the relational input has exactly 31 encoded columns. Probe invalidity above one percent stops the affected partition.

Post-outcome routing totals remain legitimate descriptive or secondary outcomes. They are never predictors of the primary outcome.

## Candidate and baseline comparison

The registered candidate set contains:

- an additive relational logistic model;
- a hierarchical logistic model adding exactly 12 declared interactions;
- a shallow relational gradient booster using the same pre-outcome input budget.

The interactions cross probe response with dose, peak, duration, load, damage, integrity, and recovery; they also cross local margins with forcing family and declared history. No interaction mining is permitted after validation opens.

The comparison includes prevalence and transport-only references, a capacity-matched native logistic model, a capacity-matched native gradient booster, and the full native gradient booster used as a separate performance ceiling. Capacity matching requires identical row access, preprocessing, tuning opportunities, input-column caps, and coefficient or tree-complexity caps. The relational design uses 31 encoded input columns under a cap of 32 and 48 fitted terms. The matched native design also freezes 31 columns: 15 native parameters, six initial-state variables, three forcing-family contrasts, three schedule variables, and four history variables.

This distinction matters. A relational candidate must not receive credit merely because it is more flexible than the comparison model.

## Outcomes and analysis

`hosted` remains the primary binary outcome and retains the independent host declaration, target attainment, damage, and integrity requirements. Target non-attainment, damage violation, and integrity violation are analyzed as separate binary endpoints rather than forced into a single mutually exclusive reason.

Productive uptake, rejected exchange, buffering, damage accumulation, integrity loss, and recovery are separate secondary routing responses. They can show *how* a case fails without leaking post-outcome information into prediction.

Brier score remains primary. Secondary metrics are log loss, average precision, AUROC, calibration intercept and slope, and ten-bin equal-count expected calibration error. Paired uncertainty uses 2,000 bootstrap resamples stratified by outcome and forcing family.

## Selection and authorization rules

Hyperparameters are chosen on the tune partition, Platt calibration is fitted only on the calibration partition, and a single winner is chosen on the selection partition. A Brier difference of at most 0.002 is a tie; ties prefer lower capacity, stronger regularization, and simpler structure. No refit is permitted after winner selection.

Final-test authorization requires every fresh-validation gate:

- at least 0.005 absolute and 2% relative Brier improvement over transport-only, with a paired 95% interval excluding zero;
- at least 0.005 absolute Brier improvement over the additive relational ablation, with a paired 95% interval excluding zero;
- at least 0.002 absolute Brier improvement over the matched native model, with a paired 95% interval excluding zero;
- no more than 0.005 Brier disadvantage to the full native gradient booster, a 95% upper disadvantage no greater than 0.01, and no more than one-third of its feature count;
- calibration slope from 0.8 to 1.2, intercept from -0.1 to 0.1, and equal-count ECE no greater than 0.05;
- no forcing family worse than transport-only by more than 0.01 Brier, with at least 1,500 rows per family;
- all numerical-integrity and minimum-event rules satisfied.

The 0.005 incremental threshold and one-third compression threshold are retained from Stage 3. They are not relaxed after observing the negative result.

If an event-count or integrity rule fails, the program stops without outcome-dependent resampling and without opening the final test. Any amendment applies only to new fresh evidence. If any fresh-validation authorization gate fails, the revised confirmatory claim stops and the final test remains sealed.

## Reproducibility and current status

The machine-readable protocol is `validation/regulated-transport/config/stage5_relational_routing_protocol.json`. The audit module and focused tests enforce the evidence firewall, partition independence, pre-outcome boundary, capacity matching, frozen thresholds, stopping rules, and claims boundary.

The audit passes 12 invariants and eight focused tests pass. This is a protocol result only:

```text
stage5_data_generation_authorized       = false
stage5_candidate_fitting_authorized     = false
stage5_validation_generation_authorized = false
stage5_validation_opening_authorized    = false
confirmatory_final_test_authorized      = false
final_test_generated                    = false
final_test_opened                       = false
```

The next permissible action is a separate Stage 5.1 implementation-and-integrity review of the fresh development generator. That review must verify the generator, seed and row nonoverlap, feature timing, probe isolation, solver integrity, and balance tables before any candidate is fitted.

