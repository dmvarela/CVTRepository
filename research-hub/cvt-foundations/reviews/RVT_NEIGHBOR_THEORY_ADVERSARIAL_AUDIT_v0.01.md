# RVT Neighbor-Theory Adversarial Audit v0.01

**Status:** adversarial literature-positioning audit / working review  
**Date:** 2026-09-14  
**Project:** Relation Viability Theory (RVT)  
**Purpose:** identify which parts of `rvt-candidate-theory-v0.01.md` are already supplied by established neighboring theories, which claims must be abandoned as novelty claims, and what—if anything—survives as a specifically RVT contribution.

---

## 1. Audit rule

This note is deliberately hostile to novelty claims.

For every neighboring literature, ask:

1. What does it already explain that RVT has been treating as important?
2. Which RVT sentences become non-novel once that literature is taken seriously?
3. Can RVT be represented as an ordinary model inside the neighboring framework?
4. If yes, what added causal decomposition, diagnostic, prediction, intervention, or control value remains?
5. What would make the RVT machinery redundant?

The governing rule is:

> **Do not protect the name RVT. Protect the map.**

A useful result of this audit may be that RVT is best understood as a problem class, synthesis, causal decomposition, or diagnostic framework rather than a new branch of mathematics.

---

## 2. Current RVT claim under audit

The current candidate core is:

> **RVT studies how structured exchange among differentiated systems reshapes the conditions of future viable exchange and action.**

with the schematic mechanism:

\[
\boxed{
R_t
\rightarrow
e_t
\rightarrow
(X_{t+1},H_{t+1})
\rightarrow
R_{t+1}
\rightarrow
\mathfrak V_{t+1}^T
}
\]

where:

- \(X_t\): constituent state;
- \(R_t\): relational/exchange architecture;
- \(H_t\): retained history relevant to future dynamics;
- \(e_t\): realized exchange;
- \(\mathfrak V_t^T\): future viability structure over a declared horizon and control set.

The strongest RVT sentence is currently:

> **The relation does not merely move the system through the landscape; it can alter the landscape through which later action occurs.**

This audit asks whether that sentence is actually new.

Preliminary answer: **not by itself.** Several mature literatures already contain close versions of it.

---

# 3. Neighbor 1 — Classical viability theory and controlled invariance

## What this literature already has

Aubin's viability theory studies dynamical systems under state constraints, including viability kernels, capture/connection basins, state-dependent control constraints, regulation, restoration of viability, robustness, and hysteresis-like problems.

The viability kernel already asks:

\[
\text{From which states does there exist an admissible evolution that remains inside }K?
\]

Modern viability work also supports robustness measures and augmented-state formulations. Therefore RVT cannot claim novelty merely from using:

- viability constraints;
- viability kernels;
- capture basins;
- recovery/restoration;
- state-dependent controls;
- finite-horizon viable reachability;
- robustness margins;
- augmentation of state by memory/history.

## Direct threat to RVT

The strongest mathematical threat is simple:

\[
Z_t=(X_t,R_t,H_t,\theta_t)
\]

can be treated as an ordinary augmented state.

Then a generic RVT model may simply become:

\[
Z_{t+1}=F(Z_t,u_t,\xi_t)
\]

with constraints and controls analyzed by standard viability machinery.

If this representation loses nothing important, RVT has **not** introduced new mathematics.

Likewise, the claim

> history changes future viability

is not enough: one can place history in the state.

## What may survive

Potential RVT contribution is not the kernel itself but the **causal decomposition of the augmented state**:

\[
\text{constituents}\;X
\quad+
\text{exchange architecture}\;R
\quad+
\text{relationally generated history}\;H
\]

and the intervention question:

> Does changing the relational/exchange architecture, while holding relevant constituent/environmental conditions fixed, alter future viability structure in a repeatable and predictive way?

RVT may also contribute a domain-general relational counterfactual signature rather than a new kernel algorithm.

## Redundancy test

