from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Callable

import numpy as np
from scipy.integrate import solve_ivp

Array = np.ndarray
Schedule = Callable[[float], tuple[float, float]]


@dataclass(frozen=True)
class Parameters:
    p_cap: float = 8.0
    u_max: float = 5.0
    k_p: float = 0.9
    k_b: float = 0.6
    k_rel: float = 0.2
    k_e: float = 0.4
    s_max: float = 6.0
    r_s: float = 0.05
    k_rep: float = 0.2
    r_q: float = 0.04
    c_safe: float = 1.0
    u_safe: float = 3.5
    c_q: float = 2.0
    j_safe: float = 1.5
    k_s: float = 1.0
    k_q: float = 0.5
    s_export: float = 1.5
    k_rep_half: float = 1.0
    k_qs: float = 1.0
    k_d1: float = 0.10
    k_d2: float = 0.08
    k_d3: float = 0.04
    a_p: float = 0.06
    a_e: float = 0.04
    a_b: float = 0.03
    a_r: float = 0.08
    b_d: float = 0.12
    b_l: float = 0.08
    h: float = 0.5
    include_direct_flux_damage: bool = True
    q_modulates_flux: bool = True


@dataclass(frozen=True)
class InitialState:
    c_a: float = 0.0
    p: float = 0.0
    u: float = 0.0
    d: float = 0.0
    s: float = 4.5
    q: float = 0.9

    def as_array(self) -> Array:
        return np.array([self.c_a, self.p, self.u, self.d, self.s, self.q], dtype=float)


@dataclass(frozen=True)
class SimulationConfig:
    t_intervention: float = 20.0
    t_follow: float = 30.0
    dt_out: float = 0.05
    rtol: float = 1e-7
    atol: float = 1e-9
    method: str = "LSODA"

    @property
    def t_end(self) -> float:
        return self.t_intervention + self.t_follow


@dataclass
class SimulationResult:
    t: Array
    y: Array
    j_raw: Array
    j_prod: Array
    j_buf_in: Array
    j_buf_out: Array
    j_reject: Array
    solver_success: bool
    solver_message: str
    projection_count: int
    params: Parameters
    initial: InitialState
    config: SimulationConfig
    schedule: Schedule
    dense_solution: Callable[[float], Array]

    @property
    def c_a(self) -> Array:
        return self.y[0]

    @property
    def p(self) -> Array:
        return self.y[1]

    @property
    def u(self) -> Array:
        return self.y[2]

    @property
    def d(self) -> Array:
        return self.y[3]

    @property
    def s(self) -> Array:
        return self.y[4]

    @property
    def q(self) -> Array:
        return self.y[5]


def _clip_state(y: Array, p: Parameters) -> tuple[Array, int]:
    lower = np.zeros(6)
    upper = np.array([np.inf, np.inf, p.u_max, 1.0, p.s_max, 1.0])
    clipped = np.minimum(np.maximum(y, lower), upper)
    return clipped, int(np.count_nonzero(np.abs(clipped - y) > 1e-12))


