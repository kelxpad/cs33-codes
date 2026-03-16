from dataclasses import dataclass
from collections import deque
from collections.abc import Sequence
type Cell = tuple[int, int]

@dataclass
class Edge:
    u: object
    v: object
    cap: int
    flow: int
    reverse: "Edge | None"

def find_path(nadj, s, t):
    parent = {node: None for node in nadj}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            path = []
            cur = t
            while cur != s:
                e = parent[cur]
                path.append(e)
                cur = e.u
            path.reverse()
            return path
        for e in nadj[u]:
            if parent[e.v] is None and e.v != s and (e.cap - e.flow) > 0:
                parent[e.v] = e
                q.append(e.v)
    return []

def max_flow(adj, s, t):
    nadj = {node: [] for node in adj}
    for u in adj:
        for e in adj[u]:
            fe = Edge(e.u, e.v, e.cap, e.flow, None)
            re = Edge(e.v, e.u, 0, 0, fe)
            fe.reverse = re
            nadj[u].append(fe)
            nadj[e.v].append(re)
    flow = 0
    while True:
        path = find_path(nadj, s, t)
        if not path:
            break
        bottleneck = min(e.cap - e.flow for e in path)
        if bottleneck <= 0:
            break
        for e in path:
            e.flow += bottleneck
            e.reverse.flow -= bottleneck
        flow += bottleneck
    return flow, nadj

delta = (
    (1, -2),
    (-1, 2),
    (1, 2),
    (-1, -2),
    (-2, -1),
    (2, 1),
    (-2, 1),
    (2, -1),
)
ingrid = lambda i, j, r, c: (0 <= i < r) and (0 <= j < c)

def min_lockdown_cost(
            costs: Sequence[Sequence[int]],
            hunters: Sequence[Cell],
            hideouts: Sequence[Cell],
        ) -> int | tuple[int, list[Cell]]:
    if not costs:
        return 0, []
    
    r = len(costs)
    c = len(costs[0])

    if r == 0 or c == 0:
        return 0, []

    costs = [row[:] for row in costs]

    nodes = [(i, j) for i in range(1, r+1) for j in range(1, c+1)]
    nodes += [(-i, -j) for i, j in nodes]
    source = ("S", 0)
    sink = ("T", 0)
    nodes += [source, sink]

    hideouts_set = set(hideouts)
    adj = {node: [] for node in nodes}

    # constraints say this is impossible, but just in case
    if any(h in hideouts_set for h in hunters):
        return 0, []
    
    inf = 10**18
    for hi, hj in hunters:
        if ingrid(hi, hj, r, c):
            adj[source].append(Edge(source, (-(hi+1), -(hj+1)), inf, 0, None))

    for hi, hj in hideouts_set:
        if ingrid(hi, hj, r, c):
            adj[(hi+1, hj+1)].append(Edge((hi+1, hj+1), sink, inf, 0, None))

    base = 0
    for i in range(1, r+1):
        for j in range(1, c+1):
            cell0 = (i-1, j-1)
            in_node = (-i, -j)
            out_node = (i, j)
            if cell0 in hideouts_set:
                cap = inf
            else:
                cap = costs[i-1][j-1] if costs[i-1][j-1] >= 0 else 0
                if costs[i-1][j-1] < 0:
                    base += costs[i-1][j-1]
            adj[in_node].append(Edge(in_node, out_node, cap, 0, None))

            for di, dj in delta:
                ni = i + di
                nj = j + dj
                if not ingrid(ni-1, nj-1, r, c):
                    continue
                neighbor_in = (-(ni), -(nj))
                adj[out_node].append(Edge(out_node, neighbor_in, inf, 0, None))

    f, residual = max_flow(adj, source, sink)
    min_cost = base + f
    reachable = set()
    dq = deque([source])
    reachable.add(source)
    while dq:
        u = dq.popleft()
        for e in residual.get(u, []):
            if (e.cap - e.flow) > 0 and e.v not in reachable:
                reachable.add(e.v)
                dq.append(e.v)

    locked = []
    for i in range(1, r+1):
        for j in range(1, c+1):
            in_node = (-i, -j)
            out_node = (i, j)
            cell0 = (i-1, j-1)
            if cell0 in hideouts_set:
                continue
            if in_node in reachable and out_node not in reachable:
                locked.append((i-1, j-1))

    return min_cost, locked

# quick smoke tests (your examples)
if __name__ == "__main__":
    print(min_lockdown_cost([
            [10, 1, 10],
            [1, 10, 1],
            [10, 1, 10],
        ],
        [(0, 0)],
        [(2, 2)],
    ))
    print(min_lockdown_cost([
            [5, 5],
            [5, 5],
        ],
        [(0, 0)],
        [(1, 1)],
    ))