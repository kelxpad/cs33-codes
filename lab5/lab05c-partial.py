"""
matching -> min vertex cover -> max independent set
compute matching via kuhns
start from unmatched left nodes
dfs using unmatched edges (l -> r) to matched edges (r -> l)
let vis_l, vis_r be reachable left, right nodes

so min vertex cover:
left: not visited, right: visited

and max independent set:
left: visited, right: not visited

np equivalence reduction bb gurl
"""

from collections.abc import Sequence
type Coord = tuple[int, int]

class Kuhn:
    def __init__(self, n: int, m: int) -> None:
        self.n = n
        self.m = m
        self.adj = [[] for _ in range(n)] # edges from left to right

        self.match_l = [-1] * n
        self.match_r = [-1] * m

    def add_edge(self, u: int, v: int) -> None:
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
        pairs = []
        for u in range(self.n):
            if self.match_l[u] != -1:
                pairs.append((u, self.match_l[u]))
        return pairs

def max_knights(marked: Sequence[Sequence[bool]]) -> int | list[Coord]:
    r, c = len(marked), len(marked[0])
    moves = [(2,1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    def in_bounds(i, j): return 0 <= i < r and 0 <= j < c

    # map cells to ids
    id_l = {}
    id_r = {}

    left = 0; right = 0

    for i in range(r):
        for j in range(c):
            if marked[i][j]:
                continue
            if (i + j) % 2 == 0:
                id_l[(i, j)] = left
                left += 1
            else:
                id_r[(i, j)] = right
                right += 1
    
    kuhn = Kuhn(left, right)

    for (i, j), u in id_l.items():
        for di, dj in moves:
            ni, nj = i + di, j + dj
            if in_bounds(ni, nj) and not marked[ni][nj]:
                if (ni, nj) in id_r:
                    kuhn.add_edge(u, id_r[(ni, nj)])
    
    matching = kuhn.max_matching()
    free_cells = left + right

    return free_cells - matching

res1 = max_knights((
    (False, False, False),
    (False, False, False),
))
exp1 = 4

assert res1 == exp1, f"{res1}"