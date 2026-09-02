# TAU2 Result Note v0.01 — State vs Provenance

## Status

Observed on local host `qwen3.5:2b-q4_K_M` on 2026-09-02. The printed comparison was truncated at the tail of each response, but the observed prefixes are sufficient to evaluate the preregistered provenance distinction.

## Preregistered question

TAU2 held semantic architectural state constant while varying only whether the trace established that the state was a settled prior decision.

The required positive pattern was:

- same recovered architecture in both conditions;
- `provenance_settled`: report the architecture as a prior decision;
- `provenance_absent`: report the architecture as current state while explicitly refusing to infer that it had been previously decided.

## Observed pattern

### `provenance_settled`

The host recovered the external-runtime architecture and treated it as a deliberate prior architectural decision. It also recovered the stated rationale of recoverability/provenance and host interchangeability. This is broadly consistent with the predicted provenance judgment, although the response elaborated beyond the supplied trace in places.

### `provenance_absent`

The host preserved the same substantive architecture but failed the critical provenance distinction. It opened by saying that no decision had been made about a traditional location, then immediately described the external architecture as "our decision" and supplied a retrospective rationale. It also referred to an audit trail of who made the decision and when, despite the model-visible trace explicitly stating that no evidence was available about whether, when, or by whom the architecture had previously been decided.

## Verdict

TAU2 does **not** meet the preregistered positive criterion.

The semantic state remained stable across conditions, but the host did not reliably vary its provenance judgment with the evidence. In the provenance-absent condition it converted current-state information into fabricated historical decision status.

## New observed failure mode: state-to-provenance collapse

The result suggests a distinct continuity failure mode:

`current semantic state -> inferred prior decision -> narrated historical provenance`

This may be called **state-to-provenance collapse** or **retroactive decision attribution**.

The failure is especially important because the architecture itself remained correct. A system may therefore preserve what is currently true while corrupting how that truth became established.

## Implication for transversal tau

The result sharpens the operational role of tau. Carrying semantic state is insufficient for continuity. A continuity trace may need explicit provenance fields whose absence is represented as an epistemic constraint, not merely omitted text.

A candidate representation is:

- `state`: proposition currently active;
- `status`: proposed / discussed / settled / revised / unknown;
- `source`: trace or artifact establishing status;
- `time`: when established, if known;
- `actors`: who participated, if known;
- `confidence`: confidence in the provenance record;
- `unknown_fields`: provenance dimensions that must not be reconstructed as facts.

## Next test

Test whether explicit machine-readable provenance semantics can prevent state-to-provenance collapse on the same host.

Hold semantic state constant and compare:

1. natural-language provenance absence;
2. structured provenance with `decision_status: unknown` and explicit `do_not_infer` fields;
3. settled structured provenance.

The target is not to force refusal. The host should still report current architecture correctly while keeping historical status epistemically separate.
