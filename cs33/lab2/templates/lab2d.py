"""
PROBLEM IS 1-INDEXED
n = islands/nodes
m = ferry routes/edges

Ryo is also traveling across the country via her family helicopter. 
She agreed to let Kita ride with her at most once to go between any two islands.

ryo's helicopter can allow an edge to:
- be repeated
- optionally be used
ryo condition: only one bridge left to cross
fun trip = eulerian walk

INCLUDE THE TEMPORARY EDGE AS RYO'S HELICOPTER

(assuming the graph is completely connected), if you can get the amount of 
odd-degree vertices down to 2, the problem is solvable

"""
from collections.abc import Sequence
from kita import Route, Movement

class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr: 
            return False
        # else, union by rank
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

# hierholtzer is easy young man, checking if theres a valid solution is harder
def is_solvable(n, routes):
    deg = [0] * n
    uf = UnionFind(n)

    for u, v in routes:
        u -= 1; v-= 1
        deg[u] += 1
        deg[v] += 1
        uf.union(u, v)

    # group vertices by component, only those with degree > 0
    comps = {}
    for i in range(n):
        if deg[i] > 0:
            root = uf.find(i)
            comps.setdefault(root, []).append(i)

    components = len(comps)
    
    edges = [(i, (u - 1, v - 1)) for i, (u, v) in enumerate(routes, start=1)]

    # case: more than 2 components is impossible to fix with ryo's rich ass
    if components > 2:
        return False, [], []
    
    # case: exactly 2 components, p2w ryo
    if components == 2:
        comp_roots = list(comps.keys())
        a = comps[comp_roots[0]]
        b = comps[comp_roots[1]]

        # count odds per component
        odds_a = [v for v in a if deg[v] % 2]
        odds_b = [v for v in b if deg[v] % 2]

        # helicopter must connect a and b
        # we try connecting an odd if possible, else any vertex
        u = odds_a[0] if odds_a else a[0]
        v = odds_b[0] if odds_b else b[0]

        edges.append((0, (u, v)))
        deg[u] += 1
        deg[v] += 1

    # case: exactly one component
    else: 
        odds = [i for i in range(n) if deg[i] % 2]
        if len(odds) == 4:
            edges.append((0, (odds[0], odds[1])))
            deg[odds[0]] += 1
            deg[odds[1]] += 1
    
    odds = [i for i in range(n) if deg[i] % 2]

    if len(odds) in [0, 2]:
        return True, edges, odds
    
    # else, not solvable
    return False, [], []

def hierholtz(n, edges, start):
    used = [False] * len(edges)
    movement_path = []

    adj = [[] for _ in range(n)]

    for pos, (route_idx, (u, v)) in enumerate(edges):
        adj[u].append((pos, route_idx, v))
        adj[v].append((pos, route_idx, u))

    stack = [(start, None)] # (vertex, edge_used_to_get_here)

    while stack:
        v, incoming = stack[-1]
        # print(used)
        # print(v)
        # print(adj[v])
        while adj[v] and used[adj[v][-1][0]]:
            adj[v].pop()
        
        if not adj[v]:
            stack.pop()
            if incoming is not None:
                pos, idx, prev = incoming
                movement_path.append(
                    Movement(
                        route_idx=None if idx == 0 else idx, s=prev+1, t=v+1
                    )
                )

        else:
            pos, idx, u = adj[v].pop()
            if used[pos]: continue
            used[pos] = True
            stack.append((u, (pos, idx, v)))

    return movement_path[::-1]

def find_fun_trip(n: int, routes: Sequence[Route]) -> list[Movement] | None:
    if not routes: return []
    solv, edges, odds = is_solvable(n, routes)

    if not solv:
        return None

    if odds:
        start = odds[0]
    else:
        # find any vertex with degree > 0
        start = next((u for _, (u, v) in edges), 0)    
    return hierholtz(n, edges, start)

res1 = find_fun_trip(4, [
    (1, 2),
    (1, 3),
    (1, 4),
])
exp1 = [
    Movement(route_idx=1, s=2, t=1),
    Movement(route_idx=2, s=1, t=3),
    Movement(route_idx=None, s=3, t=1),
    Movement(route_idx=3, s=1, t=4),
]

assert res1 == exp1, f"got {res1}"

res2 = find_fun_trip(8, [
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (6, 5),
    (7, 5),
    (8, 5),
    (8, 5),
])
exp2 = None

assert res2 == exp2, f"got {res2}"

res3 = find_fun_trip(5, (
    (1, 2),
    (1, 2),
    (1, 3),
    (1, 4),
))

exp3 = [
    Movement(route_idx=1, s=1, t=2),
    Movement(route_idx=2, s=2, t=1),
    Movement(route_idx=3, s=1, t=3),
    Movement(route_idx=None, s=3, t=1),
    Movement(route_idx=4, s=1, t=4),
]

assert res3 == exp3, f"got {res3}"
