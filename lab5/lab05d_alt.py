from collections import deque
from collections.abc import Sequence

class HopcroftKarp:
    def __init__(self, n: int, is_left: list[bool], adj: list[list[int]], added: list[bool]) -> None:
        self.n = n
        self.is_left = is_left
        self.adj = adj
        self.added = added

        self.match_l = [-1] * n
        self.match_r = [-1] * n
        self.dist =    [-1] * n
    
    def bfs(self) -> bool:
        q = deque()

        for u in range(self.n):
            if not self.is_left[u] or not self.added[u]:
                continue
            if self.match_l[u] == -1:
                self.dist[u] = 0
                q.append(u)
            else:
                self.dist[u] = -1
        
        found = False

        while q:
            u = q.popleft()
            du = self.dist[u]

            for v in self.adj[u]:
                w = self.match_r[v]

                if w != -1 and self.dist[w] == -1:
                    self.dist[w] = du + 1
                    q.append(w)
                
                if w == -1:
                    found = True
        
        return found
    
    def dfs(self, u: int) -> bool:
        for v in self.adj[u]:
            w = self.match_r[v]

            if w == -1 or (self.dist[w] == self.dist[u] + 1 and self.dfs(w)):
                self.match_l[u] = v
                self.match_r[v] = u
                return True
        
        self.dist[u] = -1
        return False
    
    def run(self) -> int:
        res = 0

        while self.bfs():
            for u in range(self.n):
                if (self.is_left[u] and self.added[u] and self.match_l[u] == -1):
                    if self.dfs(u):
                        res += 1
        
        return res
    
def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    if not x or not x[0]:
        return []

    r, c = len(x), len(x[0])
    n = r * c

    def in_bounds(i, j): return 0 <= i < r and 0 <= j < c
    mv = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    vals = [(x[i][j], i*c+j) for i in range(r) for j in range(c)]
    vals.sort()

    is_left = [(i // c + i % c) % 2 == 0 for i in range(n)]

    adj = [[] for _ in range(n)]
    added = [False] * n

    hk = HopcroftKarp(n, is_left, adj, added)

    res = [-1] * n
    ptr = 0
    added_cnt = 0
    matching = 0

    i = 0
    while i < n:
        cost = vals[i][0]

        j = i
        while j < n and vals[j][0] == cost:
            _, u = vals[j]
            added[u] = True
            added_cnt += 1

            x0 = u // c
            y0 = u - x0 * c

            for dx, dy in mv:
                nx, ny = x0+dx, y0+dy
                if in_bounds(nx, ny):
                    v = nx * c + ny
                    if added[v]:
                        if is_left[u]:
                            adj[u].append(v)
                        else:
                            adj[v].append(u)

            j += 1
        
        matching += hk.run()

        mis = added_cnt - matching
        while ptr < mis:
            res[ptr] = cost
            ptr += 1
        
        i = j
    
    return res