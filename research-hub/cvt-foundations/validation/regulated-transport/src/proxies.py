from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad

from .model import InitialState, Parameters, SimulationConfig, rates, simulate
from .schedules import Forcing, pulse


@dataclass(frozen=True)
class ProxyConfig:
    j_low: float = 0.5
    j_high: float = 2.5
    overload_width: float = 2.5
    probe_c_b: float = 1.0
    probe_permeability: float = 0.25
    probe_duration: float = 0.25


@dataclass(frozen=True)
class ProxySet:
    g_b: float
    g_q: float
    g_c_direct: float
    g_c_probe: float
    g_s: float
    probe_delivered: float
    probe_productive: float


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
    capacity_headroom = max(0.0, 1.0 - initial.p / params.p_cap)
    reserve_factor = initial.s / (params.k_s + initial.s) if initial.s > 0.0 else 0.0
    return float((capacity_headroom * initial.q * reserve_factor) ** (1.0 / 3.0))


def _integrate_channel(result, channel: str, terminal_time: float) -> float:
    breakpoints = [point for point in getattr(result.schedule, "breakpoints", ()) if 0.0 < point < terminal_time]

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


def capture_probe(params: Parameters, initial: InitialState, config: ProxyConfig) -> tuple[float, float, float]:
    schedule = pulse(
        Forcing(config.probe_c_b, config.probe_permeability, t_intervention=config.probe_duration),
        duration=config.probe_duration,
    )
    simulation_config = SimulationConfig(
        t_intervention=config.probe_duration,
        t_follow=0.0,
        dt_out=min(0.01, config.probe_duration / 20.0),
        rtol=1e-8,
        atol=1e-10,
    )
    result = simulate(schedule, params=params, initial=initial, config=simulation_config)
    delivered = _integrate_channel(result, "j_raw", config.probe_duration)
    productive = float(result.p[-1] - result.p[0])
    ratio = productive / delivered if delivered > 1e-12 else 0.0
    return float(np.clip(ratio, 0.0, 1.0)), delivered, productive


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
    probe, delivered, productive = capture_probe(params, initial, proxy_config)
    return ProxySet(
        g_b=bounded_coupling(peak, proxy_config),
        g_q=float(np.clip(initial.q, 0.0, 1.0)),
        g_c_direct=capture_direct(params, initial),
        g_c_probe=probe,
        g_s=float(np.clip(initial.s / params.s_max, 0.0, 1.0)),
        probe_delivered=delivered,
        probe_productive=productive,
    )
