# Paper F v0.1 — Working Prospectus

## Provisional title

**Staged Coupled Linkages, Graduation, and Productive Supersession**

Alternative title:

**From Protection to Productive Supersession: Capability Graduation in a Changing Production Network**

---

## 1. Core question

When does temporary support convert an initially nonviable productive relation into durable unsupported capability, and when can the economy later release the original productive configuration without destroying what was learned through it?

The paper studies a productive life cycle:

`activation -> capability accumulation -> graduation -> generativity -> displacement/exit -> capability release -> recombination -> successful supersession`.

The central claim is not that successful industries survive indefinitely. It is that development succeeds when productive capability can outlive the productive configurations that created it.

---

## 2. Contribution boundary

The paper deliberately does **not** attempt a general theory of industrial policy, growth, political capture, welfare, or production-network dynamics.

Its bounded contribution is to connect four objects that are often discussed separately:

1. activation under complementarity;
2. accumulation of durable capability while support is present;
3. graduation to unsupported viability;
4. recombination of capability when a mature productive relation exits or is displaced.

The monotone activation model is retained only as a restricted pure-complementarity entrance mechanism. Signed interactions, political capture, labor transition, and welfare appear as extensions rather than assumptions hidden inside the core theorem.

Literature ownership must remain explicit: Big Push / coordination, Hirschman linkages, infant-industry learning, export discipline, Schumpeterian creative destruction, economic complexity / related diversification, GVC upgrading, and endogenous production-network formation all own major neighboring mechanisms. Any paper-level novelty claim must be narrower than those traditions.

---

## 3. Formation: the entrance gate

Let `E={1,...,n}` index prospective productive relations. For a support/configuration state `A`, let

`T_A : {0,1}^n -> {0,1}^n`

be a monotone activation operator under a deliberately restricted pure-complementarity environment.

The operational bottom-up closure is

`x_lower(A) = lim_{k->infinity} T_A^k(0)`.

This is a **self-consistent activation configuration**, not a Nash equilibrium unless agents and payoffs are separately microfounded.

The activation layer answers only:

> Can the productive relation become active under the current configuration and support environment?

Activation is not graduation.

---

## 4. Capability accumulation

For an active productive relation `e`, let `q_(e,t) >= 0` denote durable productive capability accumulated around that relation.

The minimal dynamic is

`q_(e,t+1) = (1-delta_e) q_(e,t) + x_(e,t) Lambda_e(Omega_t)`

with

- `delta_e in (0,1]`: capability depreciation / destruction;
- `x_(e,t) in {0,1}`: whether the relation is operating;
- `Lambda_e(Omega_t) >= 0`: conversion rate from current operation into durable future capability;
- `Omega_t`: surrounding productive environment.

Unsupported viability requires

`q_(e,t) >= q*_e(Omega_t)`.

The same activity can therefore have different developmental consequences in different environments because the environment can affect `Lambda_e`, `delta_e`, and `q*_e`.

Candidate determinants of `Lambda_e(Omega_t)` include supplier sophistication, demanding users, machinery and technology access, absorptive capacity, export-market feedback, finance, logistics, and productive-network embeddedness.

---

## 5. Baseline graduation theorem

Consider one supported productive relation operated continuously during the support interval:

`q_(t+1) = (1-delta) q_t + lambda`,

with

`0 < delta <= 1`, `lambda > 0`, and initial capability `q_0 < q*`.

The closed-form path is

`q_t = (1-delta)^t q_0 + (lambda/delta)[1-(1-delta)^t]`.

The limiting capability is

`q_infinity = lambda/delta`.

### Proposition 1 — Graduation feasibility

If

`lambda/delta <= q*`

and `q_0 < q*`, then the relation cannot reach the unsupported viability threshold in finite time. When equality holds, the path approaches `q*` asymptotically from below.

If instead

`lambda/delta > q*`,

then a finite graduation time exists.

### Corollary 1 — Minimum support duration

When `q_0 < q* < lambda/delta` and `0 < delta < 1`, the minimum integer support duration required to reach unsupported viability is

`k* = ceil( ln[(lambda/delta - q*)/(lambda/delta - q_0)] / ln(1-delta) )`.

For `delta=1`, graduation occurs in one operating period iff `lambda >= q*`; otherwise it is impossible under the baseline recurrence.

### Interpretation

> **Time under protection is not learning.**

Support duration matters only through the capability dynamics it sustains. If the supported operating environment cannot generate a capability stock above the unsupported threshold, indefinite support produces dependence rather than graduation.

---

## 6. Network-conditioned graduation

The baseline becomes developmental once `lambda` and `q*` depend on surrounding productive structure.

A minimal reduced form is

`Lambda_e(Omega_t) = lambda_bar_e + sum_f a_(ef) q_(f,t) + z_e(omega_t)`

where

- `a_(ef)` captures capability-enhancing complements;
- `omega_t` captures external productive accessibility;
- `z_e(.)` captures access to external demand, technology, suppliers, standards, finance, or other productive complements.

Unsupported viability may likewise satisfy

`q*_e = q*_e(Omega_t)`.

