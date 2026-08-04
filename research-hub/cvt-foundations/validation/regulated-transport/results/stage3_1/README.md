# Stage 3.1 development evidence

The full deterministic `training.csv` and `validation.csv` files are intentionally not stored in Git because they are large generated evidence artifacts. They are reproduced from the frozen Stage 3.1 code and design, then verified by the committed SHA-256 manifests.

Committed here:

- partition manifests and hashes;
- combined environment/design manifest;
- integrity summary;
- family-by-forcing-stratum balance tables;
- failure-reason counts.

Not generated or accessed in Stage 3.1:

- the final test partition;
- candidate predictions;
- fitted model or calibration parameters.

Generate the development evidence from the validation-package directory:

```bash
python -m src.stage31_dataset --output results/stage3_1 --workers 1
```

The generator writes resumable 500-row checkpoint files and refuses `test` as a partition name.
