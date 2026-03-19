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
    
def max_players(stage: str) -> int:
    rows = stage.strip().split("\n")
    r = len(rows)
    c = len(rows[0])

    def in_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c
    
    # assign an index to each platform
    pos_to_index = {}
    index = 0
    for i in range(r):
        for j in range(c):
            if rows[i][j] == '_':
                pos_to_index[(i, j)] = index
                index += 1
    total_nodes = index

    # partition nodes into black and white
    black = []
    white = []
    node_color = {}
    for (i, j), idx in pos_to_index.items():
        if (i + j) % 2 == 0:
            black.append(idx)
            node_color[idx] = 'black'
        else:
            white.append(idx)
            node_color[idx] = 'white'
        
    hk = HopcroftKarp(len(black), len(white))

    # map original node indices to left/right for hk
    black_map = {idx: i for i, idx in enumerate(black)}
    white_map = {idx: i for i, idx in enumerate(white)}

    # add edges connecting adjacent platforms
    for (i,j), idx in pos_to_index.items():
        if node_color[idx] != "black":
            continue
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i+dx, j+dy
            if in_bounds(ni, nj) and rows[ni][nj] == "_":
                v_idx = pos_to_index[(ni, nj)]
                if node_color[v_idx] == "white":
                    hk.add_edge(black_map[idx], white_map[v_idx])

    max_match = hk.max_matching()
    return total_nodes - max_match
    
res1 = max_players("""\
_____
__...
_.___
_.___
""")

exp1 = 8

assert res1 == exp1, f"{res1}"