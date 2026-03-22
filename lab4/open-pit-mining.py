"""
pi = valuei - costi
profit eges:
if pi > 0: s ->i with capacity pi
if pi < 0: i ->t with capacity -pi
dependency edges:
j->i with capacity=inf because we need to take i before j
 
"""

from collections import deque

class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = []

    def add_edge(self, u: int, v: int, cap: int) -> int:
        idx = len(self.edges)
        fwd_idx = idx
        bwd_idx = idx + 1

        self.edges.append([v, cap, bwd_idx])
        self.edges.append([u, 0, fwd_idx])

        self.graph[u].append(fwd_idx)
        self.graph[v].append(bwd_idx)

        return fwd_idx
    
    def bfs(self, s: int, t: int, parent: list[int]) -> int:
        parent[:] = [-1] * self.n
        parent[s] = -2
        q = deque([(s, 10**18)])

        while q:
            u, flow = q.popleft()

            for idx in self.graph[u]:
                v, cap, _ = self.edges[idx]

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
                rev = self.edges[idx][2]

                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow

                v = self.edges[rev][0]
        
        return flow

def open_pit_mining():
    n = int(input())

    s = n
    t = n + 1
    mf = EdmondsKarp(n + 2)

    inf = 10**18
    total_positive = 0

    for i in range(n):
        data = list(map(int, input().split()))
        value, cost, k = data[0], data[1], data[2]
        obstructs = data[3:]

        p = value - cost

        # profit edges
        if p > 0:
            mf.add_edge(s, i, p)
            total_positive += p
        elif p < 0:
            mf.add_edge(i, t, -p)
        
        # dependency edges
        for j in obstructs:
            j -= 1 # convert to 0-base
            # i obstruct j, j depends on i
            # add edge j->i
            mf.add_edge(j, i, inf)
    
    min_cut = mf.max_flow(s, t)

    print(total_positive - min_cut)

if __name__ == "__main__":
    open_pit_mining()