"""
place traps on a minimum vertex cut separating 
S and D
- BFS from S to compute dist_s
- BFS from D to compute dist_d
- let l = dist_s[d], the shortest path length

any cell v satisfying dist_s[v] + dist_d[v] = l
lies on some shortest S->D path.

if we group these cells by dist_s[v], each layer 
corresponds to a step along shortest paths.

if a layer has exactly one candidate, every shortest
path must pass through, so we must place a path there
"""
from collections import deque

class EdmondsKarp:
    """
    capacity[u][v] = capacity of edge u -> v
    adj[u] = list of neighbors for residual traversal
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.capacity = [dict() for _ in range(n)]
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        # add directed edge u -> v
        if v not in self.capacity[u]:
            self.capacity[u][v] = 0
        self.capacity[u][v] += cap

        if u not in self.capacity[v]:
            self.capacity[v][u] = 0

        self.adj[u].append(v)
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
                if parent[v] == -1 and self.capacity[u].get(v, 0) > 0:
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
                self.capacity[v][u] = self.capacity[v].get(u, 0) + new_flow
                v = u
        
        return flow
    
def place_traps(alleyways: str) -> str:
    grid = [list(r) for r in alleyways.splitlines()]
    r, c = len(grid), len(grid[0])
    n = r * c

    src = 2*n
    snk = 2*n+1
    n = 2*n+2 # transformed

    ek = EdmondsKarp(n)

    def id(i, j):
        return i*c + j

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "#":
                continue

            v = id(i, j)
            vin = v*2
            vout = v*2+1

            if grid[i][j] == "S":
                ek.add_edge(src, vin, float("inf"))
                ek.add_edge(vin, vout, float("inf"))
            
            elif grid[i][j] == "D":
                ek.add_edge(vout, snk, float("inf"))
                ek.add_edge(vin, vout, float("inf"))

            else:
                ek.add_edge(vin, vout, 1)
            
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in dirs:
                ni, nj = i + dx, j + dy
                if 0 <= ni < r and 0 <= nj < c and grid[ni][nj] != "#":
                    ek.add_edge(vout, id(ni, nj)*2, float("inf"))

    ek.max_flow(src, snk)

    # residual bfs to find s-side of cut
    visited = [False] * n
    q = deque([src])
    visited[src] = True

    while q:
        u = q.popleft()
        for v in ek.adj[u]:
            if not visited[v] and ek.capacity[u].get(v, 0) > 0:
                visited[v] = True
                q.append(v)
    
    # cut vertex edges = traps
    for i in range(r):
        for j in range(c):
            if grid[i][j] != ".":
                continue

            v = id(i, j)
            vin = v*2
            vout = v*2 + 1

            if visited[vin] and not visited[vout]:
                grid[i][j] = "X"
    
    return "\n".join("".join(row) for row in grid)

print(place_traps("""\
.#...#.
..#....
.S.....
.....D.
....#..
.#...#.
""")
)

print(place_traps("""\
#.#.#
.S...
#.#.#
...D.
#.#.#
"""))