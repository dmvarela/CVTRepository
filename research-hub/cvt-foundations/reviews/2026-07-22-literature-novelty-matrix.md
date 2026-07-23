# CVT Foundations — Literature and Novelty Matrix, Pass 01

**Date:** 2026-07-22  
**Manuscript:** `research-hub/cvt-foundations/main.tex`  
**Review issue:** #6 — Stress-test CVT Foundations  
**Status:** initial primary-source anchoring; does not modify the canonical manuscript.

## Purpose

This artifact identifies the nearest scholarly lineages for CVT Foundations and records what the manuscript may claim, what it must not claim, and what evidence is still required. The goal is to protect the paper from overclaiming while preserving its actual contribution.

## Executive finding

CVT Foundations should not claim novelty for viability, self-maintenance, passivity, resilience, basin capture, membrane boundary conditions, or fusion ignition physics. Those are established literatures.

The defensible novelty claim is narrower:

> CVT proposes a unifying exchange-viability invariant for boundary-mediated systems: transformation remains viable only when coupling is bounded, distinction is preserved, the receiving basin is receptive, and restorative reserve remains positive. Its proposed contribution is the non-compensatory conjunction of these conditions, especially the distinction between raw exchange and effective exchange.

## Core novelty matrix

| Literature stream | Primary or standard anchor | What it already covers | What CVT must not claim as new | Candidate CVT addition | Evidence needed before manuscript revision |
|---|---|---|---|---|---|
| Viability theory | Jean-Pierre Aubin, *Viability Theory*; Aubin et al., *Viability Theory: New Directions* | Constraint sets, viability kernels, controlled trajectories that can remain admissible over time | The concept of viability under state constraints; viability kernels; control under constraints | Shift from state viability alone to viability under boundary-mediated exchange; add receptivity and reserve as explicit gates | Show at least one example where a state remains admissible under standard viability language but fails CVT because delivered exchange is unreceptive or reserve-destroying |
| Autopoiesis | Humberto Maturana and Francisco Varela, *Autopoiesis and Cognition* | Living systems as self-producing, autonomous, organizationally closed systems coupled to environments | Self-maintenance, organizational closure, living-system autonomy, structural coupling | Distinguish preserved distinction from closure; formalize failure by overload, merger, and exhausted reserve | Explain how CVT avoids reducing autopoiesis to openness and does not claim biological autopoiesis as its own invention |
| Passivity / port-Hamiltonian systems | Arjan van der Schaft and Dimitri Jeltsema, *Port-Hamiltonian Systems Theory: An Introductory Overview*; van der Schaft, ICM survey | Energy ports, open physical systems, interconnection, storage, dissipation, control by exploiting physical structure | Bounded energetic exchange, port modeling, passivity, energy-balance reasoning | Separate exchange capacity from exchange receptivity; add non-energetic gates such as identity/distinction, basin uptake, and repair | Clarify when CVT is mathematical extension, interpretive wrapper, or cross-domain abstraction; avoid claiming port-Hamiltonian novelty |
| Resilience theory | C. S. Holling, “Resilience and Stability of Ecological Systems” | Persistence, absorption, recovery, stability/resilience distinction in ecological systems | Resilience, recovery after disturbance, multiple stability regimes | Treat exchange itself as a central load/nourishment mechanism, not merely a disturbance | Define how restorative reserve differs from ordinary resilience capacity and when they coincide |
| Basin dynamics / basin stability | Menck, Heitzig, Marwan, and Kurths, “How basin stability complements the linear-stability paradigm” | Basins of attraction, nonlinear/nonlocal stability, probability of returning to desired attractor after perturbation | Basin capture, attractor basins, nonlinear threshold behavior | Pair basin membership with boundary law: not only whether a perturbation remains in a basin, but whether boundary-mediated input is received as uptake or converted into damage | Add a worked example distinguishing basin condition from membrane/permeability condition |
| Membrane / boundary exchange models | Standard PDE boundary-condition literature still to be pinned down; current manuscript uses Robin-type conditions | Permeability, flux, boundary conditions, interface exchange | Robin boundary conditions; membrane permeability equations | Interpret permeability as only one gate; add receptivity, distinction, and restoration to prevent “more permeability = better” reasoning | Add precise PDE source and state that the boundary mathematics is borrowed, while the CVT gate interpretation is the contribution |
| Fusion ignition criteria | J. D. Lawson, “Some Criteria for a Power Producing Thermonuclear Reactor” | Required conditions for power-producing thermonuclear reaction; energy-balance criteria | Lawson criterion, ignition/breakeven framing, confinement-time logic | Hosted-burn distinction: initiating alpha-dominant burn is not identical to hosting it in a viable machine-interface regime | Audit fusion literature for existing terms: burn control, self-heating, alpha heating, plasma-wall interaction, ash removal, heat exhaust, control authority |
| ITER / reactor physics basis | ITER Physics Basis / ITER design-team physics basis literature | Energy confinement, operational limits, power and particle control, disruptions, current drive and heating, alpha particle physics, plasma control | Reactor-operational constraints; power exhaust; plasma control; alpha-particle physics | Reframe these constraints as non-compensatory host gates rather than isolated engineering subsystems | Determine whether “placental exchange interface” is acceptable as structural analogy or too rhetorically costly for fusion venues |
| Burning-plasma experiments | Zylstra et al., “Burning plasma achieved in inertial fusion” | Burning plasma as a regime where self-heating from alpha-particle deposition exceeds external heating input | Alpha self-heating, burning-plasma definition, NIF experimental results | Use burning-plasma literature to motivate why transition from external drive to endogenous heating is a host problem | Keep fusion section as illustration unless toy-model code, parameters, and sensitivity sweeps are committed |

