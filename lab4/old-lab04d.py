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
        self.capacity = [dict() for _ in range(n+1)]
        self.adj = [[] for _ in range(n+1)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        # add directed edge u -> v
        if v not in self.capacity[u]:
            self.capacity[u][v] = 0        
        self.capacity[u][v] += cap

        if u not in self.capacity[v]:
            self.capacity[v][u] = 0

        self.adj[u].append(v)
        self.adj[v].append(u)

    def bfs(self, s: int, t: int, parent: list[int]) -> bool:
        # just look for a path we can flow to
        for i in range(self.n + 1):
            parent[i] = -1

        parent[s] = -2
        q = deque([s])

        while q:
            u = q.popleft()

            for v in self.adj[u]:
                if parent[v] == -1 and self.capacity[u].get(v, 0) > 0:
                    parent[v] = u
                    if v == t:
                        return True
                    
                    q.append(v)
        
        return False
    
    def max_flow_paths(self, s: int, t: int) -> list[list[int]]:
        # idea: push 1 unit of flow per bfs
        # so each path corresponds to one unit of flow
        # if this still RTEs, im starting from scratch
        parent = [-1] * (self.n + 1)
        paths = []

        while self.bfs(s, t, parent):
            path = []
            cur = t
            while cur != s:
                path.append(cur)
                cur = parent[cur]
                if cur == -1:
                    path = []
                    break
            if not path:
                break
            path.append(s)
            path = path[::-1]

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if self.capacity[u].get(v, 0) <= 0:
                    # skip broken path
                    path = []
                    break
                self.capacity[u][v] -= 1
                self.capacity[v][u] = self.capacity[v].get(u, 0) + 1
            if not path:
                break

            paths.append(path)
        
        return paths

    
def max_investigations(
            n: int,
            roads: Sequence[tuple[int, int, int]],
            haunted: Sequence[int],
            h: int,
        ) -> int | list[tuple[int, list[int]]]:
    
    ek = EdmondsKarp(n + 2)
    super_sink = n + 1
    inf = 10**9 # arbitrarily large number

    investigations = []
    for u, v, c in roads:
        ek.add_edge(u, v, c)
        ek.add_edge(v, u, c)

    for t in haunted:
        ek.add_edge(t, super_sink, inf)
    
    paths = ek.max_flow_paths(h, super_sink)

    groups = {}

    for p in paths:
        t = p[-2]
        if t not in groups:
            groups[t] = []
        groups[t].append(p[:-1])

    for t, ps in groups.items():
        for i in range(0, len(ps), 2):
            if i + 1 >= len(ps):
                break

            p = ps[i]
            cycle = p + p[-2::-1]
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