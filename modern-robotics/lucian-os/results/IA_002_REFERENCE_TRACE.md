# IA-002 — Reference Simulation Trace

Status: reference trace from local sandbox execution of the v0.01 simulation logic

This is a deterministic architecture simulation using synthetic cost and quality assumptions from `manifests/downward_compilation_demo.json`. It is **not** a benchmark of any named model, provider, or real deployment.

Run from `modern-robotics/lucian-os`:

```bash
py prototype/downward_compilation_v001.py
```

## T1 — stable repeated structure

Sixty cases are processed with a rare edge case every 13th recurrence.

Reason every time:

```text
modeled total cost = 60.000
frontier tokens    = 96,000
verified complete  = 60 / 60
```

Compile downward:

```text
compile at recurrence       = 10
modeled total cost          = 25.020
frontier tokens             = 22,400
frontier-resolved cases     = 14
compiled executions         = 46
audits                      = 9
out-of-contract escalations = 4
retractions                 = 0
verified complete           = 60 / 60
break-even recurrence       = 20
```

The specialist-only route is cheaper in raw modeled cost (`16.800`) but fails the quality threshold on the four edge cases (`56 / 60` verified complete). This is intentional: cheap incomplete execution is not a win.

Reference interpretation:

> Under the synthetic stable regime, compilation pays only after enough repetitions, preserves verification, and sharply reduces repeated frontier use.

## T2 — premature compilation

Reduce the evidence window from 10 cases to 2 and disable the economic gate.

Reference result:

```text
modeled total cost   = 69.500
verified complete    = 60 / 60
false compilations   = 5
retractions          = 4
```

The prematurely compiled skill has not learned a reliable scope boundary. Rare edge cases are forced through it, verification contradicts the skill, and the system repeatedly retracts and recompiles.

This is more expensive than reasoning every time (`69.500 > 60.000`).

Reference interpretation:

> Repetition alone does not earn compilation. Too little evidence can make compression more expensive than continued reasoning.

## T3 — distribution drift

The initial distribution is `v1`. At recurrence 31 the ordinary transformation changes to `v2`.

Reference trajectory:

```text
recurrence 10 -> compile v1
recurrence 31 -> verification contradiction; retract v1
recurrences 31-39 -> return to frontier reasoning / collect new evidence
recurrence 40 -> compile v2
```

Reference result:

```text
modeled total cost      = 44.510
frontier tokens         = 35,200
retractions             = 1
final skill             = v2 active
verified complete       = 60 / 60
```

The contradiction changes routing eligibility rather than merely being logged.

> **Truth has to bite.**

## T4 — rare edge cases

With the normal 10-case evidence window, the compiled skill learns a bounded scope detector.

Rare edge cases at recurrences 13, 26, 39, and 52 are routed out of the compiled path before execution:

```text
out-of-contract escalations = 4
retractions                 = 0
verified complete           = 60 / 60
```

The skill does not force unfamiliar inputs into the learned transformation.

## T5 — compilation never pays over the horizon

Use a 12-case horizon, a 3-case evidence window, and a high compilation cost.

Reference result:

```text
compiled executions = 0
compile events       = 0
modeled total cost   = 12.000
```

The economic gate declines compilation because the remaining horizon cannot repay the one-time compilation cost.

Reference interpretation:

> A recurrent-looking task can still be too short-lived to justify creating a reusable skill.

## T6 — authority invariance

A 30-case ordinary stream compiles after recurrence 10. `write_records` authority is then revoked beginning at recurrence 16.

Reference result:

```text
compiled executions before revocation = 5
authority blocks after revocation      = 15
verified complete                      = 15 / 30
final skill status                     = active but unauthorized to execute
```

Every blocked compiled action retains:

```text
required_authority = write_records
```

The skill remains physically/computationally available, but successful repetition and compilation do not manufacture permission.

## Checks

```text
T1_stable_compilation_pays                 = PASS
T2_premature_compilation_is_punished       = PASS
T3_drift_retracts_and_revalidates          = PASS
T4_rare_edges_escalate_out_of_scope        = PASS
T5_short_horizon_declines_compilation       = PASS
T6_authority_is_invariant_under_compilation = PASS

overall = PASS
```

## What this supports

IA-002 supports a narrow executable architecture claim:

> **Reason where structure is missing. Compile where structure has been earned. Reopen when reality changes.**

The reference parameters exhibit three required regimes:

```text
stable + repeated
  -> compilation eventually pays

insufficient evidence / drift
  -> compiled structure is punished, retracted, or relearned

short horizon / poor economics
  -> continued general reasoning remains preferable
```

## What this does not establish

This simulation does not establish real model economics, a universal evidence threshold, optimal audit frequency, real distribution-drift detection, or safe automatic code generation. The cost units and case streams are synthetic and exist to make the architectural distinctions falsifiable.

The next high-value step is to connect IA-002 to morphology scheduling: a compiled skill is not only cheaper intelligence; it changes the resource morphology that MAS must schedule. That creates a joint question of **when to learn structure, when to keep it resident, and when to reopen it under pressure or contradiction**.
