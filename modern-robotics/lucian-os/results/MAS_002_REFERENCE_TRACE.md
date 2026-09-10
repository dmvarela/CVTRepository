# MAS-002 — Reference Simulation Trace

Status: reference trace from local sandbox execution of the MAS-002 scheduling logic

This is a deterministic architecture simulation using synthetic costs and footprints from `manifests/mas002_scheduler_policy_demo.json`.

It is **not** a benchmark of a real OS, model, computer, cloud provider, or deployment.

Run from `modern-robotics/lucian-os`:

```bash
py prototype/morphology_scheduler_v002.py
```

## Policies

```text
GREEDY
  lowest current operating-cost running morphology
  ignores future switching consequence

STICKY
  penalizes switching and preserves recent morphology

LOOKAHEAD
  six-tick bounded search over
  operating + transition + unfinished-work delay cost
```

All candidate morphologies are assumed already admissible. Voice is treated as a hard interactive workload.

---

## Scenario A — clustered pressure

Voice ticks:

```text
3, 5
```

Reference totals:

```text
GREEDY
  finish ticks       = 12
  switches           = 4
  remote ticks       = 2
  transition cost    = 14.0
  operating cost     = 3.2
  delay cost         = 23.4
  total modeled cost = 40.6

STICKY
  finish ticks       = 12
  switches           = 1
  remote ticks       = 10
  transition cost    = 4.0
  operating cost     = 11.2
  delay cost         = 23.4
  total modeled cost = 38.6

LOOKAHEAD
  finish ticks       = 12
  switches           = 2
  remote ticks       = 3
  transition cost    = 8.0
  operating cost     = 4.2
  delay cost         = 23.4
  total modeled cost = 35.6
```

Key lookahead trajectory:

```text
tick 1 local
tick 2 local
tick 3 remote   <- voice
tick 4 remote   <- stay folded
tick 5 remote   <- voice
tick 6 local    <- pressure cluster has passed
```

Greedy instead performs:

```text
local -> remote -> local -> remote -> local
```

Reference interpretation:

> Nearby future pressure can make it cheaper to remain in a temporarily suboptimal morphology than to immediately unfold and refold.

---

## Scenario B — sparse pressure

Voice ticks:

```text
3, 10
```

Reference totals:

```text
GREEDY
  finish ticks       = 12
  switches           = 4
  remote ticks       = 2
  idle ticks         = 0
  total modeled cost = 40.6

STICKY
  finish ticks       = 12
  switches           = 1
  remote ticks       = 10
  idle ticks         = 0
  total modeled cost = 38.6

LOOKAHEAD
  finish ticks       = 14
  switches           = 4
  remote ticks       = 0
  idle ticks         = 2
  total modeled cost = 38.8
```

The lookahead scheduler deliberately pauses the flexible recurring work at the two voice ticks instead of paying to enter the remote morphology.

The sticky policy wins this particular synthetic scenario by a narrow margin (`38.6 < 38.8`).

This is a useful result because MAS-002 is not parameterized so that lookahead must always win.

Reference interpretation:

> Sometimes the rational response to a short resource conflict is not to reshape the task at all; it is to let flexible work wait.

That choice sacrifices two completion ticks but avoids remote execution.

---

## Scenario C — learned morphology

Voice ticks:

```text
4, 8, 12
```

IAM-style compiled morphology becomes available at:

```text
tick 6
```

Reference totals:

```text
GREEDY
  finish ticks       = 12
  switches           = 3
  remote ticks       = 1
  transition cost    = 11.0
  operating cost     = 1.78
  total modeled cost = 36.18

STICKY
  finish ticks       = 12
  switches           = 1
  remote ticks       = 9
  transition cost    = 4.0
  operating cost     = 10.2
  total modeled cost = 37.6

LOOKAHEAD
  finish ticks       = 12
  switches           = 2
  remote ticks       = 2
  transition cost    = 7.0
  operating cost     = 2.78
  total modeled cost = 33.18
```

Key lookahead trajectory:

```text
ticks 1-3  local
tick 4     remote   <- voice pressure
tick 5     remote   <- do not fold back for one tick
tick 6     compiled <- learned form becomes available
ticks 6-12 compiled
```

Greedy does an unnecessary intermediate return:

```text
tick 4 remote
tick 5 local
tick 6 compiled
```

The lookahead scheduler sees enough future value in the newly learned morphology to pay the transition into it and then remain there.

Reference interpretation:

> Learning changes not only which morphology exists, but whether entering that morphology now has positive trajectory value.

---

## Regime comparison

The reference winner changes by workload:

```text
clustered pressure -> LOOKAHEAD
sparse pressure    -> STICKY
learned morphology -> LOOKAHEAD
```

No policy is defined to win universally.

Greedy is consistently harmed in these scenarios by ignoring future transition consequences, but this experiment does not establish that greedy scheduling is always inferior in real systems.

---

## Checks

Reference logic satisfies:

```text
T1_greedy_exposes_thrashing = PASS
T2_clustered_pressure_rewards_short_lookahead = PASS
T3_sparse_pressure_can_reward_stickiness = PASS
T4_lookahead_can_choose_waiting_over_unnecessary_fold = PASS
T5_learned_morphology_changes_future_optimum = PASS
T6_learned_form_is_taken_when_future_value_justifies_switch = PASS
T7_all_policies_preserve_hard_voice_and_complete_work = PASS

overall = PASS
```

---

## What MAS-002 supports

MAS-002 supports a narrow executable claim:

> **A morphology should be evaluated partly by the future trajectory it enables and by the cost of entering and leaving it, not only by its immediate resource or operating cost.**

Three behaviors emerge:

```text
clustered future pressure
  -> remain temporarily in alternative morphology

sparse short pressure
  -> waiting can beat reshaping

new learned morphology with durable future benefit
  -> pay transition cost and adopt it
```

A concise formulation:

> **Do not optimize the fold. Optimize the trajectory of folds.**

---

## What this does not establish

The simulation uses a finite six-tick horizon and synthetic scalar costs. It does not establish the correct production policy, real switching costs, realistic model residency, starvation guarantees, or continuous-control scheduling.

The next architecture question is how to choose the lookahead horizon and transition model from **observed host behavior** rather than fixed toy constants. That would connect MAS directly back to computational proprioception and calibration.
