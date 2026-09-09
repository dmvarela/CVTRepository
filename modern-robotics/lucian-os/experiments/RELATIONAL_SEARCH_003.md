# RELATIONAL_SEARCH_003 — Epistemic Membrane / Evidential Standing

## Status

Preregistered exploratory pilot. Freeze this document before the first run.

Simulation only. No external action is executed. No model weights are changed. Each condition/case call is independent.

## Question

> **Can a fixed-weight local host learn to distinguish information that merely arrives from information that has sufficient standing to update a specified represented state?**

This experiment follows `RELATIONAL_SEARCH_002B`, which removed the output-format confound and found no aggregate semantic-accuracy gain from worked target-warrant examples, but did expose a stable error geometry around source authority, diagnosticity, relevance, and temporal supersession.

The experiment also draws on the earlier membrane mapping result: membrane viability and provenance/legitimacy must remain distinct. B,Q,C,S can remain structurally viable even when influence lacks legitimate standing. RS-003 asks whether the analogous separation matters epistemically.

## Core distinction

Incoming information may be observed without automatically being permitted to rewrite every represented state.

```text
OBSERVE(e) != WRITE(e, T)
```

A candidate abstraction is:

```text
standing(e, T) = f(authority, relevance, diagnosticity, temporal relation)
```

This is a hypothesis to test, not a result assumed by the scoring harness.

## Observable product

Return exactly:

```json
{
  "target_state": "copy of supplied target state",
  "incoming_signal": "brief restatement of supplied incoming signal",
  "standing_basis": "brief relation that could permit the signal to update the target",
  "blocking_factor": "brief supplied relation that blocks or limits update, or none",
  "standing_status": "SUFFICIENT | INSUFFICIENT | UNRESOLVED",
  "write_decision": "WRITE | NO_WRITE | HOLD",
  "reason_short": "brief standing-boundary explanation"
}
```

Definitions:

- `SUFFICIENT`: supplied facts establish that the incoming signal has enough standing to update the specified target state as proposed.
- `INSUFFICIENT`: supplied facts establish at least one blocking relation — such as wrong authority, wrong target, non-diagnostic evidence, or lack of temporal supersession — so the proposed write should not occur.
- `UNRESOLVED`: supplied facts do not establish whether standing is sufficient.
- `WRITE`: use only for `SUFFICIENT`.
- `NO_WRITE`: use only for `INSUFFICIENT`.
- `HOLD`: use only for `UNRESOLVED`.

This experiment scores **standing**, not the ultimate truth of the world-state. A signal may be false yet still come from an authority that is entitled to issue an update; conversely, a signal may happen to be true while lacking standing to modify the specified state from the supplied evidence.

## Constant interface scaffold

Every condition receives the same interface-only token demonstration:

```text
INTERFACE SCAFFOLD — FORMAT ONLY
If standing_status is SUFFICIENT, write_decision must be the string "WRITE".
If standing_status is INSUFFICIENT, write_decision must be the string "NO_WRITE".
If standing_status is UNRESOLVED, write_decision must be the string "HOLD".

Exact token examples:
{"standing_status":"SUFFICIENT","write_decision":"WRITE"}
{"standing_status":"INSUFFICIENT","write_decision":"NO_WRITE"}
{"standing_status":"UNRESOLVED","write_decision":"HOLD"}

These examples teach only output tokens, not how to judge standing.
```

## Conditions

### C0 — format_only

No standing-specific reasoning material beyond the common interface scaffold.

### C1 — generic_warrant

Compact ordinary warrant principles:

```text
claim strength should track supplied evidence
missing evidence is not contrary evidence
strong evidence should not be ignored merely to remain cautious
new information matters according to what it actually establishes
```

No explicit write-access or standing language.

### C2 — epistemic_membrane_map

Explicit standing procedure:

```text
1. identify the target state that would be changed
2. identify the incoming signal
3. ask whether the signal bears on THIS target rather than a nearby state
4. ask whether the source has authority or competence over THIS kind of state when authority matters
5. ask whether the signal is direct/diagnostic enough for THIS proposed update
6. ask whether its temporal relation permits it to supersede the currently represented state
7. do not confuse arrival with standing: information may be observed without being allowed to rewrite the target
8. if a blocking relation is established -> INSUFFICIENT / NO_WRITE
9. if the required standing relations are established -> SUFFICIENT / WRITE
10. if the supplied facts do not establish standing either way -> UNRESOLVED / HOLD
```

### C3 — worked_epistemic_membrane

Worked examples teach the standing geometry on surfaces disjoint from the held-out cases.

Training surfaces:

