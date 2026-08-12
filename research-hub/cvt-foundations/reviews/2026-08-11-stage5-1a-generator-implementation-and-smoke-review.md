# Stage 5.1A Fresh-Generator Implementation and Smoke Review

Date: 2026-08-11  
Status: complete; Stage 5.1B development generation authorized

## Decision

Stage 5.1A implements the fresh Stage 5 generator contract and passes its bounded pre-generation review. The implementation may proceed to Stage 5.1B generation of the four fresh development partitions, totaling 24,000 rows.

This decision does not authorize candidate fitting, tuning, calibration, selection, fresh-validation generation or opening, or any final-test action.

## Implemented boundary

The Stage 5.1A entry point is structurally unable to generate a full partition. It requires an explicit --smoke flag, accepts only development_fit, and rejects more than 12 rows. It has no Stage 3 row-input argument and no fresh-validation or final-test path.

The implementation freezes:

- SHA-256-derived 64-bit seeds and s5- row identities for each independent partition namespace;
- a 36-cell family-by-stratum-by-history cycle with balanced 12-row smoke marginals;
- four nonreserved forcing families and explicit exclusion of repeated_pulse;
- three history classes: none, subthreshold prior exposure, and prior exposure followed by recovery;
- clone-only sham-adjusted probes at two receiving states, two doses, and two readout horizons;
- eight prespecified probe levels, dose slopes, and timing/recovery contrasts;
- exactly 31 encoded relational inputs and 31 capacity-matched native inputs;
- manifests, hashes, feature contracts, integrity rules, and authorization flags.

Stage 3 row-level evidence is neither loaded nor queried. Only the frozen Stage 5.0 protocol and native simulator source are inputs.

## Time-grid defect found and repaired

The first 12-row smoke stopped on a sampled history whose exposure-plus-recovery window was not an exact multiple of a fixed output step. The existing native wrapper constructs its requested grid by stepping to the terminal time; for that sampled window, floating-point stepping requested one value just beyond the integration span.

Stage 5.1A now derives the history output interval from the sampled total window, producing exactly 200 intervals. A recovered-history regression test exercises the previously failing path. The focused suite increased from 11 to 12 tests and passes.

No real development partition existed when the defect was found, so no evidence was discarded, regenerated, or selected by outcome.

## Bounded smoke result

The authorized smoke contains 12 synthetic development-design cases:

| Check | Result |
| --- | ---: |
| unique row IDs | 12 / 12 |
| unique design hashes | 12 / 12 |
| each forcing family | 3 |
| each forcing stratum | 4 |
| each history class | 4 |
| history solver success | 1.0 |
| main solver success | 1.0 |
| accounting valid | 1.0 |
| bounds valid | 1.0 |
| finite relational features | 1.0 |
| finite native features | 1.0 |
| probe measurements | 96 |
| invalid probes | 0 |
| maximum probe/main state difference | 0.0 |
| maximum accounting residual/tolerance | 0.07578255225952624 |

The smoke records hashes and integrity summaries only. It does not commit row-level simulated trajectories or use primary outcomes for enrichment, selection, or claims.

## Reproducibility

Run the focused suite from validation/regulated-transport:

~~~bash
python -m unittest discover -s tests -p 'test_stage51a_generator.py' -v
~~~

Run the bounded smoke:

~~~bash
python -m src.stage51a_generator \
  --protocol config/stage5_relational_routing_protocol.json \
  --config config/stage51a_generator_implementation.json \
  --output results/stage5_1a \
  --smoke \
  --rows 12
~~~

The focused suite passes 13 tests, including a canonical-protocol-seal regression. The bounded smoke passes every frozen integrity rule.

## Authorization

~~~text
stage5_1b_full_development_generation_authorized = true
maximum_stage5_1b_rows                           = 24000
candidate_model_fitting_authorized               = false
fresh_validation_generation_authorized           = false
fresh_validation_opening_authorized              = false
confirmatory_final_test_authorized                = false
final_test_generated                              = false
final_test_opened                                 = false
~~~

Stage 5.1B must generate only the four development partitions under their frozen namespaces, commit manifests rather than large row-level CSVs, and stop if any integrity, balance, probe, solver, accounting, bounds, or nonoverlap rule fails. It may not fit a candidate.

