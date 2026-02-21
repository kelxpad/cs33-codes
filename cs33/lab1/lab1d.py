"""
territories = sccs
adding any bidirectional edge between two different
sccs always reduces the number of sccs
...which means we dont actually need to test for
reachability

we count the number of unordered pairs of nodes that lie in different SCCs
"""
from collections.abc import Sequence
type Gate = tuple[int, int]

def territory_shifts(n: int, gates: Sequence[Gate]) -> int:
    if n <= 1: return 0 # aint nothing shifting here boi

    # build graph, 0-indexed
    adj = [[] for _ in range(n)]
    for u, v in gates:
        adj[u - 1].append(v - 1)

    # tarjan scc
    index = 0
    stack = []
    on_stack = [False] * n
    ids = [-1] * n
    low = [0] * n
    scc_id = [-1] * n
    scc_count = 0

    for start in range(n):
        if ids[start] != -1:
            continue
        
        call_stack = [(start, 0)]
        parent = {start: None}
        while call_stack:
            u, i = call_stack.pop()

            # first time we see u
            if i == 0:
                ids[u] = low[u] = index
                index += 1
                stack.append(u)
                on_stack[u] = True
            
            if i < len(adj[u]):
                v = adj[u][i]

                # resume u after exploring v
                call_stack.append((u, i + 1))

                if ids[v] == -1:
                    parent[v] = u
                    call_stack.append((v, 0))
                elif on_stack[v]:
                    low[u] = min(low[u], ids[v])
            
            else:
                # all neighbors processed, simulate return
                if ids[u] == low[u]:
                    while True:
                        x = stack.pop()
                        on_stack[x] = False
                        scc_id[x] = scc_count
                        if x == u:
                            break
                    scc_count += 1
                
                p = parent.get(u)
                if p is not None:
                    low[p] = min(low[p], low[u])
    
    scc_size = [0] * scc_count
    for u in range(n):
        scc_size[scc_id[u]] += 1

    total_pairs = n * (n - 1) // 2
    same_scc_pairs = sum(sz * (sz - 1) // 2 for sz in scc_size)

    return total_pairs - same_scc_pairs

res1 = territory_shifts(5, [
    (1, 2),
    (4, 5),
    (3, 1),
    (3, 4),
    (2, 3),
    (5, 4),
])

exp1 = 6

assert res1 == exp1, f"got {res1}"