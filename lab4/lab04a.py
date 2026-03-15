from collections import deque
from collections.abc import Sequence
from oj import Conduit # pyright: ignore

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
    
def find_safe_thermal_flow(n: int, conduits: Sequence[Conduit]) -> list[int] | None:
    super_source = n
    super_sink = n + 1
    ek = EdmondsKarp(n + 2)

    balance = [0] * n
    edge_indices = []

    # l <= f <= u to 0 <= f' <= (u-l)
    for con in conduits:
        u = con.x - 1
        v = con.y - 1
        l = con.l
        cap = con.u - con.l

        idx = ek.add_edge(u, v, cap)
        edge_indices.append((idx, l, cap)) # remember edge to reconstruct flow

        # have l units already flow through edge and track node imbalance
        balance[u] -= l
        balance[v] += l
    
    total_demand = 0

    # nodes with positive balance need incoming flow, while negative must send flow out
    for i in range(n):
        if balance[i] > 0:
            ek.add_edge(super_source, i, balance[i])
            total_demand += balance[i]
        elif balance[i] < 0:
            ek.add_edge(i, super_sink, -balance[i])

    ek.add_edge(super_sink, super_source, 10**18) # circulation

    # if not all node demands can be satisfied, then no feasible circulation exists
    if ek.max_flow(super_source, super_sink) != total_demand:
        return None
    
    result = []

    # recover actual flow on each conduit
    for idx, l, cap in edge_indices:
        remaining = ek.edges[idx][1]
        result.append((cap - remaining) + l)

    return result