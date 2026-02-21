from collections.abc import Sequence 
from diosworld import Road
from heapq import heappush, heappop

def min_time(n: int, s: int, t: int, v: Sequence[int], roads: Sequence[Road]) -> int | None:
    st,en = s-1, t-1
    k = len(v)

    victims_at = [[] for _ in range(n)]
    for idx, loc in enumerate(v):
        victims_at[loc - 1].append(idx)
    
    adj = [[] for _ in range(n)] 
    for r in roads:
        adj[r.a - 1].append((r.b - 1, r.t, r.c))
    
    dist = {}
    pq = []  

    dist[(st, 0)] = 0
    heappush(pq, (0, st, 0))

    while pq:
        d, u, mask = heappop(pq)

        if dist.get((u, mask), float("inf")) < d:
            continue 

        speed = mask.bit_count()

        # try move without drinking
        for v2, t0, c in adj[u]:
            nd = d + max(0, t0 - c * speed)
            key = (v2, mask)
            if nd < dist.get(key, float("inf")):
                dist[key] = nd
                heappush(pq, (nd, v2, mask))

        # drink one new victim
        for vid in victims_at[u]:
            if not (mask & (1 << vid)):
                nmask = mask | (1 << vid)
                nd = d + 1
                key = (u, nmask)  
                if nd < dist.get(key, float("inf")):
                    dist[key] = nd
                    heappush(pq, (nd, u, nmask))

    res = min((d for (node, _) , d in dist.items() if node == en), default=float('inf'))

    return None if res == float("inf") else res

print(min_time(3, 1, 3, (2,), (
    Road(a=1, b=2, t=10, c=5),
    Road(a=1, b=3, t=15, c=5),
    Road(a=2, b=3, t=10, c=7),
))
)

print(min_time(3, 1, 3, (2,), (
    Road(a=1, b=2, t=10, c=5),
    Road(a=1, b=3, t=15, c=5),
    Road(a=2, b=3, t=10, c=20),
))
)