If an undifferentiated augmented-state viability model predicts and controls the system just as well, and the explicit \(R/H\) decomposition adds no interpretability, intervention target, transfer, or prediction, then the specifically RVT machinery is unnecessary.

## Threat level

**Very high.**

## Sources

- Aubin, J.-P. (2009). *Viability Theory*. Birkhäuser. DOI: 10.1007/978-0-8176-4910-4.
- Aubin, J.-P., Bayen, A. M., & Saint-Pierre, P. (2011). *Viability Theory: New Directions*. Springer. DOI: 10.1007/978-3-642-16684-6.
- Aubin, J.-P. (2006). “A Survey of Viability Theory.” *SIAM Journal on Control and Optimization*. DOI: 10.1137/0328044.
- Martin, S., & Alvarez, I. (2019). “Anticipating Shocks in the State Space: Characterizing Robustness and Building Increasingly Robust Evolutions.” *SIAM Journal on Control and Optimization*. DOI: 10.1137/16M1061175.

---

# 4. Neighbor 2 — Adaptive / coevolutionary networks

## What this literature already has

Adaptive-network theory explicitly couples:

\[
\text{dynamics on the network}
\leftrightarrow
\text{dynamics of the network topology}.
\]

Node states change links; changing links alter later node dynamics. This is already a formal version of:

\[
R_t\rightarrow X_{t+1}\rightarrow R_{t+1}.
\]

Therefore RVT cannot claim novelty for the idea that relation structure and constituent state coevolve.

The phrase “the relation changes the future transition structure” overlaps strongly with adaptive-network work whenever \(R_t\) is a topology or coupling matrix.

## Direct threat to RVT

If RVT's relational architecture is only a changing adjacency/coupling structure, then adaptive-network theory already owns most of the conceptual territory.

RVT must not relabel coevolving topology as a new theory.

## What may survive

RVT is broader than topology if \(R_t\) includes **exchange rules** that are not reducible to link existence/strength, such as:

- permeability/boundary rules;
- asymmetric authority;
- receptivity/uptake;
- role-conditioned exchange;
- rerouting after blockage;
- revocation;
- dependence and exit cost.

More importantly, adaptive-network theory usually asks how network and node dynamics coevolve; RVT's distinctive evaluative object is proposed to be the **future viability structure** generated by that coevolution.

So the candidate RVT question is not merely:

> How did the network change?

but:

> What did this pattern of relational exchange do to the set, cost, robustness, and reversibility of future viable action?

Whether that is enough for a distinct framework remains open.

## Redundancy test

If an adaptive-network model with ordinary state variables and standard viability analysis produces the same predictions and intervention guidance without any additional relational decomposition, RVT adds no explanatory value.

## Threat level

**High.**

## Source

- Gross, T., & Blasius, B. (2008). “Adaptive coevolutionary networks: a review.” *Journal of the Royal Society Interface*, 5(20), 259–271. DOI: 10.1098/rsif.2007.1229.

---

# 5. Neighbor 3 — Niche construction and eco-evolutionary feedback

## What this literature already has

Niche-construction theory states that organisms modify environments, those modifications persist as ecological inheritance, and the modified environments alter later selection pressures and evolutionary trajectories.

Schematically:

\[
\text{organism action}
\rightarrow
\text{environment modification}
\rightarrow
\text{changed future selective landscape}
\rightarrow
\text{changed organism dynamics}.
\]

Eco-evolutionary feedbacks add the reciprocal loop explicitly.

This is extremely close to RVT's phrase:

> the path can change the map.

That phrase is therefore **not a defensible novelty claim by itself**.

## Direct threat to RVT

Niche construction already provides:

- endogenous environment modification;
- persistent historical legacy;
- feedback from previous action into future selection;
- altered future possibility through inherited environmental change.

Any biological RVT application must therefore show why it is not merely niche construction under different notation.

## What may survive

Potential RVT scope is broader in two ways:

1. the modified object need not be an evolutionary selective environment; it can be an exchange architecture, authority interface, recovery structure, institutional relation, or technological coupling;
2. the dependent variable is future **viable action/reachability**, not necessarily fitness or evolutionary selection.

