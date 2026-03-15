from oj import Conduit # pyright: ignore
from lab04a import find_safe_thermal_flow


def check_feasibility(n, conduits):
    rates = find_safe_thermal_flow(n, conduits)
    assert rates is not None, f"failed check: {n=} {conduits=} {rates=}"
    junctions = range(1, n + 1)
    assert all(c.l <= e <= c.u for c, e in zip(conduits, rates, strict=True)), f"failed check: {n=} {conduits=} {rates=}"
    total_in = {i: 0 for i in junctions}
    total_out = {i: 0 for i in junctions}
    for c, e in zip(conduits, rates, strict=True):
        if e >= 0:
            total_out[c.x] += e
            total_in[c.y] += e
        else:
            total_out[c.y] += abs(e)
            total_in[c.x] += abs(e)
    assert all(total_in[i] == total_out[i] for i in junctions), f"failed check: {n=} {conduits=} {rates=}"


def test_feasible():
    check_feasibility(4, (  # subtasks: 1 2 3 4
        Conduit(1, 3, 0, 7),
        Conduit(3, 1, 2, 2),
    ))

    check_feasibility(4, (  # subtasks: 2 3 4
        Conduit(1, 3, 7, 11),
        Conduit(3, 2, 0, 7),
        Conduit(2, 1, 0, 6),
        Conduit(3, 1, 0, 5),
    ))

    check_feasibility(3, (  # subtasks: 3 4
        Conduit(1, 2, 2, 5),
        Conduit(2, 3, 1, 4),
        Conduit(3, 1, 2, 3),
    ))

    check_feasibility(4, (  # subtasks: 3 4
        Conduit(1, 2, 0, 5),
        Conduit(1, 3, 0, 5),
        Conduit(2, 4, 2, 4),
        Conduit(3, 4, 2, 4),
        Conduit(4, 1, 4, 8),
    ))

    # TODO add more tests


def test_infeasible():
    assert find_safe_thermal_flow(2, (  # subtasks: 2 3 4
            Conduit(1, 2, 3, 5),
            Conduit(2, 1, 0, 2),
        )) is None

    # TODO add more tests
