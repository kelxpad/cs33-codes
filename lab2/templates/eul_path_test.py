from functools import wraps
from itertools import count
from random import Random

from hierholzer import hierholzer
from fleury import find_eul_path as fleury_find_path

def other(edge, i):
    a, b = edge
    assert i in {a, b}
    return b if i == a else a


def test_eul_path_vertices(n, edges, start, vertex_path):
    # path must use exactly |edges| edges -> vertices = edges + 1
    assert len(vertex_path) == len(edges) + 1

    used = [0] * len(edges)
    cur = start
    
    for nxt in vertex_path[1:]:
        found = False

        # find an unused edge connecting cur -> nxt
        for idx, (a, b) in enumerate(edges):
            if not used[idx] and ((a == cur and b == nxt) or (a == nxt and b == cur)):
                used[idx] = 1
                cur = nxt
                found = True
                break
        
        assert found, "Invalid edge traversal"

    assert all(used), "Not all edges were used"

def hierholzer_adapter(n, edges):
    deg = [0]*n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    odd = [i for i in range(n) if deg[i] % 2]

    if len(odd) == 0:
        start = next((i for i in range(n) if deg[i] > 0), 0)
    elif len(odd) == 2:
        start = odd[0]
    else:
        raise ValueError

    path, edge_indices = hierholzer(n, edges, start)

    if len(path) != len(edges) + 1:
        raise ValueError

    return start, path

def fleury_adapter(n, edges):
    start, edge_path = fleury_find_path(n, edges)

    # convert edge indices to vertex sequence
    vertex_path = [start]
    cur = start
    for idx in edge_path:
        cur = other(edges[idx], cur)
        vertex_path.append(cur)

    if len(vertex_path) != len(edges) + 1:
        raise ValueError("Fleury returned invalid path length")

    return start, vertex_path

def graph_has_euler_path(n, edges):
    """
    Ground truth: check connectivity + Euler degree condition.
    """
    relevant_nodes = {i for edge in edges for i in edge} or {0}
    adj = {i: [] for i in relevant_nodes}

    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)

    s = next(iter(relevant_nodes))
    stack = [s]
    visited = {s}

    while stack:
        i = stack.pop()
        for j in adj[i]:
            if j not in visited:
                visited.add(j)
                stack.append(j)

    return (
        visited == relevant_nodes and
        sum(len(adj[i]) % 2 for i in relevant_nodes) in {0, 2}
    )


def with_test_eul_path(find_path):
    """
    Wrap solver:
    - returns False if no Euler path should exist
    - validates only when path should exist
    """
    @wraps(find_path)
    def wrapper(n, edges):
        expected = graph_has_euler_path(n, edges)

        try:
            s, seq = find_path(n, edges)
        except ValueError:
            return False

        if not expected:
            # algorithm returned a path when none should exist
            return False

        test_eul_path_vertices(n, edges, s, seq)
        return True

    return wrapper


sols = (
    graph_has_euler_path,            # ground truth
    with_test_eul_path(hierholzer_adapter),
    with_test_eul_path(fleury_adapter),
)


def main():
    rand = Random(33)

    for cas in count():
        n = rand.randint(1, 2**rand.randint(2, 5))
        e = rand.randint(1, 2**rand.randint(2, 8) + 2)

        def rand_edge():
            return tuple(rand.choices(range(n), k=2))

        edges = [rand_edge() for _ in range(e)]

        answers = [sol(n, edges) for sol in sols]
        answer = answers[0]

        print(f"Case {cas}: n={n} e={e} answer={answer}")

        assert all(ans == answer for ans in answers), answers


if __name__ == "__main__":
    main()