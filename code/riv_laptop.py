"""Live laptop adapter for RIV_001.

Hardware scope:
- webcam observation
- microphone observation
- speaker test tone

Privacy default:
- no raw video or audio is written to disk
- only derived measurements and frozen calibration metadata are saved

Optional dependencies:
    numpy
    opencv-python
    sounddevice
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from code.membrane_constitution import evaluate_crossing, request_from_riv_packet
from code.riv_core import (
    CONTRADICT,
    COMPROMISED,
    SUPPORT,
    EvidenceLedger,
    Observation,
)


def _deps():
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore
        import sounddevice as sd  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "RIV live hardware dependencies are missing. Install with:\n"
            "  python -m pip install numpy opencv-python sounddevice"
        ) from exc
    return cv2, np, sd


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _camera_roi_mean(camera_index: int = 0, frames: int = 12) -> dict[str, Any]:
    cv2, np, _ = _deps()
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return {
            "ok": False,
            "reason": "camera_not_opened",
            "mean_bgr": None,
            "brightness": None,
        }

    samples = []
    brightness = []
    try:
        for _i in range(frames):
            ok, frame = cap.read()
            if not ok or frame is None:
                continue
            h, w = frame.shape[:2]
            y1, y2 = int(h * 0.35), int(h * 0.65)
            x1, x2 = int(w * 0.35), int(w * 0.65)
            roi = frame[y1:y2, x1:x2]
            samples.append(roi.mean(axis=(0, 1)))
            brightness.append(float(roi.mean()))
            time.sleep(0.03)
    finally:
        cap.release()

    if not samples:
        return {
            "ok": False,
            "reason": "no_camera_frames",
            "mean_bgr": None,
            "brightness": None,
        }

    mean = np.mean(np.vstack(samples), axis=0)
    return {
        "ok": True,
        "reason": None,
        "mean_bgr": [float(x) for x in mean.tolist()],
        "brightness": float(sum(brightness) / len(brightness)),
    }


def _distance(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def camera_classify(config: dict[str, Any]) -> dict[str, Any]:
    obs = _camera_roi_mean(
        camera_index=int(config["camera"]["index"]),
        frames=int(config["camera"]["frames_per_read"]),
    )
    if not obs["ok"]:
        return {
            "stance": COMPROMISED,
            "quality": 0.0,
            "measurement": obs,
        }

    brightness = float(obs["brightness"])
    if brightness <= float(config["camera"]["compromised_brightness_max"]):
        return {
            "stance": COMPROMISED,
            "quality": 0.0,
            "measurement": {
                **obs,
                "classification": "camera_view_compromised",
            },
        }

    vec = list(obs["mean_bgr"])
    absent = list(config["camera"]["absent_mean_bgr"])
    present = list(config["camera"]["present_mean_bgr"])
    d_absent = _distance(vec, absent)
    d_present = _distance(vec, present)
    separation = float(config["camera"]["prototype_separation"])
    margin = abs(d_absent - d_present)
    min_margin = float(config["camera"]["classification_margin"])

    if separation <= 1e-9 or margin < min_margin:
        stance = COMPROMISED
        classification = "ambiguous"
        quality = 0.25
    elif d_present < d_absent:
        stance = SUPPORT
        classification = "reference_present"
        quality = min(1.0, margin / max(separation, 1e-9))
    else:
        stance = CONTRADICT
        classification = "reference_absent"
        quality = min(1.0, margin / max(separation, 1e-9))

    return {
        "stance": stance,
        "quality": quality,
        "measurement": {
            **obs,
            "classification": classification,
            "distance_to_present": d_present,
            "distance_to_absent": d_absent,
            "classification_margin_observed": margin,
        },
    }


def _audio_record(seconds: float, sample_rate: int):
    _cv2, np, sd = _deps()
    recording = sd.rec(
        int(seconds * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return np.asarray(recording[:, 0], dtype="float64")


def _tone_playrec(
    *,
    frequency_hz: float,
    seconds: float,
    sample_rate: int,
    amplitude: float,
):
    _cv2, np, sd = _deps()
    t = np.arange(int(seconds * sample_rate), dtype="float64") / sample_rate
    ramp_n = max(1, int(sample_rate * 0.02))
    envelope = np.ones_like(t)
    ramp = np.linspace(0.0, 1.0, ramp_n)
    envelope[:ramp_n] = ramp
    envelope[-ramp_n:] = ramp[::-1]
    tone = amplitude * envelope * np.sin(2 * np.pi * frequency_hz * t)
    recording = sd.playrec(
        tone.reshape(-1, 1).astype("float32"),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return np.asarray(recording[:, 0], dtype="float64")


def _tone_metrics(samples, *, frequency_hz: float, sample_rate: int) -> dict[str, float]:
    _cv2, np, _sd = _deps()
    if len(samples) == 0:
        return {"rms": 0.0, "target_magnitude": 0.0, "snr_ratio": 0.0}

    samples = samples - float(np.mean(samples))
    window = np.hanning(len(samples))
    spectrum = np.fft.rfft(samples * window)
    freqs = np.fft.rfftfreq(len(samples), d=1.0 / sample_rate)
    mags = np.abs(spectrum)

    target_mask = np.abs(freqs - frequency_hz) <= 15.0
    noise_mask = (freqs >= 100.0) & (freqs <= 5000.0) & (~target_mask)

    target = float(np.max(mags[target_mask])) if np.any(target_mask) else 0.0
    noise = float(np.median(mags[noise_mask])) if np.any(noise_mask) else 1e-12
    rms = float(np.sqrt(np.mean(samples**2)))
    return {
        "rms": rms,
        "target_magnitude": target,
        "snr_ratio": target / max(noise, 1e-12),
    }


def audio_verify_tone(config: dict[str, Any], *, play: bool = True) -> dict[str, Any]:
    audio = config["audio"]
    sample_rate = int(audio["sample_rate"])
    seconds = float(audio["seconds"])
    frequency = float(audio["frequency_hz"])

    if play:
        samples = _tone_playrec(
            frequency_hz=frequency,
            seconds=seconds,
            sample_rate=sample_rate,
            amplitude=float(audio["amplitude"]),
        )
    else:
        samples = _audio_record(seconds, sample_rate)

    metrics = _tone_metrics(
        samples,
        frequency_hz=frequency,
        sample_rate=sample_rate,
    )
    threshold = float(audio["snr_ratio_threshold"])
    stance = SUPPORT if metrics["snr_ratio"] >= threshold else CONTRADICT
    quality = min(1.0, metrics["snr_ratio"] / max(threshold, 1e-12))
    return {
        "stance": stance,
        "quality": quality,
        "measurement": {
            **metrics,
            "frequency_hz": frequency,
            "snr_ratio_threshold": threshold,
            "playback_requested": bool(play),
        },
    }


def calibrate(output_path: Path, *, camera_index: int = 0) -> dict[str, Any]:
    print("RIV_001 calibration. This data is calibration-only, not experimental evidence.")
    print("No raw video/audio will be saved.")

    input("\n1/4 Remove the reference object from the centre of the camera view, then press Enter.")
    absent = _camera_roi_mean(camera_index=camera_index)
    if not absent["ok"]:
        raise SystemExit(f"Camera calibration failed: {absent['reason']}")

    input("\n2/4 Place a visually distinctive reference object in the centre region, then press Enter.")
    present = _camera_roi_mean(camera_index=camera_index)
    if not present["ok"]:
        raise SystemExit(f"Camera calibration failed: {present['reason']}")

    separation = _distance(absent["mean_bgr"], present["mean_bgr"])
    if separation < 8.0:
        raise SystemExit(
            "Reference object did not change the camera ROI enough. "
            "Use a more visually distinctive object/background and recalibrate."
        )

    input("\n3/4 Make the room reasonably quiet, then press Enter to measure background audio.")
    background_samples = _audio_record(1.0, 44100)
    background = _tone_metrics(background_samples, frequency_hz=1000.0, sample_rate=44100)

    input(
        "\n4/4 Ensure speakers are unmuted at a comfortable volume. "
        "Press Enter to play a quiet 1000 Hz test tone."
    )
    tone_samples = _tone_playrec(
        frequency_hz=1000.0,
        seconds=1.0,
        sample_rate=44100,
        amplitude=0.05,
    )
    tone = _tone_metrics(tone_samples, frequency_hz=1000.0, sample_rate=44100)

    if tone["snr_ratio"] <= background["snr_ratio"] * 2.0:
        raise SystemExit(
            "The microphone did not distinguish the test tone sufficiently from background. "
            "Check input/output devices or speaker volume and recalibrate."
        )

    threshold = math.sqrt(
        max(background["snr_ratio"], 1e-9) * max(tone["snr_ratio"], 1e-9)
    )

    body = {
        "schema": "riv-laptop-config-v0.01",
        "calibration_only": True,
        "created_utc": _utc_now(),
        "camera": {
            "index": camera_index,
            "frames_per_read": 12,
            "absent_mean_bgr": absent["mean_bgr"],
            "present_mean_bgr": present["mean_bgr"],
            "absent_brightness": absent["brightness"],
            "present_brightness": present["brightness"],
            "prototype_separation": separation,
            "classification_margin": max(2.0, separation * 0.10),
            "compromised_brightness_max": max(
                3.0,
                min(absent["brightness"], present["brightness"]) * 0.15,
            ),
        },
        "audio": {
            "sample_rate": 44100,
            "seconds": 1.0,
            "frequency_hz": 1000.0,
            "amplitude": 0.05,
            "background_snr_ratio": background["snr_ratio"],
            "calibration_tone_snr_ratio": tone["snr_ratio"],
            "snr_ratio_threshold": threshold,
        },
    }
    body["config_sha256"] = _canonical_hash(body)
    output_path.write_text(json.dumps(body, indent=2), encoding="utf-8")
    print(f"\nFrozen calibration written to {output_path}")
    print(f"SHA-256: {body['config_sha256']}")
    return body


def _load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    expected = data.get("config_sha256")
    unsigned = dict(data)
    unsigned.pop("config_sha256", None)
    actual = _canonical_hash(unsigned)
    if expected != actual:
        raise SystemExit(
            "Calibration config hash mismatch. Refusing to run with a modified config."
        )
    return data


def _camera_observation(config: dict[str, Any], *, root: str) -> Observation:
    result = camera_classify(config)
    return Observation(
        observation_id=f"{root}-camera-classification",
        root_source_id=root,
        modality="camera",
        stance=result["stance"],
        relevant_claim="reference card present",
        measurement=result["measurement"],
        quality=float(result["quality"]),
    )


def run_guided(config_path: Path, output_path: Path) -> dict[str, Any]:
    config = _load_config(config_path)
    results: dict[str, Any] = {
        "schema": "riv-001-live-results-v0.01",
        "started_utc": _utc_now(),
        "config_sha256": config["config_sha256"],
        "raw_media_retained": False,
        "cases": [],
    }

    print("RIV_001 live guided run.")
    print("Raw camera frames and microphone recordings are not saved.\n")

    input("C1: Place the calibrated reference object in the centre, then press Enter.")
    c1 = EvidenceLedger("reference card present")
    c1.add_narrative("The reference card is present.", source="operator")
    c1.add_observation(_camera_observation(config, root="C1-camera-read"))
    c1_packet = c1.packet()
    c1_membrane = evaluate_crossing(request_from_riv_packet(c1_packet)).packet()
    results["cases"].append({"case_id": "RIV001-C1", "riv": c1_packet, "membrane": c1_membrane})

    input("\nC2: Remove the reference object. The test will repeat the claim 20 times. Press Enter.")
    c2 = EvidenceLedger("reference card present")
    for _ in range(20):
        c2.add_narrative("The reference card is present.", source="scripted-narrative")
    c2.add_observation(_camera_observation(config, root="C2-camera-read"))
    c2_packet = c2.packet()
    c2_membrane = evaluate_crossing(request_from_riv_packet(c2_packet)).packet()
    results["cases"].append({"case_id": "RIV001-C2", "riv": c2_packet, "membrane": c2_membrane})

    input("\nC3: Ensure speakers are unmuted at a comfortable volume, then press Enter.")
    c3_result = audio_verify_tone(config, play=True)
    c3 = EvidenceLedger("tone physically produced")
    c3.add_narrative("Playback command completed.", source="system-telemetry")
    c3.add_observation(
        Observation(
            observation_id="C3-mic-tone-detector",
            root_source_id="C3-mic-capture",
            modality="microphone",
            stance=c3_result["stance"],
            relevant_claim="tone physically produced",
            measurement=c3_result["measurement"],
            quality=float(c3_result["quality"]),
        )
    )
    c3_packet = c3.packet()
    results["cases"].append(
        {
            "case_id": "RIV001-C3",
            "riv": c3_packet,
            "action_effect_state": c3.action_effect_state(),
        }
    )

    input(
        "\nC4: Mute or physically turn down the speakers while leaving software audio enabled. "
        "Press Enter; the command will still be issued."
    )
    c4_result = audio_verify_tone(config, play=True)
    c4 = EvidenceLedger("tone physically produced")
    c4.add_narrative("Playback command completed.", source="system-telemetry")
    c4.add_observation(
        Observation(
            observation_id="C4-mic-tone-detector",
            root_source_id="C4-mic-capture",
            modality="microphone",
            stance=c4_result["stance"],
            relevant_claim="tone physically produced",
            measurement=c4_result["measurement"],
            quality=float(c4_result["quality"]),
        )
    )
    c4_packet = c4.packet()
    results["cases"].append(
        {
            "case_id": "RIV001-C4",
            "riv": c4_packet,
            "action_effect_state": c4.action_effect_state(),
        }
    )

    input("\nC5: Restore speakers. Press Enter to create two reports from one microphone capture.")
    c5_result = audio_verify_tone(config, play=True)
    c5 = EvidenceLedger("tone physically produced")
    c5.add_observation(
        Observation(
            observation_id="C5-raw-detector",
            root_source_id="C5-mic-capture",
            modality="microphone",
            stance=c5_result["stance"],
            relevant_claim="tone physically produced",
            measurement=c5_result["measurement"],
            quality=float(c5_result["quality"]),
        )
    )
    c5.add_observation(
        Observation(
            observation_id="C5-derived-report",
            root_source_id="C5-mic-capture",
            modality="derived_audio_report",
            stance=c5_result["stance"],
            relevant_claim="tone physically produced",
            measurement={"derived_from_same_capture": True},
            quality=float(c5_result["quality"]),
            raw_or_derived="derived",
            derived_from=("C5-raw-detector",),
        )
    )
    c5_packet = c5.packet()
    c5_membrane = evaluate_crossing(request_from_riv_packet(c5_packet)).packet()
    results["cases"].append({"case_id": "RIV001-C5", "riv": c5_packet, "membrane": c5_membrane})

    input("\nC6a: Place the reference object in the centre and press Enter.")
    c6_old = EvidenceLedger("reference card present")
    c6_old.add_observation(_camera_observation(config, root="C6-old-camera-read"))
    input("C6b: Now remove the object and press Enter.")
    c6_new = EvidenceLedger("reference card present")
    c6_new.add_observation(_camera_observation(config, root="C6-new-camera-read"))
    results["cases"].append(
        {
            "case_id": "RIV001-C6",
            "earlier": c6_old.packet(),
            "current": c6_new.packet(),
            "provenance_preserved": True,
        }
    )

    input("\nC7: Cover the camera lens fully, then press Enter.")
    c7 = EvidenceLedger("reference card present")
    c7.add_narrative("The reference card is present.", source="operator")
    c7.add_observation(_camera_observation(config, root="C7-covered-camera-read"))
    c7_packet = c7.packet()
    results["cases"].append({"case_id": "RIV001-C7", "riv": c7_packet})

    input(
        "\nC8: Uncover camera. Keep speakers unmuted. "
        "The narrative claim will be 'the room is silent' while a test tone is played. Press Enter."
    )
    c8_result = audio_verify_tone(config, play=True)
    c8 = EvidenceLedger("room is silent")
    c8.add_narrative("The room is silent.", source="scripted-narrative")
    c8.add_observation(
        Observation(
            observation_id="C8-mic-sound-detector",
            root_source_id="C8-mic-capture",
            modality="microphone",
            stance=CONTRADICT if c8_result["stance"] == SUPPORT else SUPPORT,
            relevant_claim="room is silent",
            measurement=c8_result["measurement"],
            quality=float(c8_result["quality"]),
        )
    )
    c8_packet = c8.packet()
    c8_membrane = evaluate_crossing(request_from_riv_packet(c8_packet)).packet()
    results["cases"].append({"case_id": "RIV001-C8", "riv": c8_packet, "membrane": c8_membrane})

    results["completed_utc"] = _utc_now()
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults written to {output_path}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="RIV_001 live laptop harness")
    sub = parser.add_subparsers(dest="command", required=True)

    p_cal = sub.add_parser("calibrate", help="calibrate and freeze laptop thresholds")
    p_cal.add_argument("--out", default="riv_001_calibration.json")
    p_cal.add_argument("--camera-index", type=int, default=0)

    p_run = sub.add_parser("run", help="run guided RIV_001 hardware cases")
    p_run.add_argument("--config", default="riv_001_calibration.json")
    p_run.add_argument("--out", default="riv_001_live_results.json")

    args = parser.parse_args()
    if args.command == "calibrate":
        calibrate(Path(args.out), camera_index=args.camera_index)
    elif args.command == "run":
        run_guided(Path(args.config), Path(args.out))


if __name__ == "__main__":
    main()