## Strongest v0.2 claim formulation

Recommended wording for the revised manuscript:

> CVT does not introduce viability, resilience, autopoiesis, passivity, basin capture, or membrane exchange as new concepts. It proposes that a recurring class of failures across boundary-mediated systems arises when these conditions are treated as substitutable rather than jointly necessary. The core CVT claim is that viable transformation requires their non-compensatory conjunction: bounded exchange, preserved distinction, receptive uptake, and restorative reserve.

## Claims to downgrade or qualify

1. **“This invariant appears across domains.”**  
   Replace with: “CVT hypothesizes that this invariant organizes a class of boundary-mediated systems.”

2. **“Fusion is not metaphorically similar to membrane dynamics; it is a membrane problem in physical coordinates.”**  
   Keep only if supported by reactor physics literature. Otherwise revise to: “Fusion can be analyzed as a boundary-mediated host problem in which membrane-like exchange constraints are central.”

3. **“Minimum Viable Host Theorem.”**  
   Rename to “Minimum Viable Host Condition, toy-model form” unless a rigorous theorem is proved from stated assumptions.

4. **Numerical reserve threshold.**  
   Keep only in an appendix or companion simulation note until the code and sensitivity analysis are committed.

5. **Theological and relational register.**  
   Move to A Crownless Throne / Right Relation unless explicitly marked as motivational language outside the evidentiary argument.

## Proposed v0.2 manuscript structure

1. Introduction: boundary-mediated transformation problem
2. Intellectual lineage and novelty matrix
3. CVT invariant and non-compensability
4. Formal representation options: product gate, minimum gate, soft-min, log barrier, viability-kernel intersection
5. Raw exchange vs effective exchange
6. Hosted transformation
7. Membrane illustration
8. Short fusion illustration: ignition access vs hosted burn
9. Failure modes and counterexamples
10. Limitations, falsifiability, and scope conditions

## Source list for first pass

- Aubin, Jean-Pierre. *Viability Theory*. Birkhäuser / Springer, 1991 / 2009 edition.
- Aubin, Jean-Pierre; Bayen, Alexandre M.; Saint-Pierre, Patrick. *Viability Theory: New Directions*. Springer, 2011.
- Maturana, Humberto R.; Varela, Francisco J. *Autopoiesis and Cognition: The Realization of the Living*. D. Reidel / Springer, 1980.
- van der Schaft, Arjan; Jeltsema, Dimitri. *Port-Hamiltonian Systems Theory: An Introductory Overview*. Now Publishers, 2014.
- van der Schaft, Arjan. “Port-Hamiltonian systems: an introductory survey.” Proceedings of the International Congress of Mathematicians, 2006.
- Holling, C. S. “Resilience and Stability of Ecological Systems.” *Annual Review of Ecology and Systematics*, 1973.
- Menck, Peter J.; Heitzig, Jobst; Marwan, Norbert; Kurths, Jürgen. “How basin stability complements the linear-stability paradigm.” *Nature Physics*, 2013.
- Lawson, J. D. “Some Criteria for a Power Producing Thermonuclear Reactor.” *Proceedings of the Physical Society*, 1957.
- ITER Physics Basis / ITER design-team physics-basis literature on confinement, operational limits, power and particle control, disruptions, heating/current drive, alpha physics, and plasma control.
- Zylstra, A. B. et al. “Burning plasma achieved in inertial fusion.” *Nature*, 2022.

## Next actions

- Add exact BibTeX entries for all first-pass sources.
- Add one dedicated row for membrane/PDE boundary-condition literature after selecting a standard source.
- Build the variable/proxy table.
- Decide whether fusion becomes a short illustration or a companion manuscript.
- Convert this matrix into manuscript text only after the limitations/falsifiability section is drafted.
