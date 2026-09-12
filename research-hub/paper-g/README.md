# Paper G — Reproductive Breadth and Capability Migration

## Working title

**Reproductive Breadth: Capability Migration, Recombination, and Development in Changing Production Networks**

**Authors:** Daniel Varela Arévalo with Lucian (AI research collaborator; authorship/disclosure to be adapted to venue rules)

**Status:** seed research note, 12 September 2026.

## Why this paper exists

Paper F asks whether temporary support creates capability that can graduate, remain viable without support, and survive or recombine when an original productive configuration exits. This paper begins one level downstream and asks a broader development question:

> **When productive configurations change, does an economy preserve and recombine capability into new viable relations, or does capability disperse faster than new reproductive structures form?**

The motivating observation is that firm exit, sectoral decline, frontier-sector growth, export growth, and even aggregate GDP growth are individually insufficient to diagnose development. A country can contain world-class productive islands while its wider productive ecology thins. Conversely, the disappearance of firms or sectors need not imply developmental failure if workers, knowledge, capital, routines, supplier relations, and institutions migrate into more productive configurations.

The proposed state variable is therefore not firm survival or sector survival. It is **reproductive capacity**, with **reproductive breadth** capturing how widely productive capability is embedded in viable, self-renewing relations.

## Core thesis

> **Development is the expansion of an economy's capacity to reproduce, recombine, and propagate productive capability through a changing network of relations.**

This yields the central diagnostic distinction:

> **Creative destruction is developmental only when capability can migrate and recombine. Otherwise, destruction may be de-accretion of the productive basin.**

A compact formulation is:

`exit + entry + mobility + recombination -> possible developmental transformation`

but

`exit without capability migration/recombination -> possible basin erosion`.

The policy objective is therefore not to freeze the current productive configuration. It is to make the configuration **transformable without unnecessarily destroying transferable capability**.

## The two-sided Argentina observation

Two Argentine news items published on 11 September 2026 provide a clean motivating contrast.

### Side A — RA-10: accumulated capability seeking propagation

An interview with Argentina's Secretary of Nuclear Affairs, Federico Ramos Napoli, describes the RA-10 multipurpose reactor as a platform for radioisotope production, silicon doping, materials testing, and research; it also describes a proposed mixed-capital commercial structure intended to scale commercial use while CNEA preserves research functions. The official government announcement of 4 September 2026 states that commissioning is expected to begin before the end of 2026 with completion in the first months of 2027, and that private capital is envisaged for the associated production plant.

The important development fact is not simply that Argentina *has a reactor*. The nuclear complex represents decades of accumulated relations among CNEA, INVAP, technical institutes, engineers, laboratories, suppliers, projects, and foreign clients. RA-10 is therefore a candidate **frontier-reproductive node**: a concentration of capability that may propagate through exports, new projects, training, supplier demand, research, and commercial services.

Empirical sources:
- Ámbito, 11 Sep 2026: https://www.ambito.com/energia/reactor-ra-10-y-exportacion-bienes-y-servicios-ramos-napoli-detallo-la-estrategia-la-politica-nuclear-n6321328
- Argentina.gob.ar / CNEA, 4 Sep 2026: https://www.argentina.gob.ar/noticias/el-ra-10-se-pondra-en-marcha-en-2027-con-un-modelo-de-produccion-de-radioisotopos-con

### Side B — employer-unit contraction: possible basin thinning

A second Ámbito report, using Superintendencia de Riesgos del Trabajo data, reports a net decline of 8,734 covered productive/employer units in the first half of 2026 (-1.8%), alongside further covered-worker losses and industrial contraction.

**Truth-discipline note:** SRT employer/covered-unit data must not automatically be equated one-for-one with legal company closures. Administrative changes, reorganizations, changes in employer status, and coverage definitions can affect the series. The paper should use the precise SRT concept and treat the observation as evidence of productive-employer contraction/stress, not as proof that exactly 8,734 legally distinct companies ceased to exist.

Empirical source:
- Ámbito, 11 Sep 2026: https://www.ambito.com/economia/cierre-empresas-el-primer-semestre-2026-se-destruyeron-casi-8800-companias-n6320900

These two observations can coexist. A frontier component may be technologically sophisticated and even locally supercritical while broad reproductive embedding weakens elsewhere.

## Reproductive breadth

Let the productive economy at time `t` be a directed weighted graph `G_t = (V_t, E_t)` whose nodes represent productive capabilities/configurations and whose edges represent economically consequential complementarities, learning flows, supplier/customer dependence, worker-skill transfer, institutional support, or other capability-reproducing relations.

