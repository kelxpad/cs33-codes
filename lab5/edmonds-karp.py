from collections import deque

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

            while v != s:
                idx = parent[v]
                rev = self.edges[idx][2]

                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow

                v = self.edges[rev][0]

        return flow