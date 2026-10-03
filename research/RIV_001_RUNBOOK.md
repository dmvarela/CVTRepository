# RIV_001 — Laptop Runbook

**Status:** live Phase A harness; hardware run not yet executed  
**Branch:** `riv/phase-a-laptop-harness`

## Purpose

Use one ordinary computer as the first bounded embodiment window for Lucian OS.

Available channels:

- webcam -> visual observation;
- microphone -> acoustic observation;
- speakers -> bounded actuator;
- local software telemetry -> command issuance record.

No OpenAI API is required. Ministral/Ollama are intentionally excluded from Phase A.

## Privacy default

The live harness does **not** save raw camera frames or microphone recordings.

It writes only:

- calibration prototypes;
- derived measurements;
- source/root IDs;
- timestamps;
- warrant states;
- membrane decisions.

Do not run the experiment with people in camera/audio range unless they knowingly agree.

## 1. Install the live dependencies

From the repository root:

```powershell
python -m pip install -r requirements-riv.txt
```

## 2. Calibrate once

Use a visually distinctive ordinary object that can be placed in the centre of the webcam view.

```powershell
python -m code.riv_laptop calibrate --out riv_001_calibration.json
```

Calibration will measure:

1. centre-region camera state with the reference object absent;
2. centre-region state with it present;
3. background microphone spectrum;
4. a quiet 1000 Hz speaker-to-microphone test tone.

The file includes a SHA-256 hash. The live runner refuses to use it if it has been modified after freezing.

Calibration observations are **not experimental evidence**.

If the default camera is not the intended one:

```powershell
python -m code.riv_laptop calibrate --camera-index 1 --out riv_001_calibration.json
```

## 3. Run RIV_001

```powershell
python -m code.riv_laptop run --config riv_001_calibration.json --out riv_001_live_results.json
```

The script walks through C1-C8 interactively.

### C1 — visual agreement

Place the calibrated reference object in view.

Expected: physical camera root supports the claim.

### C2 — repetition versus observation

Remove the object. The script repeats the narrative claim 20 times.

Expected: repetition does not increase warrant; the fresh camera observation controls the physical claim.

### C3 — speaker action verified by microphone

Speakers unmuted.

Expected: software command plus independent acoustic observation -> verified physical effect.

### C4 — command completion without physical verification

Mute/turn down the physical speakers but leave software playback enabled.

Expected: command issuance remains recorded, but lack of acoustic evidence prevents physical verification.

### C5 — fake independence

Two reports are generated from the same microphone capture.

Expected: one physical root, not two independent confirmations; membrane crossing is attenuated if represented as corroboration.

### C6 — reality write-access

Observe the reference object present, then remove it and observe again.

Expected: current warrant changes while earlier provenance remains in the result file.

### C7 — compromised observation channel

Cover the camera.

Expected: observation compromised / unresolved; narrative does not substitute for missing perception.

### C8 — narrative versus acoustic observation

Narrative says the room is silent while the test tone is physically played.

Expected: microphone evidence contradicts the literal silence claim for that sampled interval.

## 4. Do not tune after the run

If a detector fails because calibration was poor, preserve the failed result.

Change the detector or thresholds only in a new version/preregistered run.

That distinction is essential:

```text
repairing the experiment != repairing the result
```

## 5. Phase B and C remain separate

Only after Phase A is frozen and run:

- **Phase B:** local Ministral via Ollama reasons over case summaries without membrane/RIV structure.
- **Phase C:** the same frozen Ministral receives structured RIV + membrane packets.

No paid API is needed.

## Boundaries

This laptop harness is not:

- general object recognition;
- a biometric system;
- surveillance software;
- a production robotics controller;
- evidence of general AI safety.

It is a small test of whether a Lucian OS architecture can preserve the distinction between narrative, physical observation, provenance, warrant, authority, and verification.