RVT may therefore function as a cross-domain generalization of a recursive pattern already formalized in evolutionary ecology.

That is a legitimate synthesis if stated as such. It is not evidence of mathematical novelty.

## Redundancy test

For ecological/evolutionary cases, if niche-construction or eco-evolutionary feedback models already describe the mechanism and predictions, use those theories and do not rebrand the case as uniquely RVT.

## Threat level

**Very high for the “path changes map” claim; medium for RVT as a cross-domain viability synthesis.**

## Sources

- Laland, K. N., Matthews, B., & Feldman, M. W. (2016). “An introduction to niche construction theory.” *Evolutionary Ecology*, 30, 191–202. DOI: 10.1007/s10682-016-9821-z.
- Odling-Smee, J., Erwin, D. H., Palkovacs, E. P., Feldman, M. W., & Laland, K. N. (2013). “Niche Construction Theory: A Practical Guide for Ecologists.” *Quarterly Review of Biology*, 88(1), 4–28. DOI: 10.1086/669266.
- Post, D. M., & Palkovacs, E. P. (2009). “Eco-evolutionary feedbacks in community and ecosystem ecology.” *Philosophical Transactions of the Royal Society B*, 364, 1629–1640. DOI: 10.1098/rstb.2009.0012.

---

# 6. Neighbor 4 — Path dependence, hysteresis, increasing returns, and lock-in

## What this literature already has

Path-dependence literatures already formalize the proposition that timing and sequence matter, small contingencies can have large consequences, history can become difficult to reverse, and present options depend on previous trajectories.

Therefore RVT cannot claim novelty for:

- “history matters”;
- “same apparent present can have different futures”;
- “earlier choices can narrow later options”;
- hysteresis;
- lock-in;
- dependence on sequencing.

## Direct threat to RVT

RVT Proposition 4—different histories yielding different future viability structures—collapses to ordinary path dependence unless the relational mechanism is independently identified.

A same-present/different-history result is especially weak if \(H_t\) is merely an omitted state variable.

## What may survive

RVT's stronger candidate claim is narrower:

> **Relationally mediated exchange changes identifiable transition constraints/costs/channels, and those changes alter future viable action.**

That is more specific than path dependence in the abstract.

The test must therefore identify a mechanism such as:

\[
e_t\rightarrow H_{t+1}\rightarrow R_{t+1}\rightarrow\mathfrak V_{t+1}.
\]

Without the middle mechanism, RVT is just a new vocabulary for path dependence.

## Redundancy test

If historical variables predict later outcomes but intervention on the proposed relational mechanism does not change later viability, classify the result as path dependence—not RVT support.

## Threat level

**High.**

## Source

- Pierson, P. (2000). “Increasing Returns, Path Dependence, and the Study of Politics.” *American Political Science Review*, 94(2), 251–267. DOI: 10.2307/2586011.

---

# 7. Neighbor 5 — Ecological resilience, regime shifts, adaptability, transformability

## What this literature already has

Resilience theory has long distinguished persistence from local stability and later developed explicit concepts of adaptability, thresholds/stability domains, and transformability into new development trajectories.

This strongly overlaps with RVT claims that:

- current functioning is not enough;
- robustness to perturbation matters;
- thresholds and regime shifts matter;
- an old configuration may disappear while a viable new configuration becomes reachable;
- transformative viability differs from simple persistence.

Therefore RVT should not present “transformative viability” as if the underlying distinction were absent from resilience science.

## Direct threat to RVT

RVT's distinction among current, reproductive, and transformative viability may partly repackage existing resilience/adaptability/transformability concepts.

The concepts can still be useful, but novelty must be claimed cautiously.

## What may survive

RVT may add an explicit **relational causal mechanism** for why resilience/transformability changes:

\[
\text{exchange architecture}
\rightarrow
\text{future viability structure}.
\]

It may also add counterfactual relational footprints comparing which future options are created, destroyed, or made more costly by one relation versus another.