A node matters developmentally not merely because it exists, but because it participates in relations that reproduce capability through time.

Define a provisional **reproductively viable set** `R_t` as the subset of nodes belonging to one or more viable capability-reproduction paths or strongly connected components under the relevant technological, financial, human-capital, and institutional constraints.

A first crude breadth statistic could be

`RB_t = sum_{i in R_t} omega_i / sum_{i in V_t} omega_i`,

where `omega_i` weights employment, value added, capability complexity, strategic option value, or another empirically justified measure.

The measure itself is not yet settled. The conceptual point is:

> Two economies with the same GDP, exports, or number of frontier firms can differ sharply in the share and diversity of productive capability embedded in relations capable of reproducing themselves.

This extends the earlier result that **aggregate supercriticality does not imply broad reproductive embedding**.

## Capability migration and recombination

Firm and sector exit should be decomposed into the fate of the capabilities embodied in the departing configuration.

Let `q_i` denote a vector of capabilities associated with configuration `i`. After exit, capability can:

1. **Persist in place** through successor ownership or organizational restructuring.
2. **Migrate** through workers, entrepreneurs, equipment, supplier relationships, routines, intellectual property, finance, or institutions.
3. **Recombine** with different complements to form new productive configurations.
4. **Remain latent** as recoverable capability for some period.
5. **De-accrete** through unemployment, deskilling, scrapping, emigration, supplier disappearance, loss of routines, financing relationships, or institutional decay.

The developmental diagnosis therefore depends on the transfer mapping

`T_{i -> j}(q_i)`

and not merely on whether node `i` survives.

### Key proposition candidate

**Capability-Migration Condition (working):**

An episode of productive destruction is developmentally improving only if the discounted reproductive value of capability transferred and recombined into successor configurations, net of transition losses, exceeds the reproductive value destroyed by exit.

Symbolically, for an exiting set `X_t` and successor/recombination set `Y_{t+1}`:

`sum_{j in Y} RV(q_j^{inherited} + q_j^{new}) - L_transition > sum_{i in X} RV(q_i^{lost})`,

with the exact definition of `RV` to be formalized.

This is deliberately stronger than the assertion that resources were "freed". Resources can be released without preserving the capability embodied in their prior organization.

## Creative destruction versus basin erosion

The paper should distinguish at least four exit regimes:

- **Productive supersession:** old configurations disappear, but their capabilities migrate/recombine into more productive or more reproductive structures.
- **Neutral churn:** exit and entry occur with little durable change in reproductive capacity.
- **Basin erosion:** productive relations disappear and embodied capability is dispersed or lost faster than successor structures form.
- **Entrenched preservation:** incumbent configurations survive through protection/capture despite weak contribution to future reproductive capacity.

This avoids the symmetric errors of treating all exit as healthy discipline or all survival as development.

## The playing field, reformulated

The "playing field" is not merely a vector of stable macro rules. A developmentally useful playing field supports four operations:

`exit + entry + mobility + recombination`.

- **Exit** prevents indefinite preservation of nonviable configurations.
- **Entry** allows new configurations to form.
- **Mobility** allows people, capital, knowledge, and organizational resources to leave obsolete structures.
- **Recombination** allows inherited capability to couple with new complements rather than being reset to zero.

This yields a sharper interpretation of policy stability:

> **Stable rules, contestable positions, transferable capability.**

The state need not guarantee incumbents. It may have a legitimate developmental role in maintaining the conditions under which capability survives institutional and sectoral change.

## Two clocks

The Argentina nuclear case exposes a timing problem.

Let

`tau_m = market survival / financing horizon`

and

`tau_c = capability formation and reproduction horizon`.

For many advanced capabilities, `tau_c >> tau_m`.

Institutions may therefore matter not because markets are intrinsically incapable of coordination, but because some productive capabilities require continuity across horizons longer than ordinary firm financing, political terms, or short-run demand shocks. Developmental institutions can be interpreted as mechanisms that bridge these clocks while still allowing eventual discipline and reconfiguration.

This is not an argument for permanent protection. It is an argument for distinguishing **long-horizon capability formation** from **indefinite incumbent preservation**.

## Frontier growth without reproductive embedding

A country can experience rapid growth in mining, energy, agriculture, finance, or a sophisticated technological niche while broad productive relations weaken.

This motivates the concept:

> **Frontier growth without reproductive embedding:** expansion of high-productivity or high-complexity nodes whose domestic capability-reproducing neighborhood is too thin, weakly connected, or shrinking for the gains to propagate broadly.

