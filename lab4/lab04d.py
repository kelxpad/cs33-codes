"""
ONE-INDEXED PROBLEM
locations = nodes
roads = edges = bidirectional = undirected
max # of uses = capacity
basta cycle siya lmao

given a graph, whats the maximum number of times 
you can come from h, visit exactly one haunted house,
then return to h, if you can only use edges a certain 
amount of times?

idea: h -> network -> haunted_i -> super_sink
each unit of flow reaching a haunted node represents one traversal
from h to that haunted house
an investigation needs two such traversals: one to go, one to return
meaning, we need to pair paths afterwards
"""

from collections.abc import Sequence
from collections import deque

class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        # graph[u] = list of [v, rev_idx, cap]
        self.graph = [[] for _ in range(n + 1)]

    def add_edge(self, u: int, v: int, cap: int, directed: bool = True) -> None:
        forward_cap = cap
        backward_cap = cap if not directed else 0
        u_idx = len(self.graph[u])  # index of forward edge in graph[u]
        v_idx = len(self.graph[v])  # index of backward edge in graph[v]
        self.graph[u].append([v, v_idx, forward_cap])
        self.graph[v].append([u, u_idx, backward_cap])

    def bfs(self, s: int, t: int) -> tuple[list[int], list[int]]:
        # Returns parent nodes and parent edge indices
        parent_node = [-1] * (self.n + 1)
        parent_edge = [-1] * (self.n + 1)
        parent_node[s] = s
        q = deque([s])
        while q:
            u = q.popleft()
            for i, (v, _, cap) in enumerate(self.graph[u]):
                if parent_node[v] == -1 and cap > 0:
                    parent_node[v] = u
                    parent_edge[v] = i
                    if v == t:
                        return parent_node, parent_edge
                    q.append(v)
        return parent_node, parent_edge

    def max_flow_paths(self, s: int, t: int) -> list[list[int]]:
        paths = []
        while True:
            parent_node, parent_edge = self.bfs(s, t)
            if parent_node[t] == -1:
                break

            # Augment by 1 unit of flow along path
            v = t
            while v != s:
                u = parent_node[v]
                ei = parent_edge[v]
                self.graph[u][ei][2] -= 1
                rev = self.graph[u][ei][1]
                self.graph[v][rev][2] += 1
                v = u

            # Rebuild path from s to t
            path = []
            v = t
            while v != s:
                path.append(v)
                v = parent_node[v]
            path.append(s)
            paths.append(path[::-1])

        return paths


def max_investigations(
        n: int,
        roads: Sequence[tuple[int, int, int]],
        haunted: Sequence[int],
        h: int,
    ) -> int | list[tuple[int, list[int]]]:

    ek = EdmondsKarp(n + 2)
    super_sink = n + 1
    inf = 10**9

    # Add undirected roads
    for u, v, c in roads:
        ek.add_edge(u, v, c, directed=False)

    # Connect haunted houses to super sink
    for t in haunted:
        ek.add_edge(t, super_sink, inf, directed=True)

    # Get all paths from h to super_sink
    paths = ek.max_flow_paths(h, super_sink)

    # Group paths by haunted house visited
    groups: dict[int, list[list[int]]] = {}
    for p in paths:
        haunted_node = p[-2]  # node before super_sink
        groups.setdefault(haunted_node, []).append(p[:-1])  # strip super_sink

    # Build investigations (pair forward + return)
    investigations = []
    for t, ps in groups.items():
        for i in range(0, len(ps) - 1, 2):
            forward = ps[i]
            backward = ps[i + 1]
            cycle = forward + backward[-2::-1]  # avoid duplicating haunted node
            investigations.append((t, cycle))

    return investigations

res1 = max_investigations(
    3,
    [
        (1, 2, 2),
        (2, 3, 2),
    ],
    [3],
    1,
)

exp1 = [(3, [1, 2, 3, 2, 1])]

res2 = max_investigations(
    5,
    [
        (1, 2, 2),
        (2, 5, 2),
        (1, 3, 2),
        (3, 5, 2),
    ],
    [5],
    1,
)

exp2 = [(5, [1, 2, 5, 2, 1]), (5, [1, 3, 5, 3, 1])]

res3 = max_investigations(
    6,
    [
        (1, 2, 4),
        (2, 3, 2),
        (3, 4, 2),
        (2, 5, 2),
        (5, 6, 2),
    ],
    [4, 6],
    1,
)

exp3 = [
    (4, [1, 2, 3, 4, 3, 2, 1]),
    (6, [1, 2, 5, 6, 5, 2, 1]),
]

assert res1 == exp1, f"{res1}"
assert res2 == exp2, f"{res2}"
assert res3 == exp3, f"{res3}"