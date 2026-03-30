"""
grid problem!!

reuse reconstruction from 5c
binary search per k
"""
from collections.abc import Sequence

class Kuhn:
    def __init__(self, n: int, m: int) -> None:
        self.n = n
        self.m = m
        self.adj = [[] for _ in range(n)]

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
    
    def get_pairs(self) -> list[tuple[int, int]]:
        pairs = []
        for u in range(self.n):
            if self.match_l[u] != -1:
                pairs.append((u, self.match_l[u]))
        return pairs
    
def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    if not x or not x[0]:
        return []

    r = len(x)
    c = len(x[0])

    moves = [(2,1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    def in_bounds(i, j): return 0 <= i < r and 0 <= j < c

    # flatten + sort cells by cost
    cells = []
    for i in range(r):
        for j in range(c):
            cells.append((x[i][j], i, j))
    cells.sort()

    n = r * c

    # compute MIS size for threshold index mid
    def mis(mid: int) -> int:
        t = cells[mid][0]

        id_l = {}
        id_r = {}
        left = right = 0

        # assign ids only for active cells
        for i in range(r):
            for j in range(c):
                if x[i][j] > t:
                    continue
                if (i + j) % 2 == 0:
                    id_l[(i, j)] = left
                    left += 1
                else:
                    id_r[(i, j)] = right
                    right += 1
        
        kuhn = Kuhn(left, right)

        # build edges
        for (i, j), u in id_l.items():
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if in_bounds(ni, nj) and x[ni][nj] <= t:
                    if (ni, nj) in id_r:
                        kuhn.add_edge(u, id_r[(ni, nj)])
        
        matching = kuhn.max_matching()
        active = left + right
        return active - matching # max indep set

    res = []

    # binary search per k
    for k in range(1, n+1):
        low = 0; high = n - 1
        ans = -1
        while low <= high:
            mid = (low + high) // 2
            if mis(mid) >= k:
                ans = cells[mid][0]
                high = mid - 1
            else:
                low = mid + 1
        res.append(ans)

    return res

print(immigrants_game((
    (3, 1, 4, 1),
    (5, 9, 2, 6),
)))
