# https://codeforces.com/problemset/problem/546/E
"""
bipartite modelling
left side: source cities
right side: destination cities
super source -> left cities, with capacity = a_i
right cities -> super sink, with capacity = b_i
maintain invariant: netflow(a) = netflow(b)
left i -> right j edges 
if i = j (stay) or there is a road between i and j
cap = [100, inf] because why not
"""
from collections import deque

class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph = [[] for _ in range(n)] # adj list storing edge indice
        self.edges = [] # where edges = [to_index, residual_cap, reverse_idx]
    
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
        # find augmenting path and returns its bottleneck capacity
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

            # walk backward along augmenting path updating residual caps
            while v != s:
                idx = parent[v]
                rev = self.edges[idx][2] # reverse edge index

                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow

                v = self.edges[rev][0]
            
        return flow
        
def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    if sum(a) != sum(b):
        print("NO")
        return
    
    s = 2*n
    t = 2*n + 1
    ek = EdmondsKarp(2*n + 2)

    inf = 10**18

    # source -> left
    for i in range(n):
        ek.add_edge(s, i, a[i])

    # right -> sink
    for j in range(n):
        ek.add_edge(n+j, t, b[j])
    
    # store edge indices 
    edge_id = [[-1]*n for _ in range(n)]

    # staying
    for i in range(n):
        edge_id[i][i] = ek.add_edge(i, n+i, inf)

    # roads
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        edge_id[u][v] = ek.add_edge(u, n+v, inf)
        edge_id[v][u] = ek.add_edge(v, n+u, inf)
    
    flow = ek.max_flow(s, t)

    if flow != sum(b):
        print("NO")
        return
    
    print("YES")

    res = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if edge_id[i][j] != -1:
                idx = edge_id[i][j]
                res[i][j] = inf - ek.edges[idx][1]

    for row in res:
        print(*row)

if __name__ == "__main__":
    solve()