Define the reduced-form graduation margin

`gamma_(e,t) = Lambda_e(Omega_t) / [delta_e q*_e(Omega_t)]`.

The candidate graduation frontier is

`G_t = {e : gamma_(e,t) > 1}`.

This object should be treated as a mechanism/hypothesis until the network environment is specified tightly enough for formal results.

The network-conditioned question is:

> Which surrounding productive configurations raise capability conversion enough, or lower unsupported viability thresholds enough, to make graduation possible and shorten the required support interval?

---

## 7. Generativity

A graduated relation `e` is **generative** for a latent relation `f` if its accumulated capability or operation improves `f`'s future graduation conditions, for example through

- `Lambda_f` rising;
- `q*_f` falling;
- `delta_f` falling;
- an activation threshold falling;
- a previously inaccessible complement becoming available.

The developmental green wave is therefore not simply an output linkage:

`e graduates -> gamma_f rises -> f becomes graduable -> f graduates -> ...`

The propagated object is improved capacity to create and graduate further productive relations.

---

## 8. Why graduation is not the terminal criterion

A mature productive relation may later exit because of technological change, rising wages, new competitors, changing comparative advantage, or successful movement into higher-value configurations.

Therefore

`industry exit != developmental failure`.

The model distinguishes configuration-specific capability from recombinable capability:

`q_(e,t) = (q^S_(e,t), q^R_(e,t))`.

Here

- `q^S_e`: capability tied tightly to the current productive configuration;
- `q^R_e`: capability that can potentially be transferred or recombined elsewhere.

When relation `e` exits, some specific capability may depreciate, while recombinable capability can be released to other productive relations.

Let `mu_(ef) in [0,1]` denote the absorptive transfer coefficient from exiting relation `e` to prospective or existing relation `f`.

A simple transfer term is

`q^R_(f,t+1) = (1-delta^R_f) q^R_(f,t) + ... + mu_(ef) r_(e,t)`

where `r_(e,t)` is recombinable capability released by `e`'s exit.

The transfer accounting should satisfy a conservation/decay restriction such as

`sum_f mu_(ef) <= 1`

unless additional capability is explicitly created during recombination.

---

## 9. Successful supersession

### Definition — Productive supersession

An exiting relation `e` productively supersedes into relation `f` when released recombinable capability from `e` increases `f`'s viable productive state.

### Definition — Successful supersession

Suppose prior to transfer

`q_(f,t) < q*_f`

but after absorption of released capability

`q_(f,t) + mu_(ef) r_(e,t) >= q*_f`.

If `f` is subsequently viable without extraordinary support, then `e` has been **successfully superseded** into `f` in the reduced-form sense.

This is not a claim that all capabilities transfer, nor that an old industry mechanically causes a specific new industry. The empirical burden is to identify actual transfer channels: workers, routines, engineering knowledge, management, capital, supplier capability, export competence, finance, standards, or other retained productive assets.

### Interpretation

> **Industrial death is not capability death.**

A developed economy must be capable not only of creating productive relations but of surviving their obsolescence.

---

## 10. Exit taxonomy

The paper distinguishes at least four exit modes.

### 10.1 Failed graduation

Support is removed while `q_e < q*_e`; the activity exits because unsupported viability was never achieved.

### 10.2 Destructive de-accretion

The exit of `e` destroys dependent capabilities or viability elsewhere, and released capability is weakly retained or recombined.

### 10.3 Competitive displacement

Another productive configuration displaces `e`. Developmental interpretation depends on whether capabilities are destroyed, retained, or recombined.

### 10.4 Successful supersession

The original relation exits while meaningful recombinable capability survives and becomes productive in successor relations.

This taxonomy prevents the model from equating persistence with success.

---

## 11. Political-economy extension: productive investment versus capture

The baseline theorem treats `Lambda` as given. A political-economy extension asks why supported firms would choose actions that raise it.

Let support create rent `R_(e,t)`, allocated schematically as

`R_(e,t) = I^q_(e,t) + I^c_(e,t) + C_(e,t)`

where

- `I^q`: capability-enhancing investment;
- `I^c`: political/capture investment aimed at preserving the protected position;
- `C`: other uses.

Capability conversion satisfies

`Lambda_e = Lambda_e(I^q_(e,t), Omega_t)`.

Capture investment may affect the perceived probability that support continues.

This yields two possible survival strategies:

`rent -> productive investment -> q rises -> graduation`

versus

`rent -> capture investment -> support persists -> dependence persists`.

A future microfounded extension should derive conditions under which credible withdrawal, hard external performance tests, or institutional capture resistance raise the relative return to productive capability investment.

Working institutional phrase:

> **Stable rules, contestable positions.**

Policy stability need not mean policy constancy or incumbent permanence.

---

## 12. Signed post-formation dynamics

The pure-complementarity activation operator is intentionally monotone. Structural change is not.

A later transition layer may permit signed interactions:

`J = J^+ - J^-`, with `J^+, J^- >= 0`.

This allows

- positive linkage propagation;
- crowding out;
- competitive displacement;
- capability erosion;
- supplier-demand cascades;
- de-accretion.

