# MAS-002 — Hysteresis, Waiting, and Lookahead

Status: executable simulation experiment

## Question

When is a better immediate morphology worth the cost of reshaping into it, and when should Lucian preserve the current shape, remain in an alternative shape for a while, or deliberately let flexible work wait?

MAS-001 exposed a myopic failure mode:

```text
local -> remote -> local
```

can be individually sensible at each tick while globally wasteful because folding/unfolding has a cost.

IAM-001 then showed that learning can introduce a genuinely better new morphology, but also increased transition cost in the reference trajectory.

MAS-002 compares three scheduling postures:

```text
GREEDY
  cheapest feasible running morphology now

STICKY
  penalize switching and preserve a recent morphology for a minimum dwell

LOOKAHEAD
  reason over a bounded future horizon using operating + transition + delay cost
```

Candidate morphologies are assumed to have already passed capability, competence, authority, privacy, safety, and epistemic gates. MAS-002 optimizes only inside that admissible set.

---

## Files

```text
manifests/mas002_scheduler_policy_demo.json
prototype/morphology_scheduler_v002.py
results/MAS_002_REFERENCE_TRACE.md
```

Run from `modern-robotics/lucian-os`:

```bash
py prototype/morphology_scheduler_v002.py
```

Simulation only.

---

## Host and candidate morphologies

Fixed host:

```text
memory = 680 MB
```

Interactive voice reserves:

```text
120 MB
```

Recurring flexible work has three candidate forms:

```text
LOCAL
  memory = 620 MB
  operating cost = 0.10 / tick

REMOTE
  memory = 100 MB
  operating cost = 1.10 / tick

COMPILED
  memory = 300 MB
  operating cost = 0.04 / tick
  available only after an IAM-style learned-skill event
```

Therefore:

```text
local + voice    = 740 MB -> infeasible
remote + voice   = 220 MB -> feasible
compiled + voice = 420 MB -> feasible
```

The transition costs are intentionally non-zero.

---

## Cost decomposition

MAS-002 uses a synthetic objective:

```text
C = operating cost
  + morphology transition cost
  + delay cost for unfinished flexible work
```

Voice is a hard admitted workload rather than a price term.

The lookahead scheduler uses a finite six-tick horizon. This is intentionally small; MAS-002 is not claiming optimal model-predictive control.

---

## Scenario A — clustered pressure

Twelve units of flexible work.

Voice arrives at:

```text
3, 5
```

The two pressure events are close together.

Expected structural result:

```text
greedy:
  local -> remote -> local -> remote -> local

lookahead:
  local -> remote -> remote -> remote -> local
```

The lookahead policy should recognize that immediately returning local between nearby pressure events wastes transition cost.

---

## Scenario B — sparse pressure

Voice arrives at:

```text
3, 10
```

Now the pressure events are far apart.

A scheduler may rationally prefer one of two responses:

```text
switch to a low-memory morphology and keep working
```

or:

```text
preserve the cheap local trajectory around the sparse interruptions
and let flexible work wait during the voice ticks
```

The experiment is deliberately parameterized so the policy comparison can produce a different winner from the clustered case.

---

## Scenario C — learned morphology

Voice arrives at:

```text
4, 8, 12
```

At tick 6 an IAM-style validation event makes a compiled morphology available.

This abstracts the upstream learning process; it does not re-run IA-002 inside MAS-002.

Expected structure:

```text
before tick 6:
  local / remote tradeoff under pressure

after tick 6:
  compiled route becomes available
```

The question is whether the scheduler recognizes that the new morphology has enough future value to justify paying the transition cost into it.

---

## Pass criteria

MAS-002 supports the architecture if the synthetic workload exhibits all of the following:

1. greedy scheduling exposes avoidable morphology thrashing;
2. clustered pressure rewards preserving an alternative morphology across nearby future events;
3. sparse pressure produces a different scheduling regime rather than the same reflexive policy;
4. deliberate waiting can be preferable to unnecessary folding for flexible work;
5. an earned compiled morphology changes the future optimal schedule;
6. all policies preserve the hard interactive workload and eventually complete flexible work;
7. no single policy is defined to win every scenario.

---

## What a pass means

A pass supports a narrow claim:

> **The value of a morphology cannot be evaluated only from the present state; its future usefulness and the cost of entering and leaving it matter.**

Equivalently:

```text
best state now != best trajectory
```

---

## What a pass does not mean

MAS-002 does not establish:

- optimal scheduling;
- real model-loading costs;
- real cloud/local economics;
- an ideal lookahead horizon;
- correct starvation policy;
- continuous-control guarantees;
- that waiting is acceptable for every task class;
- that remote processing is always admissible.

The experiment contains only already-admitted candidate morphologies and a flexible background workload plus hard interactive pressure.

---

## Architectural interpretation

MAS-001 asks:

> Which admissible morphologies can coexist now?

IAM-001 adds:

> Learning can change the available morphologies.

MAS-002 asks:

> **Given those changing possibilities, when is reshaping worth it across time?**

A concise principle:

> **Do not optimize the fold. Optimize the trajectory of folds.**