But these additions need demonstration, not assertion.

## Redundancy test

If resilience/transformability metrics explain the result and relational variables add no incremental predictive or interventional value, use resilience theory alone.

## Threat level

**High conceptually; lower if RVT can operationalize the relation-specific mechanism.**

## Sources

- Holling, C. S. (1973). “Resilience and Stability of Ecological Systems.” *Annual Review of Ecology and Systematics*, 4, 1–23. DOI: 10.1146/annurev.es.04.110173.000245.
- Folke, C., Carpenter, S. R., Walker, B., Scheffer, M., Chapin, T., & Rockström, J. (2010). “Resilience Thinking: Integrating Resilience, Adaptability and Transformability.” *Ecology and Society*, 15(4):20. DOI: 10.5751/ES-03610-150420.

---

# 8. Neighbor 6 — Dynamic capabilities and organizational routines

## What this literature already has

The dynamic-capabilities literature already argues that organizational capability depends on processes of coordination and recombination, asset positions, inherited paths, and the ability to renew/reconfigure capabilities under changing environments.

Capability-lifecycle work explicitly treats capabilities as evolving, branching, and history-shaped rather than fixed objects.

Therefore RVT cannot claim novelty for:

- capability not being a fixed action list;
- capability depending on configuration;
- path-shaped organizational competence;
- reconfiguration of capability over time;
- “component present ≠ productive capability.”

## Direct threat to RVT

In organizational/development applications, the expression

\[
(C,H,R,E)\rightarrow\mathcal A_{\mathrm{acc}}
\]

has close cousins in dynamic-capability theory.

RVT must not reinvent that literature under relational language.

## What may survive

RVT may offer a different dependent variable and boundary:

- not simply competitive advantage or organizational capability;
- but the effect of relational configuration on **future viable action**, including exit, recovery, recoupling, and option preservation.

RVT also attempts to apply the same diagnostic architecture outside firms.

That is a potential cross-domain contribution, not proof of theoretical novelty.

## Redundancy test

For firm-level cases, if dynamic-capabilities/path-dependence models explain capability evolution and no viability-specific prediction remains, RVT should defer to the domain-native theory.

## Threat level

**Medium to high in development/organization applications.**

## Sources

- Teece, D. J., Pisano, G., & Shuen, A. (1997). “Dynamic Capabilities and Strategic Management.” *Strategic Management Journal*, 18(7), 509–533. DOI: 10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z.
- Helfat, C. E., & Peteraf, M. A. (2003). “The Dynamic Resource-Based View: Capability Lifecycles.” *Strategic Management Journal*, 24(10), 997–1010. DOI: 10.1002/smj.332.
- Pentland, B. T., & Feldman, M. S. (2012). “Dynamics of Organizational Routines: A Generative Model.” *Journal of Management Studies*. DOI: 10.1111/j.1467-6486.2012.01064.x.

---

# 9. Neighbor 7 — Relational Viable Systems Theory / Lavanderos–Malpartida

## Why this is the closest conceptual neighbor

This literature cannot be treated as an incidental citation.

Lavanderos and collaborators explicitly develop **relational viability**, distinguish relation from ordinary interaction, frame organization as relational/historical, connect relational and energetic-material planes, and argue that apparent structural stability need not equal relational viability.

Recent work goes even closer: the 2026 Kybernetes paper states that interactional density, information throughput, and recursive closure are insufficient to distinguish stable from relationally viable configurations, and proposes position, function, and sense as relational invariants.

Earlier ecopoiesis work treats the organism–entorno relation as the relevant unit and describes life as emerging through relational organization that produces conditions for continued existence.

Therefore RVT must explicitly position itself **inside or adjacent to an existing relational-viability tradition**. It must not claim to have invented the proposition that viability is relational.

## Direct threat to RVT

Several RVT intuitions are already present in this tradition:

- relation is not merely interaction;
- relational organization matters for viability;
- structural stability can coexist with relational vulnerability;
- sustainability/viability concerns regeneration of relation, not merely throughput;
- the relevant unit can be relation/system-in-entorno rather than isolated object;
- history/context is constitutive.

