"""
separate add_edge into add_left and add_right for 
ensuring left -> right bipartite traversal
"""
from collections.abc import Sequence

def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    if not x or not x[0]:
        return []

    r, c = len(x), len(x[0])
    n = r*c
    mv = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))

    def in_bounds(i: int, j: int) -> bool: return 0 <= i < r and 0 <= j < c
    vals = [(x[i][j], i*c+j) for i in range(r) for j in range(c)]
    vals.sort()

    neighbors = [[] for _ in range(n)]
    for i in range(r):
        base = i*c
        for j in range(c):
            u = base+j
            for di, dj in mv:
                ni, nj = i+di, j+dj
                if in_bounds(ni, nj):
                    neighbors[u].append(ni*c+nj)
    
    added = [False]*n
    match = [-1]*n
    seen = [0]*n
    parent = [-1]*n
    via = [-1]*n
    stamp = 0

    res = [-1]*n
    ptr = 0 
    added_cnt = 0
    matching = 0

    for cost, s in vals:
        added[s] = True
        stamp += 1
        seen[s] = stamp
        parent[s] = -1
        
        stack = [(s, 0)]
        while stack:
            u, i = stack[-1]
            if i ==len(neighbors[u]):
                stack.pop()
                continue
            
            stack[-1] = (u, i + 1)
            v = neighbors[u][i]

            if not added[v] or seen[v] == stamp:
                continue

            seen[v] = stamp
            w = match[v]

            if w == -1:
                cu, cv = u, v
                while True:
                    match[cu] = cv
                    match[cv] = cu
                    pu = parent[cu]
                    if pu == -1:
                        break
                    cv = via[cu]
                    cu = pu
                matching += 1
                break

            parent[w] = u
            via[w] = v
            stack.append((w, 0))
        
        added_cnt += 1
        mis = added_cnt - matching
        while ptr < mis:
            res[ptr] = cost
            ptr += 1
    
    return res

print(immigrants_game((
    (3, 1, 4, 1),
    (5, 9, 2, 6),
)))

