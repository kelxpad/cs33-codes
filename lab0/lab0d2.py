# from heapq import heappush, heappop
"""

CURRENT UNKNOWN ISSUE: what if theres a negative cycle in the adj 
list, but doesnt coincide with the path from s to t SOLVED BY BELLMAN-FORD NIGHGA

we know this isnt an mst problem since the edges are directed from
a to b

n = nodes, indexed 1
s = jotaro's Start location
t = DIO's starT location
m = edges

e of these locations have energy drinks that boost jotaro's speed

what happens when e = 0?
d is the number of energy drinks jotaro drank, so
d = 0 by default 
jotaro can pass through roads in t - d * c minutes
MEANING
jotaro passes through roads in t minutes


roads meaning
a = source location
b = dest location
t = base minutes
c = multiplied with d, energy drinks

reworded problem statement:
whats the minimum amount of time it would take for jotaro to go from
S to T?

current problem: how do i adopt this e = 0 solution to e <= 4?
- how do i model jotaro choosing to drink the energy drink or not?
"""
from diosworld import Road
from collections.abc import Sequence

def bellman_ford(n: int, s: int,
                 edges: list[tuple[int, int, int, int]],
                 drink_locs: dict[int, list[int]],
                 k: int) -> list[list[float]] | None:
    inf = float("inf")

    # dist[u][mask] = minimum time to reach node u
    # having already consumed the set of drinks encoded by mask
    dist = [[inf] * (1 << k) for _ in range(n + 1)]

    # start at node s with no drinks consumed, mask = 0
    dist[s][0] = 0

    # total no. of states is now (n+1) * (2^k), b-f needs - 1 of that
    for _ in range((n + 1) * (1 << k) - 1):
        relaxed = False

        for u in range(1, n + 1):
            for mask in range(1 << k):
                if dist[u][mask] == inf:
                    continue

                # number of gatorade jotaro ate
                d = bin(mask).count("1")
                
                # road transitions
                for x, v, t, c in edges:
                    if x != u:
                        continue
                    w = t - d * c # travel time as described

                    # relax edge while keeping same drink history
                    if dist[v][mask] > dist[u][mask] + w:
                        dist[v][mask] = dist[u][mask] + w
                        relaxed = True
            
                # drink transitions
                # consider only nodes w energy drinks
                if u in drink_locs:

                    for i in drink_locs[u]:
                        if mask & (1 << i):
                            continue

                        nmask = mask | (1 << i)

                        if dist[u][nmask] > dist[u][mask] + 1:
                            dist[u][nmask] = dist[u][mask] + 1
                            relaxed = True

        if not relaxed: # early exit if nothing changed
            break 
        
    return dist

def min_time(n: int, s: int, t: int, 
             energydrink_locations: Sequence[int], 
             roads: Sequence[Road]) -> int | None:
    # initialize my edges until i relax
    edges = []
    drink_locs: dict[int, list[int]] = {}

    # process roads into edges
    for road in roads:
        edges.append((road.a, road.b, road.t, road.c))

    # keep track of white monster energies
    for i, loc in enumerate(energydrink_locations):
        if loc not in drink_locs:
            drink_locs[loc] = []
        drink_locs[loc].append(i)

    k = len(energydrink_locations)

    # bellman and ford sitting on a tree, k-i-s-s-i-n-g
    dist = bellman_ford(n, s, edges, drink_locs, k)
    if dist == None:
        return None
    
    ans = min(dist[t])

    return ans if ans != float("inf") else None

from diosworld import Road
from collections.abc import Sequence
from collections import deque

def bellman_ford(n: int, s: int,
                 edges: list[tuple[int, int, int, int]],
                 drink_locs: dict[int, int],
                 k: int) -> tuple[list[list[float]], set[tuple[int,int]]]:
    """
    Returns:
      dist[u][mask] = minimum time to reach u having consumed drinks in mask
      neg_states = set of (u, mask) states affected by a negative cycle
    """
    inf = float("inf")
    dist = [[inf] * (1 << k) for _ in range(n + 1)]
    dist[s][0] = 0
    states = (n + 1) * (1 << k)

    # standard Bellman–Ford relaxations
    for _ in range(states - 1):
        relaxed = False

        # road transitions
        for u, v, t, c in edges:
            for mask in range(1 << k):
                if dist[u][mask] == inf:
                    continue
                d = bin(mask).count("1")
                w = t - d * c
                if dist[v][mask] > dist[u][mask] + w:
                    dist[v][mask] = dist[u][mask] + w
                    relaxed = True

        # drink transitions
        for u in range(1, n + 1):
            if u not in drink_locs:
                continue
            i = drink_locs[u]
            for mask in range(1 << k):
                if dist[u][mask] == inf or (mask & (1 << i)):
                    continue
                nmask = mask | (1 << i)
                if dist[u][nmask] > dist[u][mask] + 1:
                    dist[u][nmask] = dist[u][mask] + 1
                    relaxed = True

        if not relaxed:
            break

    # detect all states that can still relax (negative cycles)
    neg_states = set()
    for u, v, t, c in edges:
        for mask in range(1 << k):
            if dist[u][mask] == inf:
                continue
            d = bin(mask).count("1")
            w = t - d * c
            if dist[v][mask] > dist[u][mask] + w:
                neg_states.add((v, mask))

    return dist, neg_states

def reachable_neg_cycle_to_target(n, edges, drink_locs, k, neg_states, t):
    """
    BFS in lifted-state graph from all negative-cycle affected states
    to check if t is reachable
    """
    visited = set()
    q = deque(neg_states)

    while q:
        u, mask = q.popleft()
        if (u, mask) in visited:
            continue
        visited.add((u, mask))

        if u == t:
            return True  # t is affected by negative cycle

        # road transitions
        for uu, vv, tt, cc in edges:
            if uu != u:
                continue
            q.append((vv, mask))

        # drink transitions
        if u in drink_locs:
            i = drink_locs[u]
            if not mask & (1 << i):
                q.append((u, mask | (1 << i)))

    return False

def min_time(n: int, s: int, t: int, 
             energydrink_locations: Sequence[int], 
             roads: Sequence[Road]) -> int | None:

    edges = [(r.a, r.b, r.t, r.c) for r in roads]
    drink_locs = {loc: i for i, loc in enumerate(energydrink_locations)}
    k = len(energydrink_locations)

    dist, neg_states = bellman_ford(n, s, edges, drink_locs, k)

    if neg_states:
        # check if t is reachable from any negative-cycle affected state
        if reachable_neg_cycle_to_target(n, edges, drink_locs, k, neg_states, t):
            return None

    ans = min(dist[t])
    return ans if ans != float("inf") else None


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