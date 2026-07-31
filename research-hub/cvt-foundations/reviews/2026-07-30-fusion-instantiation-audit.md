# CVT Foundations v0.2 — Fusion Instantiation Audit

**Date:** 2026-07-30  
**Status:** bounded scholarly review; no manuscript rewrite in this artifact  
**Canonical section audited:** `research-hub/cvt-foundations/main.tex`, `Fusion Instantiation: Hosted Burn`

## 1. Audit question

The present fusion section performs several different jobs at once:

1. it offers fusion as a vivid illustration of the difference between initiating a transition and hosting it;
2. it makes claims about burning-plasma physics and reactor subsystems;
3. it defines CVT-specific gates, receptivity, reserve, and pacing equations;
4. it reports numerical toy-model results;
5. it states a Minimum Viable Host theorem and a numerical reserve boundary.

These jobs do not carry the same evidentiary status. The audit asks what can remain in a general foundations paper, what must be rewritten as a bounded hypothesis, and what must move into a separate reproducible fusion-host research module.

## 2. Publication decision

### Decision

**Retain fusion in _CVT Foundations_ only as a short, source-anchored illustration of hosted transformation.**

The foundations paper may retain the following narrow claim:

> A transition toward alpha-dominated self-heating is not by itself a sufficient criterion for a viable fusion operating state. A declared reactor host must also remain within independently specified plasma, exhaust, material, particle-control, diagnostic, and control-authority constraints over a stated horizon.

This is not presented as a new result in fusion physics. The proposed CVT contribution is the explicit separation between:

- the transformation metric;
- the independently declared host-viability outcome;
- pre-existing host conditions proposed to predict whether the transition can be sustained.

### Move out of the foundations paper

The following material should leave `CVT Foundations`:

- the six-gate placental product score;
- the fusion receptivity product functional;
- the post-ignition throttle and alpha-pacing equations;
- the universal-looking rate inequality;
- all five numerical simulation-result subsections;
- the placental reserve sweep;
- the linear reserve curve;
- the Minimum Viable Host theorem;
- numerical thresholds and terminal values;
- claims that the toy simulations support CVT.

These may be preserved in a separate fusion-host model archive, but they should not return to a manuscript as results until code, parameters, units, initial conditions, numerical methods, sensitivity tests, and domain-native baselines are public and reproducible.

## 3. Primary physics baseline

The fusion illustration must be anchored to established fusion literature rather than introduced through CVT vocabulary alone.

### 3.1 Fusion performance and self-heating

Lawson's original power-balance analysis establishes that reactor relevance depends on more than temperature alone; confinement and duration enter the power-producing criterion. The ITER Physics Basis and its 2007 update provide the domain-native framework for projected burning-plasma performance, control, exhaust, and operational limits.

A burning plasma is commonly characterized by a substantial or dominant contribution of fusion-born alpha-particle heating. Zylstra et al. provide an experimental burning-plasma result in inertial confinement fusion. That source can support the general self-heating concept, but it cannot by itself support tokamak-specific claims about divertors, magnetic confinement, plasma-facing components, or steady-state control.

### 3.2 Host constraints already recognized by fusion physics

Power and particle exhaust, helium removal, fuelling, plasma-facing component loads, impurity transport, tritium retention, energetic-particle behavior, diagnostics, and control are established fusion research problems. CVT must not claim their discovery.

The defensible CVT question is narrower:

> Does explicitly separating transformation progress from independently measured host viability, capture readiness, and remaining control or recovery margin improve prediction or control beyond existing integrated fusion models?

## 4. Claim-by-claim disposition