The empirical question is not whether a frontier sector has domestic suppliers in a static input-output sense, but whether its expansion creates durable capability cycles:

`projects -> learning -> people/suppliers -> harder projects -> expanded capability -> new projects`.

This is the difference between a frontier node and a reproductive frontier.

## Candidate empirical test: restructuring or erosion?

The strongest empirical test suggested by the Argentina case is to track what happens to the factors and capabilities released by shrinking firms/sectors.

For cohorts of exiting/shrinking firms or sectors, measure where possible:

- worker transitions by occupation, wage, industry, formality, and geography;
- re-employment time and skill retention;
- new-firm formation by former workers/managers/owners;
- movement or scrapping of machinery and productive assets;
- supplier/customer-network survival and substitution;
- patent, engineering, certification, and technical-team continuity;
- regional entry rates and establishment density;
- import substitution of formerly domestic intermediate inputs;
- survival of training pipelines and specialized educational programs;
- time required to reconstitute lost capability.

A transition is more consistent with **recombination** when displaced capability appears in viable successor configurations. It is more consistent with **erosion** when capability leaves the productive network through prolonged non-employment, informality unrelated to prior capability, deskilling, emigration, asset scrapping, supplier disappearance, or permanent import replacement without domestic capability formation.

## Argentina as motivating case, not predetermined verdict

The paper must not begin with the conclusion that Argentina's current restructuring is either successful or destructive. RA-10 is a motivating example of long-horizon accretion and attempted propagation. The SRT/industrial data are a motivating signal of stress and contraction. Whether current restructuring represents supersession, neutral churn, or basin erosion is an empirical question.

Likewise, South Korea should not be used as a morality play. The relevant question is whether declining activities released transferable capability into successor industries, under what institutions, and with what transition losses.

Chile, Canada, Poland, Ireland, Singapore, Japan, and other cases can be used only where they permit measurement of the proposed mechanism rather than as decorative country comparisons.

## Relationship to Paper F

Paper F remains narrower:

`activation -> capability accumulation -> graduation -> unsupported viability -> generativity -> supersession/de-accretion`.

Paper G takes the supersession/de-accretion boundary as its starting point and asks what happens at system scale:

`exit/change -> capability migration -> recombination -> reproductive breadth -> development trajectory`.

Paper F asks whether a productive relation can graduate and what survives its exit. Paper G asks whether the economy as a whole becomes better at **reusing what it learns**.

## Formal agenda

1. Define productive capability separately from current output and current firm identity.
2. Define transferability and recombinability of capability.
3. Define reproductive value of a capability/configuration.
4. Define reproductive breadth and distinguish breadth from aggregate output or average complexity.
5. Model exit as a transformation operator on the capability graph rather than node deletion alone.
6. Derive conditions under which creative destruction increases reproductive breadth.
7. Derive conditions for basin erosion / de-accretion cascades.
8. Introduce the two-clock problem `tau_c > tau_m` and characterize when bridging institutions can improve long-run reproductive capacity without freezing incumbents.
9. Separate frontier-node growth from reproductive-frontier propagation.
10. Produce empirically testable measures of capability migration after exit.

## Claims to stress-test aggressively

- Reproductive breadth contains information not already captured by economic complexity, input-output centrality, related variety, industrial relatedness, or employment diversity.
- Capability migration can be observed well enough to distinguish supersession from erosion.
- The framework does not smuggle welfare conclusions into a positive network measure.
- A broad productive network is not automatically better; some dense networks can reproduce low-productivity traps.
- Reproductive breadth must incorporate quality/viability, not merely number of links.
- Frontier sectors may generate foreign rather than domestic reproductive loops; the framework must handle international embedding without treating domestic autarky as the objective.
- Long capability horizons do not automatically justify state intervention; the model must specify the failure/coordination mechanism and compare institutional alternatives.
- The framework must allow successful development through international complementarity, not only domestic closure.

## Strong working claims

> **Firm survival is not the objective. Capability survival is not enough either. The developmental objective is capability that can migrate, recombine, and reproduce.**

> **Creative destruction is developmental only when capability can migrate.**

> **Exit without entry empties the field. Entry without inherited capability repeatedly starts from zero.**

> **Stable rules, contestable positions, transferable capability.**

> **A frontier is developmentally important when it reproduces a widening neighborhood of capability, not merely when it grows.**

> **Development succeeds when an economy becomes better at reusing what it learns.**