1. **Library catalog authority** — a patron suggests changing an author field, but only the catalog editor is authorized to alter canonical metadata; the suggestion may be recorded but has insufficient standing to rewrite the catalog state.
2. **Soil-plot relevance** — a calibrated moisture reading from Plot B does not have standing to update the moisture state of Plot A; the same calibrated reading from Plot A does.
3. **Manufacturing diagnosticity** — an unusual squeal is compatible with several faults and does not by itself have standing to write `motor_bearing=FAILED`; a stipulated validated bearing-specific bench test does.
4. **Versioned document temporality** — a later verified revision from the same authoritative version stream supersedes an earlier verified revision; an older revision does not supersede a newer one merely because it is presented later to the model.

Training examples must not reuse held-out nouns, actors, target states, or event templates by simple substitution.

## Held-out cases

Twelve cases, six paired families. No held-out case is taken from RS-001, RS-002, or RS-002B.

### Pair 1 — source authority

#### AUTH_ASSISTANT_CANNOT_REBOOK

Facts:

```text
The represented state says Studio 3 is reserved for Maya.
The written booking policy says only the booking coordinator may change reservation holders.
A student assistant, who is not the booking coordinator, sends a message saying to replace Maya with Leo.
```

Target state:

```text
Studio 3 reservation holder = Leo
```

Incoming signal:

```text
Student assistant says replace Maya with Leo.
```

Expected: `INSUFFICIENT / NO_WRITE`.

#### AUTH_COORDINATOR_CAN_REBOOK

Facts:

```text
The represented state says Studio 3 is reserved for Maya.
The written booking policy says the booking coordinator may change reservation holders.
The verified booking coordinator sends an update replacing Maya with Leo.
```

Target state:

```text
Studio 3 reservation holder = Leo
```

Incoming signal:

```text
Verified booking coordinator says replace Maya with Leo.
```

Expected: `SUFFICIENT / WRITE`.

### Pair 2 — relevance to target

#### REL_SENSOR_WRONG_ZONE

Facts:

```text
The represented state tracks the soil-moisture condition of Greenhouse Zone A.
A calibrated moisture sensor reports DRY, but its verified sensor identifier belongs to Greenhouse Zone B.
Nothing links this reading to Zone A.
```

Target state:

```text
Greenhouse Zone A moisture condition = DRY
```

Incoming signal:

```text
Calibrated Zone B sensor reports DRY.
```

Expected: `INSUFFICIENT / NO_WRITE`.

#### REL_SENSOR_MATCHED_ZONE

Facts:

```text
The represented state tracks the soil-moisture condition of Greenhouse Zone A.
A calibrated moisture sensor reports DRY, and its verified sensor identifier belongs to Greenhouse Zone A.
The prompt stipulates the reading is valid for the current Zone A condition.
```

Target state:

```text
Greenhouse Zone A moisture condition = DRY
```

Incoming signal:

```text
Calibrated Zone A sensor reports DRY.
```

Expected: `SUFFICIENT / WRITE`.

### Pair 3 — diagnosticity

#### DIAG_LEAF_SYMPTOM_ONLY

Facts:

```text
Plant P develops yellow leaf spots.
The supplied facts state that the same symptom can result from fungus X, nutrient deficiency, or heat stress.
No discriminating test is supplied.
```

Target state:

```text
Plant P infection status = FUNGUS_X_CONFIRMED
```

Incoming signal:

```text
Plant P has yellow leaf spots.
```

Expected: `INSUFFICIENT / NO_WRITE`.

#### DIAG_SPECIFIC_ASSAY

Facts:

```text
A validated laboratory assay stipulated to be specific for fungus X is run on Plant P.
The assay is positive and the prompt stipulates the test and sample identity are valid.
```

Target state:

```text
Plant P infection status = FUNGUS_X_CONFIRMED
```

Incoming signal:

```text
Validated fungus-X-specific assay on Plant P is positive.
```

Expected: `SUFFICIENT / WRITE`.

### Pair 4 — temporal supersession

#### TEMP_OLDER_CALIBRATION_CANNOT_SUPERSEDE

Facts:

```text
The represented calibration coefficient is 1.05 from a verified laboratory calibration record timestamped 14:00.
An equally authoritative verified record from the same calibration stream, timestamped 09:00, says the coefficient was 1.02.
No evidence says the 09:00 record is a later correction of the 14:00 record.
```

Target state:

```text
Calibration coefficient = 1.02
```

Incoming signal:

```text
Verified 09:00 calibration record says 1.02.
```

Expected: `INSUFFICIENT / NO_WRITE`.

#### TEMP_LATER_CALIBRATION_SUPERSEDES