| ID | Current claim or construction | Status | Decision |
|---|---|---|---|
| F1 | A burning plasma becomes increasingly self-heated by fusion-born alpha particles. | Established physical idea. | **Keep with primary sources.** Distinguish inertial and magnetic confinement evidence. |
| F2 | `chi_alpha = P_alpha/(P_alpha + P_aux)` measures the externally driven to alpha-dominated transition. | Author-defined diagnostic; algebraically meaningful, not established here as a universal ignition metric. | **Keep only if explicitly labeled a local diagnostic.** Do not equate it automatically with ignition or reactor success. |
| F3 | Ignition access is not hosted burn. | CVT interpretive distinction. | **Keep, but rewrite.** Use “transition to alpha-dominated self-heating” unless a domain-standard ignition criterion is specified. Define hosted success through independent fusion outcomes. |
| F4 | A fusion device is a coupled plasma-machine system involving fuelling, heat and particle exhaust, confinement, energetic particles, materials, diagnostics, and control. | Established systems description. | **Keep with ITER Physics Basis sources.** Do not present as CVT novelty. |
| F5 | The plasma-machine interface is a placental exchange organ. | Heuristic metaphor. | **Remove from the technical foundations core.** It may remain in a separate conceptual note if explicitly non-physical. |
| F6 | Total placental viability is the product of six normalized gates. | Unsupported modeling choice. | **Remove.** If revisited, compare product, minimum, soft-minimum, and direct constraints against the same independent outcome. |
| F7 | All relevant fusion exchange can be represented as `J_raw = Pi Delta`. | Over-generalized transport analogy across quantities with different units and mechanisms. | **Remove from fusion.** Define channel-specific power, particle, momentum, ash, or heat flows using domain-native equations. |
| F8 | Fusion receptivity equals a product of burn, machine, separation, restoration, spectral gates, and `(1-D)`. | Circular and double-counted under the repaired formal architecture. | **Remove.** Measure outcomes independently; estimate pre-existing readiness from non-overlapping observables. |
| F9 | Alpha dominance should obey the proposed host-gated pacing equation. | Uncalibrated toy-controller law. | **Move to the separate model module.** Compare with ordinary fusion-control baselines before any physical interpretation. |
| F10 | `d chi_alpha/dt <= R_host` is the formal version of pacing. | Dimensionally unsupported without a domain-specific derivation. | **Remove.** Any bound must have compatible units and follow from declared dynamics. |
| F11 | The reported controller simulations show that capacity maximization performs worst. | Internal toy-model output only; no reproducibility package. | **Remove from foundations.** Preserve as unverified historical output until reproduced. |
| F12 | Ablation confirms a real cascade cost and validates the mechanism map. | Overstated inference from a model constructed with those mechanisms. | **Remove.** Ablation can show dependence inside the chosen model, not physical reality or CVT validity. |
| F13 | Fixed alpha ramp produces “over-ignition.” | Model-specific interpretation using a nonstandard term. | **Remove from foundations.** The term may be explored only after mapping to domain-native failure modes. |
| F14 | A scalar placental reserve combines exhaust, materials, coolant, ash removal, diagnostics, control, magnetic margin, and inertia. | Heterogeneous composite with no validated normalization. | **Decompose.** Do not treat as one scalar reserve unless the aggregation is justified and tested. |
| F15 | `R_P,crit ≈ 6.25 + 5.5 Lambda_alpha` identifies a hosted-burn boundary. | Calibration-specific numerical artifact; units, code, parameters, and sensitivity absent. | **Remove from manuscript.** Preserve only in the reproducibility archive with provenance. |
| F16 | Minimum Viable Host is a theorem. | Not established. Threshold existence requires assumptions such as monotonicity, continuity, fixed policy, and a declared success set. | **Remove theorem status.** At most: model-specific estimated feasibility boundary. |
| F17 | The fusion instantiation supports the broader CVT claim. | Evidentiary overreach. | **Change to “illustrates.”** Support requires independent data or reproducible comparison against baselines. |
| F18 | The reactor becomes an artificial star when the host accepts the handoff. | Rhetorical metaphor. | **Remove from the technical argument.** It may remain outside the evidentiary chain. |

## 5. Repaired fusion vocabulary

The foundations illustration should separate four layers.

### 5.1 Domain-native observables

Potential observables include, depending on the selected operating scenario:

- fusion power and auxiliary heating power;
- fusion gain, written `Q_fus` to avoid collision with the CVT organization symbol `Q`;
- alpha-heating fraction or another explicitly defined self-heating diagnostic;
- energy-confinement time;
- plasma density and temperature profiles;
- divertor and first-wall heat loads;
- helium-ash concentration and exhaust performance;
- impurity concentration and radiative losses;
- plasma-facing component temperatures and damage proxies;
- magnetic, stability, actuator, and diagnostic margins;
- pulse duration and post-transition survival horizon.

No single list is universal. The operating scenario and declared host determine which observables are relevant.

### 5.2 CVT gate hypotheses

A bounded mapping could be investigated as follows:

- **bounded coupling `B`:** heating, fuelling, particle, momentum, and exhaust loads remain inside declared operating envelopes;
- **preserved organization `Q`:** the plasma configuration and machine functions required by the declared operating state remain intact;
- **capture readiness `C`:** the pre-transition plasma-machine state can accommodate the specified increase in self-heating or other input without leaving the declared viable set;
- **available restorative reserve `S`:** measurable actuator, exhaust, thermal, magnetic, diagnostic, or recovery headroom remains after the transition.

This mapping is provisional. Several engineering margins may not form one latent reserve variable. Some may be independent hard constraints rather than components of `S`.

### 5.3 Independent outcomes

The outcome must not be a CVT gate product. A hosted-burn illustration should declare a domain-native outcome vector or viable set before fitting CVT variables. It may include constraints on:

- self-heating or fusion-performance target;
- MHD and kinetic stability;
- heat and particle exhaust;
- plasma-facing component limits;
- helium and impurity control;
- diagnostic and actuator availability;
- duration and delayed post-transition integrity.

### 5.4 Candidate models

Only after observables and outcomes are independently defined should the study compare:

- direct simultaneous constraints;
- minimum-gate models;
- product or weighted geometric models;
- soft-minimum models;
- domain-native integrated control or transport models;
- hybrid models in which CVT variables add no duplicate information.

## 6. What should remain in CVT Foundations

The replacement fusion illustration should be short and contain no new numerical results. A suitable structure is:

