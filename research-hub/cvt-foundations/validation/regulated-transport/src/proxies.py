from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
from scipy.integrate import quad

from .model import InitialState, Parameters, SimulationConfig, rates, simulate
from .schedules import Forcing, pulse


@dataclass(frozen=True)
class ProbeSpec:
    c_b: float = 2.0
    permeability: float = 0.10
    pulse_duration: float = 0.05
    readout_horizon: float = 1.0
    delivered_floor_fraction_pcap: float = 1e-4

    def sensitivity(self) -> "ProbeSpec":
        """Return the frozen 2.5x-dose sensitivity probe."""
        return replace(self, permeability=0.25)


@dataclass(frozen=True)
class ProxyConfig:
    j_low: float = 0.5
    j_high: float = 2.5
    overload_width: float = 2.5
    probe: ProbeSpec = ProbeSpec()


@dataclass(frozen=True)
class ProbeMeasurement:
    score: float
    valid: bool
    delivered: float
    delivered_floor: float
    raw_productive: float
    sham_productive: float
    marginal_productive: float
    raw_ratio: float
    marginal_ratio: float
    incremental_c: float
    incremental_p: float
    incremental_u: float
    incremental_d: float
    incremental_s: float
    incremental_q: float


@dataclass(frozen=True)
class ProxySet:
    g_b: float
    g_q: float
    g_c_direct: float
    g_c_probe: float
    g_s: float
    probe_valid: bool
    probe_delivered: float
    probe_delivered_floor: float
    probe_raw_productive: float
    probe_sham_productive: float
    probe_marginal_productive: float
    probe_raw_ratio: float
    probe_marginal_ratio: float


def scheduled_peak(schedule, initial: InitialState, t_intervention: float, n: int = 1001) -> float:
    times = np.linspace(0.0, t_intervention, n)
    values: list[float] = []
    for time in times:
        c_b, permeability = schedule(float(time))
        values.append(permeability * max(0.0, c_b - initial.c_a))
    return float(max(values, default=0.0))


def bounded_coupling(j_peak: float, config: ProxyConfig) -> float:
    if j_peak <= 0.0:
        return 0.0
    if j_peak < config.j_low:
        return j_peak / config.j_low
    if j_peak <= config.j_high:
        return 1.0
    return max(0.0, 1.0 - (j_peak - config.j_high) / config.overload_width)


def capture_direct(params: Parameters, initial: InitialState) -> float:
    """Stage-2 structural composite retained only as a sensitivity measure."""
    capacity_headroom = max(0.0, 1.0 - initial.p / params.p_cap)
    reserve_factor = initial.s / (params.k_s + initial.s) if initial.s > 0.0 else 0.0
    return float((capacity_headroom * initial.q * reserve_factor) ** (1.0 / 3.0))


def _zero_schedule(time: float) -> tuple[float, float]:
    del time
    return 0.0, 0.0


_zero_schedule.breakpoints = ()  # type: ignore[attr-defined]


def _integrate_channel(result, channel: str, terminal_time: float) -> float:
    breakpoints = [
        point
        for point in getattr(result.schedule, "breakpoints", ())
        if 0.0 < point < terminal_time
    ]

    def integrand(time: float) -> float:
        state = result.dense_solution(time)
        return rates(time, state, result.params, result.schedule)[1][channel]

    value, _ = quad(
        integrand,
        0.0,
        terminal_time,
        points=breakpoints or None,
        epsabs=1e-10,
        epsrel=1e-9,
        limit=200,
    )
    return float(value)


def capture_probe(
    params: Parameters,
    initial: InitialState,
    spec: ProbeSpec | None = None,
    *,
    method: str = "LSODA",
    rtol: float = 1e-8,
    atol: float = 1e-10,
) -> ProbeMeasurement:
    """Measure the marginal productive response to a small pulse.

    The probe run is paired with a zero-input sham from the identical initial
    state. Subtracting sham productive conversion prevents pre-existing free or
    buffered load from being falsely attributed to the probe. Both simulations
    are discarded; the evaluated run starts from the unchanged initial state.
    """
    spec = spec or ProbeSpec()
    if spec.readout_horizon < spec.pulse_duration:
        raise ValueError("readout_horizon must be at least pulse_duration")

    probe_schedule = pulse(
        Forcing(spec.c_b, spec.permeability, t_intervention=spec.readout_horizon),
        duration=spec.pulse_duration,
    )
    simulation_config = SimulationConfig(
        t_intervention=spec.readout_horizon,
        t_follow=0.0,
        dt_out=min(0.005, spec.readout_horizon / 100.0),
        rtol=rtol,
        atol=atol,
        method=method,
    )
    probe_result = simulate(probe_schedule, params=params, initial=initial, config=simulation_config)
    sham_result = simulate(_zero_schedule, params=params, initial=initial, config=simulation_config)

    delivered = _integrate_channel(probe_result, "j_raw", spec.readout_horizon)
    raw_productive = float(probe_result.p[-1] - probe_result.p[0])
    sham_productive = float(sham_result.p[-1] - sham_result.p[0])
    marginal_productive = raw_productive - sham_productive
    delivered_floor = spec.delivered_floor_fraction_pcap * params.p_cap
    signal_valid = bool(delivered >= delivered_floor)

    raw_ratio = raw_productive / delivered if delivered > 0.0 else float("nan")
    marginal_ratio = marginal_productive / delivered if signal_valid else float("nan")
    ratio_valid = bool(
        signal_valid
        and np.isfinite(marginal_ratio)
        and -1e-8 <= marginal_ratio <= 1.0 + 1e-8
    )
    valid = ratio_valid
    score = float(np.clip(marginal_ratio, 0.0, 1.0)) if valid else float("nan")
    incremental = probe_result.y[:, -1] - sham_result.y[:, -1]

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


def compute(
    schedule,
    params: Parameters,
    initial: InitialState,
    simulation_config: SimulationConfig | None = None,
    proxy_config: ProxyConfig | None = None,
) -> ProxySet:
    simulation_config = simulation_config or SimulationConfig()
    proxy_config = proxy_config or ProxyConfig()
    peak = scheduled_peak(schedule, initial, simulation_config.t_intervention)
    probe = capture_probe(params, initial, proxy_config.probe)
    return ProxySet(
        g_b=bounded_coupling(peak, proxy_config),
        g_q=float(np.clip(initial.q, 0.0, 1.0)),
        g_c_direct=capture_direct(params, initial),
        g_c_probe=probe.score,
        g_s=float(np.clip(initial.s / params.s_max, 0.0, 1.0)),
        probe_valid=probe.valid,
        probe_delivered=probe.delivered,
        probe_delivered_floor=probe.delivered_floor,
        probe_raw_productive=probe.raw_productive,
        probe_sham_productive=probe.sham_productive,
        probe_marginal_productive=probe.marginal_productive,
        probe_raw_ratio=probe.raw_ratio,
        probe_marginal_ratio=probe.marginal_ratio,
    )
