from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .model import SimulationResult


@dataclass(frozen=True)
class Thresholds:
    x_crit: float = 4.0
    d_max: float = 0.45
    q_min: float = 0.55
    c_max: float = 5.0
    s_terminal_fraction: float = 0.15


@dataclass(frozen=True)
class Outcome:
    target_reached: bool
    viable: bool
    hosted: bool
    productive_at_intervention: float
    peak_damage: float
    minimum_integrity: float
    peak_free_load: float
    terminal_reserve: float


def evaluate(result: SimulationResult, thresholds: Thresholds | None = None) -> Outcome:
    th = thresholds or Thresholds()
    index = int(np.searchsorted(result.t, result.config.t_intervention, side="right") - 1)
    productive = float(result.p[index] - result.p[0])
    target = productive >= th.x_crit
    viable = bool(
        np.max(result.d) <= th.d_max
        and np.min(result.q) >= th.q_min
        and np.max(result.c_a) <= th.c_max
        and np.max(result.u) <= result.params.u_max + 1e-9
        and result.s[-1] >= th.s_terminal_fraction * result.params.s_max
    )
    return Outcome(
        target_reached=target,
        viable=viable,
        hosted=target and viable,
        productive_at_intervention=productive,
        peak_damage=float(np.max(result.d)),
        minimum_integrity=float(np.min(result.q)),
        peak_free_load=float(np.max(result.c_a)),
        terminal_reserve=float(result.s[-1]),
    )
