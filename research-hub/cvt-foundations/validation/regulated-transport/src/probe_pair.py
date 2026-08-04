from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from .model import InitialState, Parameters, rates
from .proxies import ProbeMeasurement, ProbeSpec, _zero_schedule
from .schedules import Forcing, pulse


def capture_probe_pair_combined(
    params: Parameters,
    initial: InitialState,
    primary: ProbeSpec | None = None,
    sensitivity: ProbeSpec | None = None,
    *,
    method: str = "BDF",
    rtol: float = 1e-8,
    atol: float = 1e-10,
) -> tuple[ProbeMeasurement, ProbeMeasurement]:
    """Evaluate two probes against one shared zero-input sham.

    Primary, sensitivity, and sham copies are integrated together. Delivered
    load is an auxiliary cumulative state, not part of the native host state.
    The pulse end is an explicit integration boundary.
    """
    primary = primary or ProbeSpec()
    sensitivity = sensitivity or primary.sensitivity()
    if primary.readout_horizon != sensitivity.readout_horizon:
        raise ValueError("paired probes must share a readout horizon")
    if primary.pulse_duration != sensitivity.pulse_duration:
        raise ValueError("paired probes must share a pulse duration")

    horizon = primary.readout_horizon
    pulse_end = primary.pulse_duration
    if horizon < pulse_end:
        raise ValueError("readout horizon must cover the pulse")

    primary_schedule = pulse(
        Forcing(primary.c_b, primary.permeability, t_intervention=horizon),
        duration=pulse_end,
    )
    sensitivity_schedule = pulse(
        Forcing(sensitivity.c_b, sensitivity.permeability, t_intervention=horizon),
        duration=pulse_end,
    )
    schedules = (primary_schedule, sensitivity_schedule, _zero_schedule)
    base = initial.as_array()
    current = np.concatenate(
        [np.r_[base, 0.0], np.r_[base, 0.0], np.r_[base, 0.0]]
    )

    def rhs(time: float, vector: np.ndarray) -> np.ndarray:
        pieces: list[np.ndarray] = []
        for index, schedule in enumerate(schedules):
            block = vector[index * 7 : index * 7 + 6]
            derivative, channels, _ = rates(time, block, params, schedule)
            delivered_rate = channels["j_raw"] if index < 2 else 0.0
            pieces.append(np.r_[derivative, delivered_rate])
        return np.concatenate(pieces)

    segments = [(0.0, pulse_end)]
    if horizon > pulse_end:
        segments.append((pulse_end, horizon))
    for start, end in segments:
        solution = solve_ivp(
            rhs,
            (start, end),
            current,
            method=method,
            rtol=rtol,
            atol=atol,
            t_eval=[end],
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        current = solution.y[:, -1]

    sham_state = current[14:20]
    sham_productive = float(sham_state[1] - initial.p)

    def measurement(index: int, spec: ProbeSpec) -> ProbeMeasurement:
        start = index * 7
        state = current[start : start + 6]
        delivered = float(current[start + 6])
        raw_productive = float(state[1] - initial.p)
        marginal_productive = raw_productive - sham_productive
        delivered_floor = spec.delivered_floor_fraction_pcap * params.p_cap
        signal_valid = bool(delivered >= delivered_floor)
        marginal_ratio = (
            marginal_productive / delivered if signal_valid else float("nan")
        )
        valid = bool(
            signal_valid
            and np.isfinite(marginal_ratio)
            and -1e-8 <= marginal_ratio <= 1.0 + 1e-8
        )
        score = (
            float(np.clip(marginal_ratio, 0.0, 1.0))
            if valid
            else float("nan")
        )
        raw_ratio = raw_productive / delivered if delivered > 0.0 else float("nan")
        incremental = state - sham_state
        return ProbeMeasurement(
            score=score,
            valid=valid,
            delivered=delivered,
            delivered_floor=delivered_floor,
            raw_productive=raw_productive,
            sham_productive=sham_productive,
            marginal_productive=marginal_productive,
            raw_ratio=raw_ratio,
            marginal_ratio=marginal_ratio,
            incremental_c=float(incremental[0]),
            incremental_p=float(incremental[1]),
            incremental_u=float(incremental[2]),
            incremental_d=float(incremental[3]),
            incremental_s=float(incremental[4]),
            incremental_q=float(incremental[5]),
        )

    return measurement(0, primary), measurement(1, sensitivity)