The generic phrase “relations reshape the conditions of their own viability” is therefore **not enough to establish distinctiveness**.

## What may survive

The current RVT program appears to differ in emphasis and formal target rather than basic relational ontology.

Candidate distinguishing features are:

1. **Exchange architecture as an intervention-ready causal decomposition** rather than relation as a broad epistemic primitive.
2. Explicit separation of
   \[
   X_t,\;R_t,\;H_t,\;\theta_t
   \]
   for empirical ablation and comparison against simpler models.
3. A declared target object of **finite-horizon future viability structure**:
   \[
   \mathfrak V_t^T
   \]
   including kernels/reachable sets/cost/robustness where defined.
4. Counterfactual relational footprints:
   \[
   \mathcal G_R,\;\mathcal L_R,\;\Delta c_R,\;\Delta m_R.
   \]
5. A strong falsification rule: relational variables must add out-of-sample prediction, intervention value, control value, or transferable explanation beyond augmented constituent/history baselines.
6. Explicit separation of **dynamic viability** from **normative admissibility**; FTL\(\tau\)A is an application-layer admissibility structure, not the definition of generic viability.

Whether these differences are enough to justify a new label rather than a dynamical/operational extension of relational viability remains unresolved.

## Redundancy test

If Lavanderos-style relational viability plus ordinary viability/control theory already supplies the same causal decomposition, measurable predictions, and intervention logic, RVT should be presented as a synthesis/extension rather than a distinct theory.

## Threat level

**Extremely high conceptually. This is the literature RVT must engage most directly and respectfully.**

## Sources

- Lavanderos, L., & Massey, K. (2014/2015). *From Manufacture to Mindfacture: A Relational Viable Systems Theory*. IGI Global. DOI: 10.4018/978-1-4666-7369-4.
- Lavanderos, L., & Malpartida, A. (2023/2024). “Life as a relational unit, the process of ecopoiesis.” *Kybernetes*, 53(12), 5047–5060. DOI: 10.1108/K-05-2023-0859.
- Lavanderos, L. (2026). “Beyond recursive observation: relational viability in von Foerster’s cybernetics.” *Kybernetes*. DOI: 10.1108/K-12-2025-3181.
- Lavanderos, L., & Malpartida, A. (2022). “Ecological Viability and Cybernetic of Ayllu.” *Global Journal of Human-Social Science*, 22(5), 47–55.

---

# 10. Preliminary result of the sandblasting

The audit removes several possible novelty claims immediately.

RVT should **not** claim as novel that:

- systems can remain within constraints under controlled dynamics;
- viability kernels/recovery/capture basins matter;
- network structure and node states can coevolve;
- organisms/systems can modify the landscape that later acts back on them;
- path, history, sequencing, or hysteresis matter;
- current stability/performance can differ from resilience/transformability;
- capability can be path- and configuration-dependent;
- relational viability is conceptually prior to isolated-object viability.

Those territories are already occupied.

This is not a failure of RVT. It tells us where not to build a novelty claim.

---

# 11. What currently survives as specifically RVT?

After this first audit, the strongest surviving candidate is **not one proposition in isolation**.

It is a particular causal-and-evaluative stack:

\[
\boxed{
\text{structured relational exchange}
\rightarrow
\text{endogenous change in exchange architecture}
\rightarrow
\text{measurable deformation of future viability structure}
}
\]

with the following discipline:

### A. Relation is an explicit causal object

RVT does not use “relation” only as a philosophical primitive. It asks for an operationalizable architecture \(R_t\) that can be intervened upon or ablated independently enough to support causal comparison.

### B. The dependent object is future viable action

The target is not topology, fitness, current output, persistence, or capability alone, but changes in declared viable reachability, recovery/reconfiguration cost, robustness, and option structure over a specified horizon.

### C. Relational footprint is counterfactual and non-scalar

Rather than labeling a relation regenerative/extractive in advance, compare:

