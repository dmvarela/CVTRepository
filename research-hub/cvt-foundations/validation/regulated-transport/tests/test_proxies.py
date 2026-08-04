from src.model import InitialState, Parameters, SimulationConfig
from src.proxies import capture_direct, compute
from src.schedules import Forcing, constant


def test_all_proxies_are_bounded() -> None:
    params = Parameters()
    initial = InitialState()
    proxies = compute(constant(Forcing(2.0, 0.5)), params, initial)
    assert all(
        0.0 <= value <= 1.0
        for value in [
            proxies.g_b,
            proxies.g_q,
            proxies.g_c_direct,
            proxies.g_c_probe,
            proxies.g_s,
        ]
    )


def test_direct_capture_increases_with_q_and_s() -> None:
    params = Parameters()
    lower = InitialState(q=0.4, s=1.0)
    higher = InitialState(q=0.9, s=5.0)
    assert capture_direct(params, higher) > capture_direct(params, lower)


def test_probe_does_not_mutate_evaluated_initial_state() -> None:
    params = Parameters()
    initial = InitialState(c_a=0.2, p=0.3, u=0.1, d=0.1, s=4.0, q=0.8)
    proxies = compute(
        constant(Forcing(2.0, 0.5)),
        params,
        initial,
        SimulationConfig(t_intervention=5.0, t_follow=0.0),
    )
    assert initial == InitialState(c_a=0.2, p=0.3, u=0.1, d=0.1, s=4.0, q=0.8)
    assert proxies.probe_delivered >= 0.0


def test_proxy_construction_is_deterministic() -> None:
    params = Parameters()
    initial = InitialState(c_a=0.1, p=0.2, u=0.2, d=0.05, s=3.0, q=0.75)
    schedule = constant(Forcing(3.0, 0.4))
    first = compute(schedule, params, initial)
    second = compute(schedule, params, initial)
    assert first == second