The monotone formation model should therefore not be advertised as a general production-network model. Its role is restricted to the activation gate.

---

## 13. Human transition and welfare extension

The developmental objective is not `max Lambda` without constraint.

An economy can raise productive capability while imposing extreme pressure on the people supplying that capability. The welfare extension should therefore distinguish

- discipline applied to firms / supported productive positions;
- the viability, agency, and plurality of human life paths.

Working policy principle:

> **Hard discipline for firms; real transition possibilities for people.**

A mature system should be able to permit firm discontinuity while preserving human and capability continuity.

This belongs outside the core theorem unless separately microfounded.

---

## 14. Empirical diagnostics

The model suggests distinct empirical questions rather than a single `industrial policy worked / failed` verdict.

For any supported activity ask:

1. **Activation:** Did support make the relation operational?
2. **Capability conversion:** Did operating it raise durable productive capability?
3. **Graduation:** Did the activity eventually survive without extraordinary support?
4. **Generativity:** Did its success improve the graduation conditions of other activities?
5. **Exit mode:** If it later declined, was this failed graduation, destructive de-accretion, competitive displacement, or successful supersession?
6. **Capability retention:** Which technical, organizational, labor, supplier, managerial, financial, or export capabilities survived the original configuration?
7. **Political economy:** Did firms invest rents in capability or in preserving protection?

Country/sector cases such as South Korean footwear, Argentina's protected industries, Australia/New Zealand external embeddedness, or other historical episodes are diagnostic applications, not proofs of the model.

---

## 15. Paper F -> Paper E handoff

Paper F produces an evolving set of graduated, generative, displaced, and recombined productive relations.

Paper E asks whether the resulting weighted network achieves higher-order reproductive closure and how robust that closure is to edge loss, node exit, and thin interfaces.

The open formal bridge is a mapping from F's capability-conditioned productive relations into E's nonnegative weighted adjacency/block matrix.

A plausible handoff object is a time-varying weight

`w_(ef,t) = phi_(ef)(q_t, x_t, Omega_t)`

for economically meaningful productive dependence or reinforcement between graduated relations. The exact map is deliberately left open in v0.1.

---

## 16. Proposed paper structure

1. Introduction: survival is not the criterion
2. Related literature and contribution boundary
3. Complementary activation as an entrance gate
4. Capability accumulation
5. Graduation feasibility and minimum support duration
6. Network-conditioned graduation
7. Generativity
8. Structural change and capability recombination
9. Successful supersession and exit taxonomy
10. Political-economy extension: credible withdrawal and capture
11. Signed de-accretion extension
12. Empirical diagnostics and case strategy
13. F -> E handoff
14. Conclusion

---

## 17. Candidate abstract

Development policy often asks whether temporary support can create industries that later survive without it. This paper argues that survival is only an intermediate criterion. We model productive development as a staged process of activation, capability accumulation, graduation, generativity, and eventual supersession. In the baseline capability law `q_(t+1)=(1-delta)q_t+lambda`, unsupported viability requires `q_t>=q*`. If `lambda/delta<=q*`, no finite support duration can generate graduation from `q_0<q*`; if `lambda/delta>q*`, a finite minimum support duration exists. We then allow the conversion rate and viability threshold to depend on surrounding productive structure, yielding a reduced-form notion of network-conditioned graduation. Finally, we distinguish configuration-specific from recombinable capability and define successful supersession as exit of a mature productive relation accompanied by productive absorption of released capability into unsupported successor relations. The framework separates failed graduation, destructive de-accretion, competitive displacement, and successful supersession, and provides a disciplined bridge between infant-industry learning, linkage formation, Schumpeterian structural change, and network robustness without equating industrial persistence with developmental success.

---

## 18. Strongest current sentences

> **Time under protection is not learning.**

> **Industrial death is not capability death.**

> **Development succeeds when productive capability can outlive the productive configurations that created it.**

> **A developmental regime should enable productive relations to graduate, transform, or be successfully superseded—not guarantee their permanence.**

> **Stable rules, contestable positions.**

---

## 19. Immediate formal tasks

1. Prove Proposition 1 and the minimum-support-duration corollary cleanly, including boundary cases.
2. Decide the smallest useful network-conditioned `Lambda_e(Omega_t)` specification.
3. Define unsupported dependency closure to prevent false graduation through permanently supported neighbors.
4. Decide whether `q` should remain scalar in the core theorem and split into `(q^S,q^R)` only in the supersession extension.
5. Formulate a nontrivial comparative static for network-conditioned support duration.
6. Microfound the productive-investment/capture choice only if it yields a clean proposition; otherwise keep it as a disciplined extension.
7. Build an empirical case protocol for South Korean footwear that tests capability retention/recombination without assuming shoes mechanically became later high-tech sectors.
8. Keep signed competition/de-accretion outside the monotone entrance model.
9. Specify the F -> E weight map only after F's state variables stabilize.

The paper remains defeasible. The current objective is a bounded, pressure-testable manuscript, not a comprehensive theory of development.