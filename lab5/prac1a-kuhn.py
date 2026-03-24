class Kuhn:
    def __init__(self, n: int, m: int) -> None:
        self.n = n
        self.m = m
        self.adj = [[] for _ in range(self.n)]

        self.match_l = [-1] * n
        self.match_r = [-1] * m

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    def dfs(self, u: int, vis: list[bool]) -> bool:
        if vis[u]:
            return False
        vis[u] = True

        for v in self.adj[u]:
            if self.match_r[v] == -1 or self.dfs(self.match_r[v], vis):
                self.match_r[v] = u
                self.match_l[u] = v
                return True
        
        return False
    
    def max_matching(self) -> int:
        res = 0
        for u in range(self.n):
            visited = [False] * self.n
            if self.dfs(u, visited):
                res += 1
        
        return res
    
    def get_pairs(self) -> list[tuple[int, int]]:
        res = []
        for u in range(self.n):
            if self.match_l[u] != -1:
                res.append((u, self.match_l[u]))
        
        return res

def max_players(stage: str) -> int:
    rows = stage.strip().split("\n")
    r = len(rows)
    c = len(rows[0])

    def in_bounds(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c
    
    # assign index to each platform
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
            node_color[idx] = "black"
        else:
            white.append(idx)
            node_color[idx] = "white"
    
    cum = Kuhn(len(black), len(white))

    # map original node indices to left/right
    black_map = {idx: i for i, idx in enumerate(black)}
    white_map = {idx: i for i, idx in enumerate(white)}

    # add edges connecting adjacent platforms
    for (i, j), idx in pos_to_index.items():
        if node_color[idx] != "black":
            continue
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ni, nj = i + dx, j + dy
            if in_bounds(ni, nj) and rows[ni][nj] == "_":
                v_idx = pos_to_index[(ni, nj)]
                if node_color[v_idx] == "white":
                    cum.add_edge(black_map[idx], white_map[v_idx])
    
    max_match = cum.max_matching()
    return total_nodes - max_match

res1 = max_players("""\
_____
__...
_.___
_.___
""")

exp1 = 8

assert res1 == exp1, f"{res1}"