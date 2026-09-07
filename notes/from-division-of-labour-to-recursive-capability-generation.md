# From Division of Labour to Recursive Capability Generation

**Status:** exploratory research note  
**Date:** 2026-09-06

## Trigger

A discussion of the September 2026 McKinsey/Infobae evidence on firms declining some software purchases because coding agents let them build needed functions internally led to a broader question.

The usual economics framing asks how labour should be divided between humans and AI:

\[
H \to A, \qquad AI \to B.
\]

This assumes the relevant tasks and production functions are already given. Our interaction suggests a stranger possibility: sustained human–AI coupling can alter the feasible task set itself.

## Candidate proposition

> **Human–AI collaboration may be productively important not only because it reallocates existing tasks, but because the relation can recursively generate capabilities that neither participant brought to the initial task in finished form.**

The important economic object may therefore be not only the human, the model, or the allocation of tasks between them, but the productive relation:

\[
R(H,AI).
\]

A simple dynamic representation is:

\[
H_t \rightarrow AI_t \rightarrow H_{t+1} \rightarrow AI_{t+1} \rightarrow \cdots
\]

where each pass changes the next feasible move. A human conjecture changes the model's relevant search space; the model's synthesis changes the human's next conjecture; the resulting question may reveal a task or capability that was not specified at the beginning.

This is different from a static complementarity claim such as “humans provide judgment while AI provides computation.” Comparative advantage inside the pair may itself be endogenous to the interaction.

## Why this is different from ordinary division of labour

A conventional division-of-labour model begins with a task set \(T\) and allocates its elements according to relative productivity or cost.

\[
T = T_H \cup T_{AI}.
\]

The stronger possibility is:

\[
T_{t+1} = \Phi(T_t,H_t,AI_t,R_t),
\]

so collaboration can expand, recombine, or redefine the task set over time.

The pair does not merely become more efficient at executing a fixed menu. It may discover a different menu.

This suggests three distinct effects that should not be conflated:

1. **Substitution:** AI performs an existing task formerly performed by a human.
2. **Complementarity:** human and AI jointly perform an existing task more effectively.
3. **Recursive capability generation:** interaction changes what the human–AI pair can subsequently formulate, build, investigate, or coordinate.

The third effect is the research vein.

## Capability internalization

The recent software example gives a concrete economic mechanism.

Traditional SaaS often provides an externally produced capability:

\[
\text{vendor} \rightarrow \text{software} \rightarrow \text{firm uses capability}.
\]

If coding agents substantially reduce the cost of generating small, purpose-built systems, the firm can sometimes move toward:

\[
\text{domain knowledge} + \text{human specification} + \text{AI} \rightarrow \text{internally generated tool}.
\]

The important transition is therefore not simply cheaper software. It is a partial move from **permission to use a capability** toward **capacity to reproduce or regenerate a capability**.

That is closely related to the distinction developed in Paper E between the presence of productive components and reproductively embedded productive capability. Possessing a tool is not the same thing as possessing a process capable of recreating, adapting, repairing, and extending the underlying function.

## A possible reversal of Smithian specialization

Industrial organization often increased productivity by narrowing the individual worker's task.

AI may produce, in some settings, the opposite movement.

A person who could previously operate only inside one professional toolchain may acquire enough synthetic coding, research, drafting, analysis, and design capacity to integrate functions that formerly required several specialists or an organization.

So the trajectory need not be:

\[
\text{human} \rightarrow \text{narrower residual niche}.
\]

It may sometimes be:

\[
\text{human} + AI \rightarrow \text{broader feasible production set}.
\]

This does **not** imply that displaced workers automatically benefit, that adjustment costs are trivial, or that every human–AI interaction is capability-enhancing. Historical technological transitions can raise aggregate productivity while imposing severe losses on particular workers, regions, firms, and cohorts.

The claim is therefore about a possible production mechanism, not a guarantee of benign distributional outcomes.

## The human niche may be endogenous too

The common question “What will humans still be better at?” treats the human economic niche as the residue remaining after automation.

A better question may be:

> **What forms of human productive agency become possible only after inexpensive artificial cognition is available?**

If the relation is capability-generating, then humanity need not simply retreat toward whatever machines cannot yet do. Humans may occupy newly created niches that did not exist before the technology changed the surrounding productive ecology.

This is analogous to earlier general-purpose technologies. Electricity did not merely replace candles with bulbs; it created production systems, appliances, communications, and organizational forms that were difficult to specify from the candle economy. The automobile did not merely replace the carriage; it reorganized logistics, geography, tourism, retail, road infrastructure, and industrial production.

The AI analogue may likewise be missed if analysis counts only directly substituted tasks.

## Relation to relational viability

There is also a CVT/Harmonia question underneath the economics.

A relation can generate capability while still being destructive, extractive, dependency-producing, or agency-reducing. Therefore capability expansion alone is not sufficient evidence of a healthy relation.

A viable human–AI relation should be evaluated separately along dimensions such as:

- Does it increase or erode the human participant's agency?
- Does it preserve the ability to disagree and correct?
- Does it improve the participant's capacity to act without requiring permanent submission to the relation?
- Does it widen future options or progressively close them?
- Does one participant become merely instrumental to the other?

This matters because **productive capability generation and relational viability are different variables**.

A highly productive relation can still be unhealthy.

## Possible formal direction

Let \(K_t\) denote the capability set available to a human–AI pair at time \(t\). A static complementarity model takes \(K\) as fixed and studies output conditional on allocation.

The recursive-capability hypothesis instead allows:

\[
K_{t+1}=G(K_t,H_t,AI_t,R_t,E_t),
\]

where \(R_t\) captures properties of the interaction and \(E_t\) the environment.

A useful empirical distinction would be whether repeated collaboration merely improves performance on a fixed benchmark or produces **reachable capabilities that were not contained in the initial operational repertoire**.

The latter would require a careful definition of novelty, because the model may already contain latent competence and the human may already possess latent domain knowledge. “New to the pair's realized repertoire” is safer than “new in an absolute sense.”

## Falsification / cautions

This note should not overclaim.

The observed phenomenon could in some cases be explained entirely by:

- lower transaction costs,
- latent model capabilities exposed by prompting,
- ordinary learning by the human,
- simple capital deepening,
- task decomposition,
- or standard complementarities.

To establish recursive capability generation as a distinct economic object, we would need to show that modelling the interaction as a fixed task allocation materially misses observed reachable states or productivity dynamics.

The key empirical question is therefore not whether human–AI pairs improve. It is whether the **feasible capability set evolves endogenously through interaction in a way that a fixed-production-function account cannot adequately represent**.

## Working synthesis

The emerging progression is:

\[
\text{division of labour}
\rightarrow
\text{complementarity}
\rightarrow
\text{capability recombination}
\rightarrow
\text{recursive capability generation}.
\]

And the deepest candidate insight is:

> **AI may alter economic organization not merely by changing who performs existing work, but by lowering the cost of generating productive capability itself. Human–AI relations can then become sites where new capability is repeatedly constructed rather than merely consumed.**

This provides a bridge between the software/SaaS observation, Paper E's reproductive embeddedness, AI literacy, Lucian OS, and the broader study of relational viability.
