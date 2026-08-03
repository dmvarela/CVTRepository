from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

Schedule = Callable[[float], tuple[float, float]]


@dataclass(frozen=True)
class Forcing:
    c_b: float
    permeability: float
    t_intervention: float = 20.0


def constant(forcing: Forcing) -> Schedule:
    def schedule(t: float) -> tuple[float, float]:
        if t <= forcing.t_intervention:
            return forcing.c_b, forcing.permeability
        return 0.0, 0.0
    return schedule


def pulse(forcing: Forcing, duration: float = 3.0, start: float = 0.0) -> Schedule:
    def schedule(t: float) -> tuple[float, float]:
        active = start <= t <= start + duration
        return (forcing.c_b, forcing.permeability) if active else (0.0, 0.0)
    return schedule


def repeated_pulse(forcing: Forcing, duration: float = 3.0, starts: tuple[float, ...] = (0.0, 7.0, 14.0)) -> Schedule:
    def schedule(t: float) -> tuple[float, float]:
        active = any(start <= t <= start + duration for start in starts)
        return (forcing.c_b, forcing.permeability) if active else (0.0, 0.0)
    return schedule


def ramp(forcing: Forcing) -> Schedule:
    def schedule(t: float) -> tuple[float, float]:
        if 0.0 <= t <= forcing.t_intervention:
            fraction = t / forcing.t_intervention
            return forcing.c_b * fraction, forcing.permeability
        return 0.0, 0.0
    return schedule


def shock_tail(forcing: Forcing, shock_duration: float = 2.0, tail_fraction: float = 0.35) -> Schedule:
    def schedule(t: float) -> tuple[float, float]:
        if 0.0 <= t <= shock_duration:
            return forcing.c_b, forcing.permeability
        if shock_duration < t <= forcing.t_intervention:
            return forcing.c_b * tail_fraction, forcing.permeability
        return 0.0, 0.0
    return schedule
