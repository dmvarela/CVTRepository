# CP-002 — Read-Only Host Proprioception Probe

Status: ready for local execution on the Windows development host

## Question

Can Lucian OS replace static host assumptions with a privacy-conscious, read-only snapshot of the machine it is actually running on, without acquiring write authority or performing network/device actions?

CP-001 showed in simulation that experienced transition/resource measurements can improve scheduling. CP-002 is the first bridge from synthetic host state toward real computational proprioception.

## Prototype

```text
prototype/host_proprioception_probe_v001.py
```

Default run:

```bash
py prototype/host_proprioception_probe_v001.py --host-id windows-dev-001
```

Optional local-runtime status check:

```bash
py prototype/host_proprioception_probe_v001.py --host-id windows-dev-001 --include-runtime-status
```

The optional flag executes only the read-only command `ollama ps`. It does not load, unload, download, or name models in the output.

## Default observations

The probe reports:

```text
OS family / release
architecture
Python version
logical CPU count
memory total / available / used
disk total / free / used
whether Python, Git, Ollama, and PowerShell are discoverable
UTC observation timestamp
caller-supplied host label
```

These are separated conceptually into:

```text
STATIC-ish AFFORDANCES
  architecture
  runtime availability
  CPU topology

DYNAMIC STATE
  available RAM
  used RAM
  free disk
  runtime responsiveness when explicitly requested
```

## Privacy boundary

The probe deliberately does **not** collect:

```text
hostname
username
hardware serial number
MAC / IP address
network location
executable paths
model names
personal files
process command lines
```

A caller supplies a non-secret host label such as `windows-dev-001`; the probe does not derive identity from hardware fingerprints.

## Side-effect contract

Default and optional modes must preserve:

```text
file writes        = false
permission changes = false
network probe      = false
model load/unload  = false
device actuation   = false
```

The script prints JSON to stdout only. Redirecting that output to a file would be a separate user/shell action, not behavior performed by the probe itself.

## Initial tests

### T1 — baseline snapshot

Run the probe once on the Windows development host.

Expected:

- Windows host detected;
- Python available;
- memory/CPU fields populated;
- no identity-sensitive fields collected.

### T2 — repeated snapshots

Run twice under ordinary conditions.

Expected:

```text
static fields mostly stable
dynamic memory fields allowed to differ
observation timestamps differ
```

This distinguishes embodiment identity/context from live body state.

### T3 — runtime availability

If Ollama is installed, default mode should report only its availability.

With `--include-runtime-status`, the probe may report:

```text
responding = true/false
loaded_model_count = integer/null
```

but not model names.

### T4 — no-write audit

Run in a clean working tree and compare Git/file state before and after.

Expected:

```text
no repository mutations
no generated files
no permission changes
```

### T5 — adapter bridge

Use the returned JSON as input to a future converter that creates an operational host snapshot for ECM/MAS.

The converter must preserve the distinction:

```text
declared capability
!=
observed current state
!=
empirically calibrated transition cost
```

CP-002 does **not** yet measure model load/unload transitions.

## What CP-002 does not do

It does not:

- benchmark CPU/GPU performance;
- inspect personal processes or files;
- probe external network connectivity;
- identify hardware by serial number;
- load or unload a model;
- infer authority from capability;
- write a persistent host profile;
- replace CP-001's transition-calibration problem.

## Next step after successful local run

CP-003 should add an **explicitly authorized bounded transition probe** for one harmless computational morphology, for example timing a known local module initialization/uninitialization while measuring RAM before/after.

That probe should preserve:

```text
predict
-> bounded transition
-> observe
-> update only the relevant host-scoped edge
-> verify contraction
```

and should not begin with model loading if a cheaper deterministic module can validate the measurement pipeline first.

Concise principle:

> **First learn the resting body without touching it. Then, only with bounded authority, learn how the body changes when it moves.**
