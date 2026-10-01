# TEXTURE_001 — Execution Status

**Active design:** v2.1  
**Status:** NOT RUN  
**Provider outputs:** none  
**Adjudication:** not started  
**Execution authorized:** no  
**Harness:** BUILT — REVIEW PENDING CI

TEXTURE_001 v1 was rejected at design review before execution because its compact cues contained evaluative leakage and its packet risked cross-condition contamination.

The complete v1 design is preserved under `archive_v1/`.

The pre-audit v2 design is preserved under `archive_v2_pre_audit/`.

TEXTURE_001 v2.1 is frozen with:

- true counterfactual twins;
- C1 full-Wake versus C2 non-evaluative structured-texture comparison;
- one-item-per-context isolation;
- C0 as an underdetermination baseline;
- a lexical exclusion rule for C2;
- exact current-state, constraint, and question wording within each family.

The pre-run design audit passed.

A provider-agnostic harness now exists at:

```text
code/texture_001_runner.py
```

with tests at:

```text
tests/test_texture_001_runner.py
```

and procedure at:

```text
RUN_PROTOCOL.md
```

The harness:

- prepares one provider-visible prompt per case;
- does not call any provider API;
- requires explicit fresh-context attestation;
- preserves malformed outputs rather than repairing them;
- refuses result overwrite;
- hashes prompt and raw output;
- freezes raw-result artifacts before adjudication;
- does not read the adjudication key.

No model run has been performed under v1, pre-audit v2, or v2.1.

The next permitted activity is **harness review / CI verification only**.

Execution still requires a separate explicit decision.
