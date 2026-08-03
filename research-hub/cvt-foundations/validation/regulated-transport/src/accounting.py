from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad

from .model import SimulationResult, rates


@dataclass(frozen=True)
class Accounting:
    delivered: float
    productive: float
    rejected: float
    initial_free_and_buffered: float
    terminal_free_and_buffered: float
    residual: float
    tolerance: float

    @property
    def valid(self) -> bool:
        return abs(self.residual) <= self.tolerance


def integrate(t: np.ndarray, rate: np.ndarray) -> float:
    return float(np.trapezoid(rate, t))


def _channel_integral(result: SimulationResult, channel: str) -> float:
    def integrand(t: float) -> float:
        state = result.dense_solution(t)
        return rates(t, state, result.params, result.schedule)[1][channel]

    value, _ = quad(
        integrand,
        0.0,
        result.config.t_end,
        epsabs=1e-10,
        epsrel=1e-9,
        points=[result.config.t_intervention],
        limit=300,
    )
    return float(value)


def accounting(result: SimulationResult) -> Accounting:
    delivered = _channel_integral(result, "j_raw")
    productive = float(result.p[-1] - result.p[0])
    rejected = _channel_integral(result, "j_reject")
    initial_mass = float(result.c_a[0] + result.u[0])
    terminal_mass = float(result.c_a[-1] + result.u[-1])
    residual = delivered + initial_mass - productive - rejected - terminal_mass
    tolerance = max(1e-8, 1e-6 * max(delivered, 1.0))
    return Accounting(
        delivered=delivered,
        productive=productive,
        rejected=rejected,
        initial_free_and_buffered=initial_mass,
        terminal_free_and_buffered=terminal_mass,
        residual=residual,
        tolerance=tolerance,
    )
