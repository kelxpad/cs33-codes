from collections import deque

class HopcroftKarp:
    def __init__(self, n: int, m: int) -> None:
        self.n = n # left size
        self.m = m # right size
        self.adj = [[] for _ in range(n)]

        self.match_l = [-1] * n
        self.match_r = [-1] * m
        self.dist = [-1] * n

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    def bfs(self) -> bool:
        q = deque()
        for u in range(self.n):
            if self.match_l[u] == -1:
                self.dist[u] = 0
                q.append(u)
            else:
                self.dist[u] = -1
        
        found_augmenting = False

        while q:
            u = q.popleft()
            for v in self.adj[u]:
                u2 = self.match_r[v]
                if u2 != -1 and self.dist[u2] == -1:
                    self.dist[u2] = self.dist[u] + 1
                    q.append(u2)
                if u2 == -1:
                    found_augmenting = True

        return found_augmenting

    def dfs(self, u: int) -> bool:
        for v in self.adj[u]:
            u2 = self.match_r[v]
            if u2 == -1 or (self.dist[u2] == self.dist[u] + 1 and self.dfs(u2)):
                self.match_l[u] = v
                self.match_r[v] = u
                return True
        
        self.dist[u] = -1 # prune
        return False

    def max_matching(self) -> int:
        res = 0
        while self.bfs():
            for u in range(self.n):
                if self.match_l[u] == -1 and self.dfs(u):
                    res += 1
        return res
    
    def get_pairs(self) -> list[tuple[int, int]]:
        pairs = []
        for u, v in enumerate(self.match_l):
            if v != -1:
                pairs.append((u, v))
        return pairs