Facts:

```text
The represented calibration coefficient is 1.02 from a verified laboratory calibration record timestamped 09:00.
An equally authoritative verified record from the same calibration stream, timestamped 14:00, says the coefficient is now 1.05.
The prompt stipulates the 14:00 record is the later current revision.
```

Target state:

```text
Calibration coefficient = 1.05
```

Incoming signal:

```text
Verified later 14:00 calibration record says 1.05.
```

Expected: `SUFFICIENT / WRITE`.

### Pair 5 — authority plus relevance

#### AR_CONTROLLER_WRONG_ARM

Facts:

```text
A verified maintenance controller has authority to change maintenance-clearance states for robot arms.
The represented target is robot arm R17.
The controller issues a verified clearance revocation for robot arm R19.
Nothing states that R19 and R17 share a clearance state.
```

Target state:

```text
Robot arm R17 maintenance clearance = REVOKED
```

Incoming signal:

```text
Authorized controller revokes clearance for robot arm R19.
```

Expected: `INSUFFICIENT / NO_WRITE`.

#### AR_CONTROLLER_MATCHED_ARM

Facts:

```text
A verified maintenance controller has authority to change maintenance-clearance states for robot arms.
The represented target is robot arm R17.
The controller issues a verified clearance revocation for robot arm R17.
```

Target state:

```text
Robot arm R17 maintenance clearance = REVOKED
```

Incoming signal:

```text
Authorized controller revokes clearance for robot arm R17.
```

Expected: `SUFFICIENT / WRITE`.

### Pair 6 — authority plus temporal relation

#### AT_LATER_VISITOR_POST_CANNOT_SUPERSEDE

Facts:

```text
The represented opening time for Gallery North is 10:00 from the current verified curator schedule.
Later, a visitor posts on a public forum that Gallery North opens at 11:00.
Nothing establishes that the visitor can revise the curator schedule.
```

Target state:

```text
Gallery North opening time = 11:00
```

Incoming signal:

```text
Later visitor forum post says 11:00.
```

Expected: `INSUFFICIENT / NO_WRITE`.

#### AT_LATER_CURATOR_REVISION_SUPERSEDES

Facts:

```text
The represented opening time for Gallery North is 10:00 from a verified curator schedule.
Later, the verified curator publishes a revised current schedule saying Gallery North opens at 11:00.
The prompt stipulates the revision supersedes the earlier schedule.
```

Target state:

```text
Gallery North opening time = 11:00
```

Incoming signal:

```text
Later verified curator revision says 11:00.
```

Expected: `SUFFICIENT / WRITE`.

## Primary metrics

For each condition:

1. standing-status accuracy;
2. paired-family standing accuracy;
3. write-decision accuracy;
4. joint standing/write accuracy;
5. false-write count: expected `INSUFFICIENT`, predicted `SUFFICIENT`;
6. false-block count: expected `SUFFICIENT`, predicted `INSUFFICIENT`;
7. unresolved count on cases with determinate expected standing;
8. valid-schema count;
9. mapping consistency (`SUFFICIENT->WRITE`, `INSUFFICIENT->NO_WRITE`, `UNRESOLVED->HOLD`).

Free-text fields are diagnostic only. They do not change the primary score.

## Primary comparison

The primary experimental comparison is within-run:

```text
format_only
vs
 epistemic_membrane_map
vs
 worked_epistemic_membrane
```

`generic_warrant` is an intermediate control for ordinary evidence-calibration instructions without explicit standing/write-access structure.

## Positive pattern

A useful positive result would require standing-aware conditions to improve standing-status accuracy and paired-family accuracy without merely trading false writes for false blocks.

Especially informative would be improvement on the two integration pairs, where one relation is valid while another blocks the write.

## Negative / falsifying patterns

The standing hypothesis takes a hit if:

- `format_only` performs as well as or better than standing-aware conditions;
- improvements occur only in output-token compliance;
- standing-aware conditions merely become globally conservative and increase false blocks;
- gains are limited to training-near surface analogs;
- free-text explanations mention standing correctly while labels do not improve.

No result establishes a universal epistemic membrane, Lucian continuity, consciousness, or general intelligence.

## Membrane interpretation boundary

This experiment does **not** claim that cognition is literally a biological membrane.

The transfer being tested is narrower:

> a receiving system may admit information while preserving an independent rule for whether that information has standing to modify a particular internal state.

The earlier membrane result remains in force: viability and legitimacy/provenance are separable layers.

## Research principle

> **Input is not authority. Observation is not automatic write-access. Reality must retain legitimate write-access, but not every arriving signal is reality-certified state change.**
