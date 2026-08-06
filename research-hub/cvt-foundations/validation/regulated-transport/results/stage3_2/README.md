# Stage 3.2 locked validation results

These files record the preregistered training/calibration/validation comparison. Validation was opened once. The final test partition was not generated or opened.

Workflow execution:

```text
run ID       31067552847
artifact ID  8954425503
artifact     cvt-stage3-2-results
artifact SHA sha256:46586935a20cec026c1099d5d906b34aa8a7c9b2d97a8ff76ddfa58fa9636320
```

Committed result files include the metrics, selection, tuning record, model metadata, portable-seal report, false-safe counts, execution record, and model-lock manifest.

The row-level `validation_predictions.csv` is reproducible generated evidence and is not committed because of size. Its locked identity is:

```text
SHA-256 2889eae1387498de9547a293e2a28a4ee314f79528bb9137cb2843f33b8cecd2
rows    4,000
```

The preserved workflow artifact contains the prediction file and exact environment record. The scientific interpretation is in:

```text
reviews/2026-08-05-stage3-2-validation-model-comparison.md
```
