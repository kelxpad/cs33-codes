from collections import deque

class EdmondsKarp:
    """
    capacity[u][v] = capacity of edge u -> v
    adj[u] = list of neighbors for residual traversal
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.capacity = [[0] * n for _ in range(n)]
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        # add directed edge u -> v
        self.capacity[u][v] += cap
        self.adj[u].append(v)
        # prepare reverse edge for residual graph
        self.adj[v].append(u)

    def bfs(self, s: int, t: int, parent: list[int]) -> int:
        # returns bottleneck flow if found, 0 if no path exists
        for i in range(self.n):
            parent[i] = -1
        
        parent[s] = -2
        q = deque([(s, float("inf"))])

        while q:
            u, flow = q.popleft()

            for v in self.adj[u]:
                if parent[v] == -1 and self.capacity[u][v] > 0:
                    parent[v] = u
                    new_flow = min(flow, self.capacity[u][v])

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
                u = parent[v]
                self.capacity[u][v] -= new_flow
                self.capacity[v][u] += new_flow
                v = u
        
        return flow
    
g = EdmondsKarp(4)

g.add_edge(0, 1, 3)
g.add_edge(0, 2, 2)
g.add_edge(1, 2, 5)
g.add_edge(1, 3, 2)
g.add_edge(2, 3, 3)

print(g.max_flow(0, 3))  # maximum s-t flow