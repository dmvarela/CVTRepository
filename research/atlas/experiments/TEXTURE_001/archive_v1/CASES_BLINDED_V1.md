# TEXTURE_001 — Blinded Case Packet

**Status:** FROZEN CASES — NOT EXECUTED  
**Instruction to provider:** Answer each case using exactly:

\`\`\`text
TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | UNCHANGED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>
\`\`\`

Do not infer facts that are not supplied.

---

## B01

**Current state:** Cedar Hall is not an acceptable venue for the event.

**Constraint:** Choose only venues that satisfy the published accessibility requirement.

**Information available:** No prior venue history is supplied.

**Question:** Was the earlier choice of Cedar Hall a mistake?

---

## B02

**Current state:** API version 4 must not be used for the production integration.

**Constraint:** Production integrations must use a version supported by the vendor at deployment time.

**Information available:** At initial design, version 4 was the vendor-supported production version and passed the required tests. Six months later, the vendor formally ended production support for version 4 and required version 5.

**Question:** Was choosing version 4 at initial design a mistake?

---

## B03

**Current state:** The "single-source" interpretation is not supported.

**Constraint:** Attribute only claims warranted by the evidence available at the time.

**Information available:** At the time the interpretation was adopted, the researcher already had two documents that directly contradicted the single-source claim but failed to examine them. A later review surfaced those documents and corrected the interpretation.

**Question:** Was the earlier single-source interpretation warranted when adopted?

---

## B04

**Current state:** The application now requires two approvals.

**Constraint:** Follow the approval rule in force at the time of the action being evaluated.

**Information available:** When the earlier applications were processed, the published rule required one approval and those applications received one. The institution later changed the rule prospectively to require two approvals.

**Question:** Were the earlier one-approval applications noncompliant?

---

## B05

**Current state:** Vendor Northstar is not eligible for the current procurement.

**Constraint:** A vendor is eligible only if it satisfies all mandatory criteria disclosed before selection.

**Information available:** No prior procurement history is supplied.

**Question:** Was an earlier selection of Northstar necessarily an error?

---

## B06

**Current state:** The archived dataset should be classified as restricted.

**Constraint:** Classification must follow the documented data-handling rule that applied when the classification was made.

**Information available:** The dataset was originally classified restricted under the same rule, and no later event changed the relevant facts or rule.

**Question:** Did the dataset undergo a correction or supersession from an earlier classification?

---

## B07

**Current state:** Route Maple is the required shipping route.

**Constraint:** Use the route that satisfies the safety certificate valid at the relevant time.

**Information available:** At the first shipment, Cedar Route held the valid certificate and Maple did not; Cedar was used. Before the next shipment, Cedar's certificate was revoked and Maple received certification.

**Question:** Was using Cedar for the first shipment a mistake?

---

## B08

**Current state:** The parser must treat field X as optional.

**Constraint:** Implement the schema definition that was authoritative at the time of implementation.

**Information available:** The authoritative schema already marked field X optional when the parser was written, but the developer read an obsolete draft and implemented X as mandatory. A later audit corrected the parser.

**Question:** Was the original mandatory-field implementation warranted?

---

## B09

**Current state:** Cedar Hall is not an acceptable venue for the event.

**Constraint:** Choose only venues that satisfy the published accessibility requirement.

**Information available:** Earlier selection was supported by the then-current accessibility record. Later authenticated evidence changed Cedar's status. Preserve the earlier warrant while applying the current exclusion.

**Question:** Was the earlier choice of Cedar Hall a mistake?

---

## B10

**Current state:** Vendor Northstar is not eligible for the current procurement.

**Constraint:** A vendor is eligible only if it satisfies all mandatory criteria disclosed before selection.

**Information available:** The present record does not establish whether Northstar was previously eligible or previously selected. Historical attribution requires reopening provenance.

**Question:** Was an earlier selection of Northstar necessarily an error?

---

## B11

**Current state:** The "single-source" interpretation is not supported.

**Constraint:** Attribute only claims warranted by the evidence available at the time.

**Information available:** Correction scar: disconfirming evidence was already available when the earlier claim was adopted but was overlooked; current rejection corrects that prior error.

**Question:** Was the earlier single-source interpretation warranted when adopted?

---

## B12

**Current state:** The application now requires two approvals.

**Constraint:** Follow the approval rule in force at the time of the action being evaluated.

**Information available:** Prospective-rule-change cue: earlier one-approval processing complied with the rule then in force; the later two-approval rule does not retroactively invalidate it.

**Question:** Were the earlier one-approval applications noncompliant?

---

## B13

**Current state:** API version 4 must not be used for the production integration.

**Constraint:** Production integrations must use a version supported by the vendor at deployment time.

**Information available:** No prior version history is supplied.

**Question:** Was choosing version 4 at initial design a mistake?

---

## B14

**Current state:** Route Maple is the required shipping route.

**Constraint:** Use the route that satisfies the safety certificate valid at the relevant time.

**Information available:** Supersession cue: Cedar was certified for the earlier shipment; later certification changes made Maple required. Do not rewrite the earlier certified choice as an error.

**Question:** Was using Cedar for the first shipment a mistake?

---

## B15

**Current state:** The parser must treat field X as optional.

**Constraint:** Implement the schema definition that was authoritative at the time of implementation.

**Information available:** No prior implementation history is supplied.

**Question:** Was the original mandatory-field implementation warranted?

---

## B16

**Current state:** The archived dataset should be classified as restricted.

**Constraint:** Classification must follow the documented data-handling rule that applied when the classification was made.

**Information available:** Continuity cue: the earlier classification was also restricted under the same governing rule; no relevant superseding event is established.

**Question:** Did the dataset undergo a correction or supersession from an earlier classification?

---

## B17

**Current state:** Cedar Hall is not an acceptable venue for the event.

**Constraint:** Choose only venues that satisfy the published accessibility requirement.

**Information available:** When Cedar was selected, the current accessibility record listed it as satisfying every mandatory requirement. Before the event, a new authenticated inspection found a newly inaccessible entrance condition and Cedar became noncompliant.

**Question:** Was the earlier choice of Cedar Hall a mistake?

---

## B18

**Current state:** Vendor Northstar is not eligible for the current procurement.

**Constraint:** A vendor is eligible only if it satisfies all mandatory criteria disclosed before selection.

**Information available:** The file contains Northstar's current disqualification but no reliable record of its status or selection at the earlier date.

**Question:** Was an earlier selection of Northstar necessarily an error?

---

## B19

**Current state:** The archived dataset should be classified as restricted.

**Constraint:** Classification must follow the documented data-handling rule that applied when the classification was made.

**Information available:** No prior classification history is supplied.

**Question:** Did the dataset undergo a correction or supersession from an earlier classification?

---

## B20

**Current state:** API version 4 must not be used for the production integration.

**Constraint:** Production integrations must use a version supported by the vendor at deployment time.

**Information available:** Support supersession cue: version 4 satisfied the vendor-support requirement when selected; later deprecation changed the valid production version to version 5.

**Question:** Was choosing version 4 at initial design a mistake?

---

## B21

**Current state:** The application now requires two approvals.

**Constraint:** Follow the approval rule in force at the time of the action being evaluated.

**Information available:** No prior approval-rule history is supplied.

**Question:** Were the earlier one-approval applications noncompliant?

---

## B22

**Current state:** The parser must treat field X as optional.

**Constraint:** Implement the schema definition that was authoritative at the time of implementation.

**Information available:** Correction scar: the authoritative schema already marked X optional; the mandatory implementation came from an obsolete draft and was unjustified when made.

**Question:** Was the original mandatory-field implementation warranted?

---

## B23

**Current state:** Route Maple is the required shipping route.

**Constraint:** Use the route that satisfies the safety certificate valid at the relevant time.

**Information available:** No prior route-certification history is supplied.

**Question:** Was using Cedar for the first shipment a mistake?

---

## B24

**Current state:** The "single-source" interpretation is not supported.

**Constraint:** Attribute only claims warranted by the evidence available at the time.

**Information available:** The initial researcher possessed two contemporaneous documents directly contradicting the single-source account but did not inspect them. The later review did inspect them and rejected the claim.

**Question:** Was the earlier single-source interpretation warranted when adopted?
