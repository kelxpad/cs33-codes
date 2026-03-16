from itertools import combinations
from collections import deque

def bfs(adj, forbidden, hunters, hideouts):
    deq = deque()
    visited = {i:False for i in adj}
    for h in hunters:
        deq.append(h)
    while deq:
        c = deq.popleft()
        if c in forbidden:
            continue
        visited[c] = True
        if c in hideouts:
            return False
        for cc in adj[c]:
            if (not visited[cc]) and (cc not in forbidden):
                deq.append(cc)
    return True

def check_ans(grid, r, c, hunters, hideouts, mincut, cuts):
    adj = {(i, j) : [] for i in range(r) for j in range(c)}
    for i in range(r):
        for j in range(c):
            for di, dj in dirs:
                ni = i + di
                nj = j + dj
                if not ingrid(ni, nj, r, c):
                    continue
                adj[(i, j)].append((ni, nj))
    assert sum(grid[i][j] for i, j in cuts) == mincut
    assert bfs(adj, cuts, hunters, hideouts)


dirs = (
    (1, -2),
    (-1, 2),
    (1, 2),
    (-1, -2),
    (-2, -1),
    (2, 1),
    (-2, 1),
    (2, -1),
)

ingrid = lambda i, j, r, c: (0 <= i < r) and (0 <= j < c)

def min_lockdown_cost(
            costs,
            hunters,
            hideouts,
        ):
    r = len(costs)
    c = len(costs[0]) if costs else 0
    hunters = set(hunters)
    hideouts = set(hideouts)
    print(r, c)
    coords = [(i, j) for i in range(r) for j in range(c) if costs[i][j] > 0 and (i, j) not in hideouts]
    oforbidden = set((i, j) for i in range(r) for j in range(c) if costs[i][j] <= 0 and (i, j) not in hideouts)
    adj = {(i, j) : [] for i in range(r) for j in range(c)}
    for i in range(r):
        for j in range(c):
            for di, dj in dirs:
                ni = i + di
                nj = j + dj
                if not ingrid(ni, nj, r, c):
                    continue
                adj[(i, j)].append((ni, nj))
    oans = sum(costs[i][j] for i, j in oforbidden)
    if bfs(adj, oforbidden, hunters, hideouts):
        return oans
    ansd = None
    ans = float('inf')
    for count in range(1, len(coords) + 1):
        for subset in combinations(coords, count):
            forbidden = set(subset).union(oforbidden)
            if bfs(adj, forbidden, hunters, hideouts):
                v = sum(costs[i][j] for i, j in forbidden)
                ans = min(v, ans)
                if ans == v:
                    ansd = subset
    print(ansd)
    return ans