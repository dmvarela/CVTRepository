# ECM-004 — Grammar Compression into Typed Transitions

Status: design experiment

## Why this experiment exists

ECM-003 introduces an adapter-friendly surface grammar:

```text
SENSE / PRESENT / COMPUTE / STORE / COMMUNICATE / ACT
```

That grammar may still encode human product distinctions that the Lucian core does not need.

A camera, display, filesystem, network link, motor, and local model can all be described more generally as **typed state transitions** between domains.

This experiment asks whether the six surface families can be lowered into a smaller core representation without losing the distinctions needed for safety, routing, verification, and embodiment calibration.

## Candidate core representation

Represent a primitive affordance as a transition edge:

```text
E = (
  source_domain,
  target_domain,
  operation,
  locality,
  preconditions,
  resources,
  authority,
  risk,
  reversibility,
  verification,
  provenance,
  confidence
)
```

A host becomes a provisional transition graph:

```text
G_declared = (state_domains, transition_edges)
```

After bounded calibration:

```text
G_declared -> evidence -> G_operational
```

Task morphology then becomes selection of an admissible task-conditioned subgraph.

## Example lowerings

### Camera

Surface syntax:

```text
sense.camera
```

Candidate transition:

```text
physical_scene -> digital_image
operation: observe
locality: local
```

### Display

Surface syntax:

```text
present.display
```

Candidate transition:

```text
digital_visual_state -> human_visible_surface
operation: present
locality: local
```

### Filesystem read

Surface syntax:

```text
store.filesystem
```

Candidate transition:

```text
persistent_bytes -> working_state
operation: read
```

### Filesystem write

Same physical substrate, different edge:

```text
working_state -> persistent_bytes
operation: write
authority: write_files
```

This immediately shows why a single `filesystem` token is too coarse for least privilege.

### Network uplink

Surface syntax:

```text
communicate.network_uplink
```

Candidate transitions:

```text
local_message -> remote_endpoint
remote_response -> local_state
```

with separate authority/privacy/cost constraints.

### Manipulator

Surface syntax:

```text
act.manipulator
```

Candidate transition:

```text
control_command -> physical_world_state
operation: actuate
authority: physical_actuation
verification: perception / force / position evidence
```

### Local model runtime

Surface syntax:

```text
compute.local_model_runtime
```

Candidate transition:

```text
working_state -> transformed_working_state
operation: infer
locality: local
```

## Compression hypothesis

The six surface families may be reducible at the core to a small number of directional transition classes:

```text
INGRESS      environment/other state -> local working state
TRANSFORM    local working state -> local working state
EGRESS       local working state -> environment/other state
```

Persistence and communication then become properties of the source/target domain rather than top-level verbs.

This is only a hypothesis.

The compression is useful only if it preserves safety-relevant semantics. A representation that makes a speaker, file write, network send, and robot motor look indistinguishable would be too compressed to route safely.

## Two-level architecture candidate

```text
ADAPTER SURFACE GRAMMAR
  SENSE / PRESENT / COMPUTE / STORE / COMMUNICATE / ACT
            |
            v
        compiler / lowering
            |
            v
CORE TRANSITION GRAPH
  typed source/target domains
  + direction
  + operation
  + resources
  + authority
  + risk
  + verification
  + provenance/confidence
```

This gives adapters a vocabulary humans and device integrations can understand while keeping the core ontology general.

## Test A — semantic preservation

Lower every primitive used in ECM-003 into transition edges.

Reconstruct the task-relevant requirements from the lowered form.

Expected:

```text
ECM-003 morphology decisions remain unchanged.
```

If lowering changes which morphologies are viable, identify whether the surface grammar carried information that the core representation lost.

## Test B — least-privilege gain

Split coarse affordances that currently bundle asymmetric operations.

Primary target:

```text
filesystem
```

Expected lowered edges:

```text
read persistent state
write persistent state
```

A read-only task must not acquire write authority merely because the same physical storage device supports both.

## Test C — locality substitution

Compare two reasoning edges:

```text
local working state -> locally transformed state
local working state -> remote endpoint -> returned transformed state
```

Expected:

The core can compare both as routes to a task function while still accounting for latency, privacy, network authority, and cost.

## Test D — embodiment calibration

Mark one declared transition as contradicted by observation.

Expected:

The operational graph retracts or downgrades that edge, and any morphology depending on it becomes unavailable or contested.

This preserves the earlier rule:

> Truth has to bite by changing reachability.

## Test E — over-compression failure

Deliberately erase source/target domain types and retain only `INGRESS/TRANSFORM/EGRESS`.

Expected:

The representation should become insufficient for safe routing.

This is a necessary negative control: the goal is not maximal compression. The goal is the **smallest grammar that preserves the distinctions that actually matter**.

## Success criterion

ECM-004 succeeds if a transition-graph representation can reproduce ECM-003 decisions while making at least one important distinction cleaner — especially read vs write, local vs remote, or physical vs informational effects — without relying on device labels.

## Architectural consequence if successful

The quiet-revolution stack becomes:

```text
human intent
-> task demand
-> operational transition graph
-> admissible subgraph selection
-> temporary morphology
-> execution / proposal
-> verification
-> contraction
```

The host adapter no longer answers:

> What kind of device am I?

It answers:

> What state transitions can I currently support, under what constraints, and how do we know?

That is a much more general substrate interface.

## After ECM-004

ECM-005 should build the first **capability handshake**: receive a messy host/adapter description, preserve uncertainty and provenance, and compile it into the transition representation rather than assuming a perfectly curated manifest.
