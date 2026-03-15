"""
ONE-INDEXED
s = stations = nodes
r = routes = edges, bidirectional

for a route i, d_i = max(0, d_i + e_i)
after k waves, 
d_i(k) = max(0, d_i + ke_i)

so the optimal strategy is, for a route d_i(k) {
d_i + ke_i, where e_i > 0
d_i, where e_i <= 0

get minimum 1-2 (s-t) cut

every edge, if k1 < k2,
di(k1) <= di(k2), with capacities either staying the same
or increasing

BINARY SEARCH BABBYYYYYYYYYY

we look for the mincut(k) >= v
"""

from collections import deque
from collections.abc import Sequence
from oj import Route

class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph = [[] for _ in range(n)] # adj list storing edge indices
        self.edges = [] # where edges = [to_index, residual_capacity, reverse_index]

    def add_edge(self, u: int, v: int, cap: int) -> int:
        idx = len(self.edges)
        fwd_idx = idx
        bwd_idx = idx + 1

        # forward edge
        self.edges.append([v, cap, bwd_idx])
        # reverse edge with 0 initial cap
        self.edges.append([u, 0, fwd_idx])

        self.graph[u].append(fwd_idx)
        self.graph[v].append(bwd_idx)

        return fwd_idx # return index of forward edge to recover flow
    
    def bfs(self, s: int, t: int, parent: list[int]) -> int:
        # find augmenting path and return its bottleneck capacity, else 0
        parent[:] = [-1] * self.n
        parent[s] = -2
        q = deque([(s, 10**18)])

        while q:
            u, flow = q.popleft()

            for idx in self.graph[u]:
                v, cap, _ = self.edges[idx]

                # traverse only edges with remaining capacity
                if parent[v] == -1 and cap > 0:
                    parent[v] = idx
                    new_flow = min(flow, cap)

                    if v == t:
                        return new_flow

                    q.append((v, new_flow))
        
        return 0
    
    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        parent = [-1] * self.n

        while True:
            new_flow = self.bfs(s, t, parent)
            if new_flow == 0:
                break

            flow += new_flow
            v = t

            # walk backward along augmenting path updating residual capacities
            while v != s:
                idx = parent[v]
                rev = self.edges[idx][2] # reverse edge index

                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow

                v = self.edges[rev][0]
        
        return flow

def min_num_fortification_waves(s: int, routes: Sequence[Route], v: int) -> int | None:
    def feasible(k: int) -> bool:
        # check if k fortification waves make the min s-t cut >= v
        ek = EdmondsKarp(s + 1)

        # for each route, use the formula in the docstring
        for r in routes:
            if r.e > 0:
                cap = r.d + k * r.e
            else:
                cap = r.d
            
            ek.add_edge(r.x, r.y, cap)
            ek.add_edge(r.y, r.x, cap)
        
        return ek.max_flow(1, 2) >= v # mincut >= v
    
    # if already safe without fortifications, just dont lmao
    if feasible(0):
        return 0

    low, high = 1, 1

    # grow high until near constraints or condition is feasible
    while high <= 10**16 and not feasible(high): # constraints go to 10^15 but lets go one exponent higher
        high *= 2

    # out of bounds from constraints, gtfo
    if high > 10**16:
        return None
    
    # thanos search
    while low < high:
        mid = (low + high) // 2

        if feasible(mid):
            high = mid
        else:
            low = mid + 1

    return low

res1 = min_num_fortification_waves(
    3,
    (
        Route(x=1, y=3, d=2, e=1),
        Route(x=1, y=3, d=1, e=2),
        Route(x=3, y=2, d=8, e=0),
    ),
    3,
)
exp1 = 0
res2 = min_num_fortification_waves(
    3,
    (
        Route(x=1, y=3, d=2, e=1),
        Route(x=1, y=3, d=1, e=2),
        Route(x=3, y=2, d=8, e=0),
    ),
    8,
)
exp2 = 2
res3 = min_num_fortification_waves(
    3,
    (
        Route(x=1, y=3, d=2, e=1),
        Route(x=1, y=3, d=1, e=2),
        Route(x=3, y=2, d=8, e=0),
    ),
    9,
)
exp3 = None
res4 = min_num_fortification_waves(
    5,
    (
        Route(x=1, y=3, d=3, e=0),
        Route(x=1, y=4, d=1, e=1),
        Route(x=3, y=5, d=2, e=1),
        Route(x=4, y=5, d=2, e=-1),
        Route(x=5, y=2, d=6, e=7),
    ),
    5,
)
exp4 = 1