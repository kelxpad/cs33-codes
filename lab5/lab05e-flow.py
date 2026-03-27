"""
nangangamoy bipartite
we cant use kuhn's for this problem because hindi one-to-one yung mapping, it would need 5 copies of each to fit the problem
therefore, we can model this as a flow problem, edmonds-karp should do the trick

source -> horse -> race -> jockey -> sink
"""

from collections import deque
from collections.abc import Sequence
from derby import Participation # pyright: ignore take out later after restarting vsc

inf = 10**18
class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = [] # [to_idx, res_cap, rev_idx]
    
    def add_edge(self, u: int, v: int, cap: int) -> None:
        idx = len(self.edges)
        fwd_idx = idx
        bwd_idx = idx + 1

        self.edges.append([v, cap, bwd_idx])
        self.edges.append([u, 0, fwd_idx]) # no flow yet, nothing to undo

        self.graph[u].append(fwd_idx)
        self.graph[v].append(bwd_idx)

        return fwd_idx

    def bfs(self, s: int, t: int, parent: list[int]) -> int:
        # find augmenting path and return its bottleneck cap else 0
        parent[:] = [-1] * self.n # reset to find fresh augmenting path
        parent[s] = -2
        q = deque([(s, inf)])

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

            # walk backward along augmenting path updating residual capacity
            while v != s: # bfs modified parent, we use it
                idx = parent[v]
                rev = self.edges[idx][2]

                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow

                v = self.edges[rev][0]
        
        return flow

def plan_races(m: int, k: int, 
    x: Sequence[frozenset[int]], 
    y: Sequence[frozenset[int]]
    ) -> int | list[list[Participation]]:
    r = len(x) # races

    source = 0
    horse_start = 1
    race_in_start = horse_start + m
    race_out_start = race_in_start + r
    jockey_start = race_out_start + r
    sink = jockey_start + k

    nodes = sink + 1
    ek = EdmondsKarp(nodes)

    # sources -> horses
    for horse in range(m):
        ek.add_edge(source, horse_start + horse, 5)
    
    # horses -> race_in
    for race in range(r):
        for horse in x[race]:
            ek.add_edge(horse_start + horse, race_in_start + race, 8)
    
    # race_in -> race_out (capacity 8 per race)
    for race in range(r):
        ek.add_edge(race_in_start + race, race_out_start + race, 8)

    # race_out -> jockeys
    for race in range(r):
        for jockey in y[race]:
            ek.add_edge(race_out_start + race, jockey_start + jockey, 8)
    
    # jockeys -> sink
    for jockey in range(k):
        ek.add_edge(jockey_start + jockey, sink, 5)
    
    # compute max flow
    return ek.max_flow(source, sink)
    
res1 = plan_races(3, 3, (
    frozenset({0, 1}), 
    frozenset({1, 2}),
), (
    frozenset({0, 1}),
    frozenset({0, 2}),
))
exp1 = [15] 
assert res1 in exp1, f"{res1}"