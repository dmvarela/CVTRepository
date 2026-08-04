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
    refined: bool = False

    @property
    def valid(self) -> bool:
        return abs(self.residual) <= self.tolerance


def integrate(t: np.ndarray, rate: np.ndarray) -> float:
    return float(np.trapezoid(rate, t))


def _integrand(result: SimulationResult, channel: str):
    def function(time: float) -> float:
        state = result.dense_solution(time)
        return rates(time, state, result.params, result.schedule)[1][channel]

    return function


def _channel_integral_fast(result: SimulationResult, channel: str) -> float:
    breakpoints = [
        point
        for point in getattr(result.schedule, "breakpoints", ())
        if 0.0 < point < result.config.t_end
    ]
    value, _ = quad(
        _integrand(result, channel),
        0.0,
        result.config.t_end,
        epsabs=1e-10,
        epsrel=1e-9,
        points=breakpoints or None,
        limit=300,
    )
    return float(value)


def _channel_integral_refined(
    result: SimulationResult,
    channel: str,
    maximum_width: float = 5.0,
) -> float:
    terminal = result.config.t_end
    regular_points = np.arange(maximum_width, terminal, maximum_width)
    schedule_points = getattr(result.schedule, "breakpoints", ())
    points = sorted(
        {
            0.0,
            terminal,
            *[float(point) for point in regular_points],
            *[
                float(point)
                for point in schedule_points
                if 0.0 < float(point) < terminal
            ],
        }
    )
    function = _integrand(result, channel)
    total = 0.0
    for start, end in zip(points[:-1], points[1:]):
        value, _ = quad(
            function,
            start,
            end,
            epsabs=1e-11,
            epsrel=1e-10,
            limit=200,
        )
        total += value
    return float(total)


def _assemble(
    result: SimulationResult,
    delivered: float,
    rejected: float,
    refined: bool,
) -> Accounting:
    productive = float(result.p[-1] - result.p[0])
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
        refined=refined,
    )


def accounting_refined(result: SimulationResult) -> Accounting:
    """Recompute accounting on bounded subintervals.

    This path is used only when whole-window adaptive quadrature fails the
    frozen conservation tolerance or exceeds the Stage 3.1 time limit.
    """
    return _assemble(
        result,
        _channel_integral_refined(result, "j_raw"),
        _channel_integral_refined(result, "j_reject"),
        True,
    )


def accounting(result: SimulationResult) -> Accounting:
    fast = _assemble(
        result,
        _channel_integral_fast(result, "j_raw"),
        _channel_integral_fast(result, "j_reject"),
        False,
    )
    if fast.valid:
        return fast
    return accounting_refined(result)