1. **Why fusion is a scoped illustration.** A transition toward alpha-dominated self-heating occurs inside a machine whose continued viability is part of success.
2. **Transformation is not host viability.** Define a local self-heating diagnostic separately from the declared viable operating set.
3. **Domain-native host constraints.** Briefly cite confinement, exhaust, energetic particles, materials, diagnostics, and control.
4. **Provisional CVT mapping.** Present `B,Q,C,S` as hypotheses to be operationalized, not reactor variables already validated.
5. **Limits and falsifiers.** State that CVT adds value only if the decomposition improves out-of-sample prediction, control, or failure diagnosis beyond established fusion models.

Target length: approximately 1–2 manuscript pages.

## 7. Separate fusion-host research module

Create a new bounded project rather than letting the detailed model remain embedded in the foundations paper.

Proposed path:

`research-hub/fusion-host-model/`

Minimum contents:

- `README.md` — scope, non-claims, and relationship to CVT Foundations;
- `model.md` or `model.tex` — complete equations, units, assumptions, and variable provenance;
- `src/` — executable code;
- `configs/` — parameter sets and initial conditions;
- `tests/` — conservation, bounds, limiting cases, and regression tests;
- `results/` — machine-readable outputs rather than manuscript-only numbers;
- `sensitivity/` — parameter and structural sensitivity;
- `baselines/` — fixed-rate, standard feedback, and domain-native comparison controllers;
- `CITATION.cff` — software and model citation metadata.

A future fusion-host paper should not claim reactor-physics validation without calibrated domain equations, primary-source parameterization, and review by fusion-domain expertise.

## 8. Reproducibility requirements before numerical claims return

The existing numerical results are not presently auditable from the manuscript. Before any result is treated as evidence, the repository must include:

1. full equations and update order;
2. units or an explicit nondimensionalization;
3. parameter table and provenance;
4. initial and boundary conditions;
5. solver, step size, tolerances, and run horizon;
6. controller definitions;
7. random seeds, if any;
8. exact success and failure criteria;
9. raw output files;
10. parameter sensitivity and structural alternatives;
11. comparison with simpler models and domain-native baselines;
12. tests showing that conclusions do not follow tautologically from the definitions.

## 9. Counterexamples and falsification tests

The fusion illustration would constrain or falsify its CVT interpretation under any of the following results:

- a transition remains viable despite persistent failure of a proposed essential condition;
- a simpler fusion model predicts sustained operation and failure equally well or better with fewer variables;
- the proposed capture-readiness proxy is not measurable before the outcome or merely restates that outcome;
- the reserve construct adds no predictive value beyond established engineering margins;
- additive or compensatory models consistently outperform non-compensatory models;
- apparent hosted success disappears or appears solely through arbitrary normalization thresholds;
- conclusions reverse under reasonable parameter, timescale, or controller choices;
- equal total delivered input under different schedules produces no systematic viability difference after relevant state variables are controlled.

## 10. Source audit

Primary or foundational sources suitable for the next manuscript revision:

1. J. D. Lawson, “Some Criteria for a Power Producing Thermonuclear Reactor,” _Proceedings of the Physical Society, Section B_, vol. 70, pp. 6–10, 1957. doi:10.1088/0370-1301/70/1/303.
2. ITER Physics Basis Editors et al., “ITER Physics Basis, Chapter 1: Overview and Summary,” _Nuclear Fusion_, vol. 39, pp. 2137–2174, 1999. doi:10.1088/0029-5515/39/12/301.
3. M. Shimada et al., “Chapter 1: Overview and Summary,” _Nuclear Fusion_, vol. 47, pp. S1–S17, 2007. doi:10.1088/0029-5515/47/6/S01.
4. A. Loarte et al., “Chapter 4: Power and Particle Control,” _Nuclear Fusion_, vol. 47, pp. S203–S263, 2007. doi:10.1088/0029-5515/47/6/S04.
5. A. Fasoli et al., “Chapter 5: Physics of Energetic Ions,” _Nuclear Fusion_, vol. 47, pp. S264–S284, 2007. doi:10.1088/0029-5515/47/6/S05.
6. A. B. Zylstra et al., “Burning Plasma Achieved in Inertial Fusion,” _Nature_, vol. 601, pp. 542–548, 2022. doi:10.1038/s41586-021-04281-w.

The Zylstra paper is an inertial-fusion source. It should be used only for claims it actually supports, such as the experimental meaning of a self-heated burning-plasma regime, not for tokamak-specific machine claims.

## 11. Final audit judgment

The fusion section contains one strong and portable insight:

> Reaching a transformation criterion is not identical to sustaining that transformation inside a viable host.

That insight should remain.

The current fusion mathematics and numerical results do not yet carry evidentiary weight because they are uncalibrated, circular in places, inconsistent with the repaired formal architecture, and not reproducible from the repository. Removing them from the foundations paper does not weaken CVT. It prevents a vivid illustration from being mistaken for validation.

## 12. Authorized next manuscript action

After this audit is accepted, open a separate bounded rewrite branch that:

- replaces the current fusion section with the 1–2 page illustration described above;
- adds the primary fusion references;
- makes no numerical or theorem claims;
- preserves the removed detailed material in the future `fusion-host-model` archive rather than deleting its intellectual history;
- leaves the rest of `CVT Foundations` unchanged.
