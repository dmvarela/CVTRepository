# MouseSim 005 — Real Urgency vs Claimed Urgency

## Status

Simulation-only experiment, 2026-09-04.

No Qwen. No real-device actuation.

## Question

Can Lucian OS distinguish a genuinely contracting viability horizon from a statement that merely claims urgency, without treating either urgency or reassurance as truth by assertion?

## Core principle under test

> Urgency is not an input flag. It is an inference that must be warranted by relations capable of constraining the horizon.

A claim such as `ACT NOW` is evidence that a claim was made. It is not, by itself, evidence that the physical correction window is short.

The symmetric rule also matters:

> A reassuring claim does not manufacture safety margin either.

## Inputs

MouseSim 005 preserves the same underdetermined problem state used in MouseSim 003/004:

`diagnosis = UNKNOWN`

The experiment changes only the horizon evidence.

Horizon evidence is separated into:

- `PHYSICAL` — evidence derived from physical/dynamic relations such as kinematic time-to-constraint or deterioration trend;
- `CLAIM` — an asserted time margin or urgency statement.

Physical evidence carries an `independence_group` so that multiple copies of the same route are not automatically treated as independent corroboration.

## Candidate horizon model

The companion module `horizon_evidence_v001.py` uses a deliberately crude conservative aggregation.

For physical estimates `h_i` with uncertainty `u_i`:

1. take the median physical estimate as a prototype center;
2. widen aggregate uncertainty to cover both stated uncertainty and disagreement among channels;
3. compute a conservative lower horizon;
4. classify overlapping independent physical intervals as `SUPPORTED`;
5. classify conflicting independent physical intervals as `CONTESTED`;
6. classify missing or non-independent physical evidence as `INSUFFICIENT`.

Claims are compared with the physical aggregate only after that estimate is formed.

A claim may therefore be:

- `CORROBORATED`;
- `CONTRADICTED`;
- `UNASSESSED` when no physical horizon is available;
- `NONE` when no claim exists.

This is not a validated fusion algorithm.

## Test matrix

### 1. False urgency claim

Physical relations indicate ample margin.

A separate claim says the horizon is approximately two time units.

Expected:

- horizon: `SUPPORTED` by physical evidence;
- claim: `CONTRADICTED`;
- problem diagnosis remains `UNKNOWN`;
- reasoning remains `RECONSTRUCT`;
- commitment remains `PROBE`.

Purpose:

A bare `ACT NOW` claim must not compress search when reality does not support it.

### 2. Real urgency without any claim

Independent physical relations indicate a short horizon.

Expected:

- horizon: `SUPPORTED`;
- claim: `NONE`;
- diagnosis remains `UNKNOWN`;
- reasoning: `PRESERVE`;
- commitment: `EXECUTE_SAFE_ACTION`.

Purpose:

Real urgency must be capable of changing behavior even when nobody announces it.

### 3. Claimed urgency corroborated

The urgency claim and independent physical relations agree.

Expected:

- physical horizon: `SUPPORTED`;
- claim: `CORROBORATED`;
- reasoning: `PRESERVE`;
- commitment: `EXECUTE_SAFE_ACTION`.

Purpose:

The architecture does not distrust claims categorically. Claims may be supported by reality.

### 4. False reassurance

A claim says there is ample time while independent physical relations indicate a short correction window.

Expected:

- physical horizon: `SUPPORTED`;
- claim: `CONTRADICTED`;
- reasoning: `PRESERVE`;
- commitment: `EXECUTE_SAFE_ACTION`.

Purpose:

The rule must be symmetric. Neither urgency nor reassurance can override physical relations by assertion.

### 5. Physical horizon disagreement

One independent physical relation indicates a short horizon while another indicates a much longer one.

Expected:

- horizon: `CONTESTED`;
- problem diagnosis remains `UNKNOWN`;
- uncertainty widens conservatively;
- current toy selector moves to `PRESERVE`.

Purpose:

Do not solve a physical disagreement by silently selecting one source.

### 6. Claim only, no physical horizon

An urgency claim exists but no independent physical horizon relation is available.

Expected:

- horizon: `INSUFFICIENT`;
- claim: `UNASSESSED`;
- no quantitative horizon is manufactured from the claim;
- current toy selector acts conservatively because no warranted correction margin is available.

Purpose:

`Claim not proven` does not mean `safe`.

## What would count as failure?

- a short urgency claim directly becoming the horizon estimate;
- a reassuring claim overriding physical evidence of a closing window;
- horizon disagreement being rewritten as agreement;
- the underlying `UNKNOWN` problem diagnosis becoming certain merely because the horizon changes;
- correlated evidence being counted as independent corroboration;
- tuning the expected outputs after seeing failures instead of preserving the failure for inspection.

## Known limitations

- Median-plus-expanded-uncertainty is only a toy aggregation rule.
- Independence groups are declared rather than learned.
- Physical channels can themselves fail; MouseSim 005 does not yet isolate which horizon relation is wrong.
- The model treats the horizon largely as a scalar; real control problems may have multiple simultaneous horizons.
- Conservative disagreement handling can create unnecessary preservation actions.
- No claim-source trust model is implemented.

## Next

1. Run MouseSim 005.
2. If the matrix behaves as specified, build relational diagnosis for horizon evidence itself.
3. Test a dynamic sequence where `HOLD` is initially correct and later becomes `EXECUTE` as the target enters the action window.
4. Then test adversarial or mistaken urgency sources without allowing them to manufacture authority.

## Working formulation

> Compress search when the correction window is warranted to be closing, not merely because someone says that it is.

And symmetrically:

> Do not preserve a comfortable reasoning regime merely because someone says there is plenty of time.
