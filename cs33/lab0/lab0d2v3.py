from collections.abc import Sequence
from collections import deque
from diosworld import Road

def min_time(n: int, s: int, t: int,
             energydrink_locations: Sequence[int],
             roads: Sequence[Road]) -> int | None:

    st, en = s - 1, t - 1
    e_count = len(energydrink_locations)
    inf = float("inf")

    # map drinks to their indices; allow multiple drinks at same node
    edrink = [[] for _ in range(n)]
    for i, loc in enumerate(energydrink_locations):
        edrink[loc - 1].append(i)

    # adjacency list for directed roads: adj[u] = list of (v, t, c)
    adj = [[] for _ in range(n)]
    for r in roads:
        adj[r.a - 1].append((r.b - 1, r.t, r.c))

    ss = 1 << e_count  # number of masks
    # precompute popcount for masks
    popcount = [bin(m).count("1") for m in range(ss)]

    # dist[u][mask] = min time to reach u having consumed drinks=mask
    dist = [[inf] * ss for _ in range(n)]
    dist[st][0] = 0

    total_states = n * ss

    # bellman-ford on expanded graph
    for _ in range(total_states - 1):
        relaxed = False

        for u in range(n):
            row = dist[u]
            if all(x == inf for x in row):
                continue
            for mask in range(ss):
                cur = dist[u][mask]
                if cur == inf:
                    continue

                # drink transitions: consume any unused drink at u
                for di in edrink[u]:
                    if mask & (1 << di):
                        continue
                    nmask = mask | (1 << di)
                    ntime = cur + 1
                    if dist[u][nmask] > ntime:
                        dist[u][nmask] = ntime
                        relaxed = True

                # road transitions (directed)
                d = popcount[mask]
                for v, tt, cc in adj[u]:
                    ntime = cur + tt - d * cc
                    if dist[v][mask] > ntime:
                        dist[v][mask] = ntime
                        relaxed = True

        if not relaxed:
            break

    # detect negative cycles that can reach t:
    # collect states (v,mask) that can still be relaxed
    seen = [[False] * ss for _ in range(n)]
    q = deque()
    for u in range(n):
        for mask in range(ss):
            cur = dist[u][mask]
            if cur == inf:
                continue
            d = popcount[mask]
            for v, tt, cc in adj[u]:
                if cur + tt - d * cc < dist[v][mask]:
                    if not seen[v][mask]:
                        seen[v][mask] = True
                        q.append((v, mask))

    # BFS over state graph from relaxable states:
    # road edges within same mask, and drink edges to mask|bit
    while q:
        u, mask = q.popleft()
        if u == en:
            return None  # negative cycle can reach target

        # road neighbors (same mask)
        for v, _, _ in adj[u]:
            if not seen[v][mask]:
                seen[v][mask] = True
                q.append((v, mask))

        # drink neighbors (increase mask)
        for di in edrink[u]:
            if not (mask & (1 << di)):
                nmask = mask | (1 << di)
                if not seen[u][nmask]:
                    seen[u][nmask] = True
                    q.append((u, nmask))

    # no negative-cycle path to t found; return best finite answer
    ans = min(dist[en])
    return ans if ans != inf else None

res1 = min_time(3, 1, 3, (), ( # modified example where e = 0
    Road(a=1, b=2, t=10, c=5),
    Road(a=1, b=3, t=15, c=5),
    Road(a=2, b=3, t=10, c=10),
))
exp1 = 15
assert res1 == exp1, f"got {res1}"

res2 = min_time(5, 1, 5, (), ( # shortest path reduction
    Road(a=1, b=2, t=10, c=5),
    Road(a=2, b=3, t=10, c=5),
    Road(a=3, b=4, t=10, c=5),
    Road(a=4, b=5, t=10, c=5),
    Road(a=1, b=5, t=100,c=5)
))
exp2 = 40
assert res2 == exp2, f"got {res2}"

res3 = min_time(5, 1, 5, (), ( # t is unreachable from s
    Road(a=1, b=2, t=10, c=5),
    Road(a=2, b=3, t=10, c=5),
    Road(a=3, b=4, t=10, c=5),
    Road(a=4, b=3, t=10, c=5),
    Road(a=2, b=4, t=10, c=5)
))
exp3 = None
assert res3 == exp3, f"got {res3}"

res4 = min_time(3, 1, 3, (2,), ( # e = 1 test case
    Road(a=1, b=2, t=10, c=5),
    Road(a=1, b=3, t=15, c=5),
    Road(a=2, b=3, t=10, c=10),
))
exp4 = 11
assert res4 == exp4, f"got {res4}"

res5 = min_time(3, 1, 3, (2,), (
    Road(a=1, b=2, t=10, c=5),
    Road(a=1, b=3, t=15, c=5),
    Road(a=2, b=3, t=10, c=20),
))
exp5 = 1
assert res5 == exp5, f"got {res5}"