def rates(t: float, y: Array, p: Parameters, schedule: Schedule) -> tuple[Array, dict[str, float], int]:
    state, projections = _clip_state(y, p)
    c_a, p_pool, u, d, s, q = state
    c_b, permeability = schedule(t)

    q_factor = q if p.q_modulates_flux else 1.0
    j_raw = max(0.0, permeability * q_factor * (c_b - c_a))

    f_cap = max(0.0, 1.0 - p_pool / p.p_cap)
    f_res = s / (p.k_s + s) if s > 0 else 0.0
    f_int = q / (p.k_q + q) if q > 0 else 0.0
    f_export = min(1.0, s / p.s_export) if p.s_export > 0 else 0.0

    j_prod = p.k_p * c_a * f_cap * f_res * f_int
    j_buf_in = p.k_b * c_a * max(0.0, 1.0 - u / p.u_max)
    j_buf_out = p.k_rel * u * f_res * f_int
    j_reject = p.k_e * c_a * f_export

    repair = p.k_rep * p.h * (s / (p.k_rep_half + s) if s > 0 else 0.0) * d
    direct_flux_damage = p.k_d3 * max(0.0, j_raw - p.j_safe) if p.include_direct_flux_damage else 0.0

    dc_a = j_raw + j_buf_out - j_prod - j_buf_in - j_reject
    dp_pool = j_prod
    du = j_buf_in - j_buf_out
    dd = (
        p.k_d1 * max(0.0, c_a - p.c_safe)
        + p.k_d2 * max(0.0, u - p.u_safe)
        + direct_flux_damage
        - repair
    )
    ds = (
        p.r_s * p.h * (p.s_max - s)
        - p.a_p * j_prod
        - p.a_e * j_reject
        - p.a_b * j_buf_out
        - p.a_r * repair
    )
    dq = (
        p.r_q * p.h * (s / (p.k_qs + s) if s > 0 else 0.0) * (1.0 - q)
        - p.b_d * d * q
        - p.b_l * max(0.0, c_a - p.c_q) * q
    )

    deriv = np.array([dc_a, dp_pool, du, dd, ds, dq], dtype=float)
    if c_a <= 0 and deriv[0] < 0:
        deriv[0] = 0.0
    if u <= 0 and deriv[2] < 0:
        deriv[2] = 0.0
    if u >= p.u_max and deriv[2] > 0:
        deriv[2] = 0.0
    if d <= 0 and deriv[3] < 0:
        deriv[3] = 0.0
    if d >= 1 and deriv[3] > 0:
        deriv[3] = 0.0
    if s <= 0 and deriv[4] < 0:
        deriv[4] = 0.0
    if s >= p.s_max and deriv[4] > 0:
        deriv[4] = 0.0
    if q <= 0 and deriv[5] < 0:
        deriv[5] = 0.0
    if q >= 1 and deriv[5] > 0:
        deriv[5] = 0.0

    channels = {
        "j_raw": j_raw,
        "j_prod": j_prod,
        "j_buf_in": j_buf_in,
        "j_buf_out": j_buf_out,
        "j_reject": j_reject,
    }
    return deriv, channels, projections


def simulate(
    schedule: Schedule,
    params: Parameters | None = None,
    initial: InitialState | None = None,
    config: SimulationConfig | None = None,
) -> SimulationResult:
    p = params or Parameters()
    init = initial or InitialState(s=0.75 * p.s_max)
    cfg = config or SimulationConfig()
    t_eval = np.arange(0.0, cfg.t_end + cfg.dt_out / 2.0, cfg.dt_out)
    projection_counter = 0

    def rhs(t: float, y: Array) -> Array:
        nonlocal projection_counter
        deriv, _, count = rates(t, y, p, schedule)
        projection_counter += count
        return deriv

    sol = solve_ivp(
        rhs,
        (0.0, cfg.t_end),
        init.as_array(),
        method=cfg.method,
        t_eval=t_eval,
        rtol=cfg.rtol,
        atol=cfg.atol,
        dense_output=True,
    )
    if sol.y.shape[1] != t_eval.size:
        raise RuntimeError(f"Integration returned {sol.y.shape[1]} points, expected {t_eval.size}: {sol.message}")

    clipped_columns = []
    output_projection_count = 0
    for column in sol.y.T:
        clipped, count = _clip_state(column, p)
        clipped_columns.append(clipped)
        output_projection_count += count
    y = np.asarray(clipped_columns).T

    channels = [rates(float(t), y[:, i], p, schedule)[1] for i, t in enumerate(sol.t)]
    arrays = {name: np.array([row[name] for row in channels]) for name in channels[0]}

    return SimulationResult(
        t=sol.t,
        y=y,
        j_raw=arrays["j_raw"],
        j_prod=arrays["j_prod"],
        j_buf_in=arrays["j_buf_in"],
        j_buf_out=arrays["j_buf_out"],
        j_reject=arrays["j_reject"],
        solver_success=bool(sol.success),
        solver_message=str(sol.message),
        projection_count=projection_counter + output_projection_count,
        params=p,
        initial=init,
        config=cfg,
        schedule=schedule,
        dense_solution=sol.sol,
    )


def with_sensitivity(params: Parameters, *, remove_flux_damage: bool = False, remove_q_flux: bool = False) -> Parameters:
    return replace(
        params,
        include_direct_flux_damage=not remove_flux_damage,
        q_modulates_flux=not remove_q_flux,
    )