\[
\mathcal G_R
=
\mathcal Y_V^R\setminus\mathcal Y_V^0,
\]

\[
\mathcal L_R
=
\mathcal Y_V^0\setminus\mathcal Y_V^R,
\]

plus changes in cost/robustness where meaningful.

A relation may create and destroy different possibilities simultaneously.

### D. Relational variables must earn inclusion

The decisive empirical question is:

\[
\boxed{
(R_t,H_t)
\text{ must add predictive, causal, intervention, or control value beyond }(X_t,\theta_t)
\text{ and beyond an ordinary augmented-state baseline.}
}
\]

If they do not, RVT loses.

### E. Dynamic viability is separated from normative admissibility

RVT must truthfully describe stable domination or exploitation as dynamically viable when that is what the dynamics show.

For agency-bearing applications, FTL\(\tau\)A constrains admissibility separately:

\[
\mathcal K_\Omega=\mathcal V\cap\mathcal A_\Omega.
\]

This is an application-layer normative geometry, not generic RVT viability.

---

# 12. Revised positioning hypothesis

The most defensible current positioning is:

> **RVT is a candidate relational-dynamics problem class and causal diagnostic framework built at the intersection of viability theory, adaptive/co-evolutionary systems, path dependence, resilience/transformability, and an existing relational-viability tradition. Its proposed contribution is to isolate and test how operationalizable exchange architectures alter future viability structure, rather than to claim that history, feedback, resilience, or relationality are themselves new discoveries.**

This statement should replace any stronger novelty rhetoric until the literature audit and empirical tests justify more.

---

# 13. Consequence for RVT-MIN-001

The minimal experiment now has a sharper burden.

It is **not enough** to show:

\[
X_T^A\approx X_T^B
\quad\text{and}\quad
\mathcal R_V^A(T)\neq\mathcal R_V^B(T).
\]

That can be ordinary hidden-state/path dependence.

It is **not enough** to show:

\[
R_{t+1}\neq R_t.
\]

That can be an adaptive network.

It is **not enough** to show that the trajectory changed the future environment.

That can be niche construction.

RVT-MIN-001 should therefore require all of the following:

1. an independently operationalized exchange architecture \(R_t\);
2. a relationally generated history variable or structural change;
3. an intervention/ablation on the path
   \[
   e_t\rightarrow H_{t+1}\rightarrow R_{t+1};
   \]
4. measurement of future viability structure under a common horizon/control/constraint definition;
5. comparison with a simpler constituent-state model;
6. comparison with a generic augmented-state model;
7. evidence that the relational decomposition improves prediction, diagnosis, transfer, or control—not merely fit;
8. a result allowed to be null.

The **killer ablation** remains:

\[
H_t\nrightarrow R_{t+1}.
\]

But the benchmark comparison is now equally important:

> If an ordinary augmented state \(Z_t\) performs just as well for every scientific purpose, the experiment does not establish a distinct RVT contribution.

---

# 14. Next literature work

This is a first-pass adversarial audit, not a systematic review.

Before publication-level novelty claims, expand especially in:

- viability theory with evolving/time-dependent constraints and hybrid dynamics;
- robust controlled invariance and barrier-function methods;
- adaptive networks beyond topology-only cases;
- niche construction / ecological inheritance / eco-evolutionary feedback;
- resilience and regime-shift mathematics;
- hysteresis and endogenous state-space deformation;
- dynamic capabilities and routine dynamics;
- Lavanderos/Malpartida relational viability, ecopoiesis, and triferential relational logic;
- causal dynamical systems approaches to changing mechanisms;
- endogenous institutions and network formation in economics.

The publication strategy should remain conservative until this deeper review is complete.

---

# 15. Current verdict

The sandblaster did **not** erase RVT.

It did erase the easiest novelty claims.

What remains is narrower and more defensible:

\[
\boxed{
\text{RVT asks whether identifiable relational exchange mechanisms alter future viable action in ways that earn explanatory or control value beyond ordinary state-based models.}
}
\]

That is now the object to test.
