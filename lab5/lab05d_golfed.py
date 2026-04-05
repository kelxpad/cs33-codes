"""
separate add_edge into add_left and add_right for 
ensuring left -> right bipartite traversal
"""
from collections.abc import Sequence

mv = (
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2),
)

def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    if not x or not x[0]:
        return []

    r, c = len(x), len(x[0])
    n = r * c
    cells = [(x[i][j], i, j) for i in range(r) for j in range(c)]
    cells.sort()

    active = [False] * n
    adj = [[] for _ in range(n)]
    mate = [-1] * n
    seen = [0] * n
    stamp = 0

    def dfs(u: int) -> bool:
        nonlocal stamp
        if seen[u] == stamp:
            return False
        seen[u] = stamp

        for v in adj[u]:
            w = mate[v]
            if w == -1 or dfs(w):
                mate[u] = v
                mate[v] = u
                return True
        return False

    ans = [-1] * (n + 1)
    active_cnt = 0
    matching_sz = 0
    prev_alpha = 0

    for cost, i, j in cells:
        u = i*c+j
        active[u] = True
        active_cnt += 1

        for di, dj in mv:
            ni, nj = i + di, j + dj
            if 0 <= ni < r and 0 <= nj < c:
                v = ni*c+nj
                if active[v]:
                    adj[u].append(v)
                    adj[v].append(u)

        stamp += 1
        if dfs(u):
            matching_sz += 1

        alpha = active_cnt - matching_sz
        for k in range(prev_alpha + 1, alpha + 1):
            ans[k] = cost
        prev_alpha = alpha

    return ans[1:]