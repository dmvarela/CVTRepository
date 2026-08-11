# Regulated-Transport Validation Package

This package implements the native two-compartment transport model, pre-outcome measurements, frozen development evidence, the locked Stage 3.2 validation comparison, the Stage 3.2.5 closure decision, the Stage 4 counterexample and architecture cycle, and the frozen Stage 5.0 relational-routing protocol for the CVT Foundations validation program.

Current completed scope:

- Stage 1 native equations, forcing schedules, accounting, and smoke runs;
- Stage 1.5 cross-solver and randomized numerical verification;
- Stage 2 candidate `B,Q,C,S` proxy construction;
- Stage 2.5 sham-adjusted micro-probe qualification;
- Stage 3 pre-fit model-comparison preregistration;
- Stage 3.1 deterministic training/validation generation and integrity review;
- Stage 3.2 fit/calibration/validation comparison under the frozen rules;
- Stage 3.2.5 fair capture-proxy sensitivity refit and final-test non-authorization;
- Stage 4.0 exploratory protocol for counterexample anatomy and relational-routing revision;
- Stage 4.1 deterministic counterexample anatomy, model-error comparison, and relational-routing hypotheses;
- Stage 4.2 architecture decision and canonical-manuscript revision plan;
- Stage 4.3 canonical-manuscript revision and verified build;
- Stage 5.0 frozen relational-routing preregistration and protocol audit.

Still excluded:

- Stage 5 fresh-data generation or revised-model fitting;
- generation or use of the untouched final test partition;
- post-validation alteration of the locked primary winners;
- claims of empirical or general CVT validation;
- confirmatory use of Stage 4 exploratory findings.

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

The Stage 3.2 comparison and locked results are recorded in:

```text
reviews/2026-08-05-stage3-2-validation-model-comparison.md
validation/regulated-transport/config/stage32_portable_seal.json
validation/regulated-transport/results/stage3_2/
```

The Stage 3.2.5 closure decision is recorded in:

```text
reviews/2026-08-06-stage3-2-5-closure-and-architecture-memo.md
validation/regulated-transport/results/stage3_2_5/
```

The Stage 4.0 counterexample-anatomy protocol is recorded in:

```text
reviews/2026-08-06-stage4-counterexample-anatomy-protocol.md
validation/regulated-transport/config/stage4_counterexample_anatomy.json
validation/regulated-transport/results/stage4_0/
```

The executed Stage 4.1 anatomy is recorded in:

```text
reviews/2026-08-06-stage4-1-counterexample-anatomy.md
validation/regulated-transport/results/stage4_1/
validation/regulated-transport/src/stage41_counterexample_anatomy.py
```

The Stage 4.2 architecture decision is recorded in:

```text
reviews/2026-08-10-stage4-2-architecture-decision.md
reviews/2026-08-10-stage4-2-manuscript-revision-plan.md
validation/regulated-transport/results/stage4_2/
```

The Stage 4.3 manuscript revision and verified build are recorded in:

```text
reviews/2026-08-11-stage4-3-manuscript-revision-and-build-report.md
main.tex
```

The frozen Stage 5.0 relational-routing protocol is recorded in:

```text
reviews/2026-08-11-stage5-0-relational-routing-protocol.md
validation/regulated-transport/config/stage5_relational_routing_protocol.json
validation/regulated-transport/results/stage5_0/
validation/regulated-transport/src/stage50_protocol_audit.py
```

Run all tests:

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

Run the Stage 3.2 comparison from the frozen Stage 3.1 artifact:

```bash
python -m src.stage32_runner \
  --data results/stage3_1 \
  --output results/stage3_2 \
  --seal config/stage32_portable_seal.json \
  --bootstrap-resamples 2000
python -m src.stage32_finalize --output results/stage3_2
```

Run the Stage 3.2.5 capture-proxy sensitivity refit:

```bash
python -m src.stage325_sensitivity_refit \
  --data results/stage3_1 \
  --output results/stage3_2_5
```

Run Stage 4.1 from the preserved Stage 3.1 and Stage 3.2 workflow artifacts:

```bash
python -m src.stage41_counterexample_anatomy \
  --validation /path/to/stage3_1/validation.csv \
  --predictions /path/to/stage3_2/validation_predictions.csv \
  --selection results/stage3_2/selection.json \
  --authorization results/stage3_2_5/authorization_decision.json \
  --output results/stage4_1 \
  --review ../../reviews/2026-08-06-stage4-1-counterexample-anatomy.md
```

Audit the Stage 5.0 protocol without generating evidence:

```bash
python -m src.stage50_protocol_audit \
  --protocol config/stage5_relational_routing_protocol.json \
  --output results/stage5_0/protocol_audit.json
python -m unittest discover -s tests -p 'test_stage50_protocol_audit.py' -v
```

Stage 3.2 locked `CVT-2-minimum` as the primary CVT candidate and `BL-6-full-native-gradient-boosting` as the primary baseline. The four-proxy operationalization did not meet the preregistered thresholds for incremental predictive value, predictive compression, or high-confidence safety-screen utility.

Stage 3.2.5 fairly refit the locked minimum scorer with the primary micro-probe, 2.5x-dose micro-probe, and direct structural capture composite. The dose perturbation left performance effectively unchanged, while the direct composite remained worse after fair calibration.

Stage 4.1 found 92 hosted rows failing at least one gate and 114 nonhosted rows passing all four. Capture-gate failure appeared in 71 of the 92 hosted contradictions, and 90 of the 114 all-pass failures did not reach the transformation target. The native gradient booster reduced error most strongly on hosted rows. Stage 4.2 rejected the measured hard-gate geometry for this bounded simulation and Stage 4.3 revised the canonical manuscript to report that mixed negative result.

Stage 5.0 prospectively defines a fresh relational-routing test. It freezes independent partitions, 31 encoded pre-outcome input/timing/load/history/probe columns, 12 interactions, an equal-column native comparison, separate routing and failure endpoints, and selection, calibration, uncertainty, integrity, stopping, and validation thresholds. The audit passes 12 invariants and eight focused tests. No Stage 5 data have been generated and no revised model has been fitted.

Revised-model execution remains unauthorized. The final test remains ungenerated, unopened, and not authorized.

