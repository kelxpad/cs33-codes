class Kuhn:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.adj = [[] for _ in range(n)] # edges from left to right

        self.match_r = [-1] * m
        self.match_l = [-1] * n

    def add_edge(self, u: int, v: int):
        self.adj[u].append(v)
    
    def dfs(self, u: int, vis: list[bool]) -> bool:
        if vis[u]:
            return False
        vis[u] = True

        for v in self.adj[u]:
            # if v is free OR we can re-match its partner
            if self.match_r[v] == -1 or self.dfs(self.match_r[v], vis):
                self.match_r[v] = u
                self.match_l[u] = v
                return True
            
        return False
    
    def max_matching(self) -> int:
        res = 0
        for u in range(self.n):
            vis = [False] * self.n
            if self.dfs(u, vis):
                res += 1
        return res
    
    def get_pairs(self):
        return [(u, self.match_l[u]) for u in range(self.n) if self.match_l[u] != -1]
    