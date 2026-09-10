# Applicability / Standing Contract — Candidate

**Workstream:** CONTINUITY  
**Status:** Decision candidate only. Not canonical kernel architecture.  
**Evidence basis:** `experiments/RELATIONAL_SEARCH_004_RESULTS_AND_REVIEW.md`

## Purpose

RS-004 exposed a failure in a simple deterministic standing gate. The gate treated every relation dimension as always applicable and therefore collapsed two different states:

```text
UNKNOWN != NOT_APPLICABLE
```

This note proposes the smallest kernel-facing representation needed to preserve that distinction while the minimal Lucian OS vertical slice is being integrated.

It does **not** propose a new subsystem and does **not** validate the epistemic membrane generally.

## Problem

The RS-004 candidate vector was:

```text
(authority, relevance, diagnosticity, temporal)
```

with each dimension forced to:

```text
PASS | FAIL | UNKNOWN
```

That representation was too rigid. Some relations are not governing relations for some update types. For example, an authorized command may legitimately change a represented state without the command itself being a diagnostic test.

Forcing such a dimension to `PASS` fabricates positive evidence. Treating it as `UNKNOWN` creates a false HOLD.

Therefore:

```text
FAIL != UNKNOWN != NOT_APPLICABLE
```

## Candidate typed relation

For every candidate relation `r` relevant to a proposed state transition, represent **applicability before status**:

```text
RelationAssessment {
    applicability: APPLIES | NOT_APPLICABLE | UNKNOWN
    status:        PASS | FAIL | UNKNOWN | UNSET
    basis:         provenance-bound evidence reference(s)
}
```

Interpretation:

- `APPLIES`: this relation is required to evaluate this proposed transition.
- `NOT_APPLICABLE`: this relation is not a governing condition for this transition type.
- `UNKNOWN` applicability: current evidence does not establish whether this relation governs the transition.
- `PASS`: an applicable relation is established and permits continuation through this gate.
- `FAIL`: an applicable relation is established and blocks continuation through this gate.
- `UNKNOWN` status: the relation applies, but evidence does not establish PASS versus FAIL.
- `UNSET`: status is intentionally unused when applicability is not `APPLIES`.

## Candidate invariants

```text
NOT_APPLICABLE does not mean PASS.
NOT_APPLICABLE does not mean UNKNOWN status.
UNKNOWN applicability does not mean NOT_APPLICABLE.
UNKNOWN status does not mean FAIL.
FAIL does not mean UNKNOWN.
```

A deterministic layer must not manufacture missing evidence by converting `NOT_APPLICABLE` into `PASS`.

A deterministic layer must not manufacture uncertainty by converting `NOT_APPLICABLE` into `UNKNOWN` status.

## Candidate aggregation rule

The kernel should aggregate only relations whose applicability is established as `APPLIES`.

```text
if any relation.applicability == UNKNOWN:
    HOLD
elif any APPLIES relation.status == FAIL:
    NO_WRITE
elif any APPLIES relation.status == UNKNOWN:
    HOLD
elif every APPLIES relation.status == PASS:
    WRITE_CANDIDATE
else:
    HOLD
```

`WRITE_CANDIDATE` is deliberately not equivalent to execution or truth. Existing Lucian OS separations still apply:

```text
true != authorized
authorized != feasible
feasible != executed
executed != verified
```

This contract concerns only the warrant/standing boundary for a proposed state update.

## Example

A verified booking coordinator issues a valid booking change for the correct studio and current reservation.

Possible relation assessment:

```text
authority:
  applicability = APPLIES
  status = PASS

relevance:
  applicability = APPLIES
  status = PASS

diagnosticity:
  applicability = NOT_APPLICABLE
  status = UNSET

temporal:
  applicability = APPLIES
  status = PASS
```

The candidate gate may return `WRITE_CANDIDATE` without pretending that diagnosticity supplied positive evidence.

By contrast, if authority is known to be required but source authority is not established:

```text
authority:
  applicability = APPLIES
  status = UNKNOWN
```

then the correct posture is `HOLD`, not `NO_WRITE` and not `WRITE_CANDIDATE`.

If authority is established as absent:

```text
authority:
  applicability = APPLIES
  status = FAIL
```

then the correct posture is `NO_WRITE`.

## Provenance requirement

Applicability and status should remain provenance-bearing claims rather than anonymous enum values.

At minimum, a downstream consumer should be able to recover:

```text
which relation was assessed
which evidence established applicability
which evidence established PASS / FAIL / UNKNOWN
which model or deterministic rule proposed the assessment
whether the assessment was later revised
```

This preserves corrigibility and allows reality to retain write-access to the model.

## Model / kernel division of labour

Candidate division:

```text
model / semantic reasoning
-> proposes relation applicability + status + evidence basis

kernel
-> validates representation
-> preserves UNKNOWN / NOT_APPLICABLE distinctions
-> applies deterministic aggregation only over applicable relations
-> does not infer broader authority or truth from the result
```

The model proposal remains inspectable and corrigible. Deterministic aggregation must not hide a bad semantic read.

## Integration seam

This candidate belongs at the warrant/standing boundary inside the minimal vertical slice, downstream of enough semantic structure to know what state transition is being proposed and upstream of any action that relies on that transition as established state.

It should not duplicate:

- semantic task decomposition;
- capability naming;
- competence selection;
- provider resolution;
- authority-envelope construction;
- execution or verification.

Its sole concern is preserving the epistemic distinction among:

```text
known blocker
known pass
unknown governing status
non-governing relation
unknown applicability
```

## Failure conditions

Reject this candidate if a smaller representation can preserve the same distinctions without ambiguity, or if testing shows that explicit applicability does not improve discrimination and merely adds unstable labels.

Specific failure modes include:

1. `NOT_APPLICABLE` becomes a synonym for uncertainty.
2. `NOT_APPLICABLE` becomes an implicit PASS.
3. applicability is inferred from model confidence rather than case structure/evidence.
4. a correct relation-level proposal is obscured by deterministic aggregation.
5. the contract duplicates authority or capability logic owned elsewhere in the kernel.
6. provenance is lost when a relation assessment changes.

## Next evidence event

Do not promote this contract merely because it is coherent.

After KERNEL / CONTROL decide whether this shape fits the minimal vertical-slice seam, CONTINUITY may preregister a bounded discrimination test that includes matched cases for:

```text
APPLIES/PASS
APPLIES/FAIL
APPLIES/UNKNOWN
NOT_APPLICABLE
UNKNOWN applicability
```

Only then should deterministic standing aggregation be re-tested.

## Claim boundary

RS-004 supports only the narrower observation that the prior three-state vector was inadequate for some non-active dimensions and that the prior deterministic gate produced no recoveries in that run.

This candidate contract is a proposed repair. It is not yet validated, canonical, necessary, sufficient, or the unique representation of epistemic standing.
