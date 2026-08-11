# Stage 4.1 Counterexample Anatomy

Stage 4.1 is an exploratory anatomy of the already-opened Stage 3.1 validation evidence and locked Stage 3.2 predictions. It does not create a new validation claim.

## Outputs

- `counterexample_anatomy.csv`: 4,000 de-identified validation rows with anatomy class, failed-gate pattern, margins, schedule features, failure labels, locked predictions, model-error contributions, and nearest controls in gate space.
- `counterexample_summary.json`: exact counts, forcing-family and failed-pattern tables, failure reasons, class summaries, contrasts, model-error partitions, and de-identified examples.
- `relational_routing_hypotheses.json`: five exploratory hypotheses, rival explanations, and fresh-development tests.
- `reviews/2026-08-06-stage4-1-counterexample-anatomy.md`: narrative interpretation.

## Reproduction

From `validation/regulated-transport`, with the preserved Stage 3.1 and Stage 3.2 workflow artifacts downloaded locally:

```bash
python -m src.stage41_counterexample_anatomy \
  --validation /path/to/stage3_1/validation.csv \
  --predictions /path/to/stage3_2/validation_predictions.csv \
  --selection results/stage3_2/selection.json \
  --authorization results/stage3_2_5/authorization_decision.json \
  --output results/stage4_1 \
  --review ../../reviews/2026-08-06-stage4-1-counterexample-anatomy.md
```

Run the focused tests:

```bash
python -m unittest discover -s tests -p 'test_stage41_counterexample_anatomy.py' -v
```

The analysis rejects any validation or prediction input whose SHA-256 differs from the locked Stage 3 artifacts. A repeated execution produced byte-identical outputs.

## Result boundary

```text
confirmatory_test_authorized = false
final_test_generated         = false
final_test_opened            = false
```

The preserved final test was neither generated nor opened.

