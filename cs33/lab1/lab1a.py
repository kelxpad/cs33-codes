"""
n = nodes
h = edges

use tarjan to find bridges then return them
NOTE: ik may mali pa dito im just about to experiment with smthn how to identify bridges

"""
from collections.abc import Sequence
type Hall = tuple[int, int]

def find_bridges(n: int, adj: list[list[tuple[int, int]]], m: int) -> list[bool]:
    tin = [-1] * n
    low = [0] * n
    is_bridge = [False] * m
    timer = 0

    for start in range(n):
        if tin[start] != -1:
            continue

        # (node, parent_edge_id, next_neighbor_index)
        stack = [(start, -1, 0)]

        while stack:
            u, pe, idx = stack.pop()

            if idx == 0:
                tin[u] = low[u] = timer
                timer += 1

            if idx < len(adj[u]):
                v, eid = adj[u][idx]

                # resume u after this neighbor
                stack.append((u, pe, idx + 1))

                if eid == pe:
                    continue

                if tin[v] == -1:
                    stack.append((v, eid, 0))
                
                else:
                    # back edge
                    low[u] = min(low[u], tin[v])
            
            else:
                # finishing u, propagate low-link to parent
                if pe != -1:
                    # find parent node via parent edge
                    for v, eid in adj[u]:
                        if eid == pe:
                            parent = v
                            break
                    
                    if low[u] > tin[parent]:
                        is_bridge[pe] = True
                    
                    low[parent] = min(low[parent], low[u])
        
    return is_bridge
    
def trappable_halls(n: int, halls: Sequence[Hall]) -> list[int]:
    # build adjacency list with edge indices
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(halls):
        u -= 1
        v -= 1
        adj[u].append((v, i))
        adj[v].append((u, i))
    
    # find all bridges
    is_bridge = find_bridges(n, adj, len(halls))

    # for this next bit, we only consider the bridges between 1 and n

    # build graph ignoring bridges(2-edge connected components)

    comp = [-1] * n
    cid = 0

    for i in range(n):
        if comp[i] != -1:
            continue

        stack = [i]
        comp[i] = cid

        while stack:
            u = stack.pop()
            for v, eid in adj[u]:
                if not is_bridge[eid] and comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        
        cid += 1

    # build bridge tree
    tree = [[] for _ in range(cid)]
    for eid, (u, v) in enumerate(halls):
        if is_bridge[eid]:
            cu = comp[u - 1]
            cv = comp[v - 1]
            tree[cu].append((cv, eid))
            tree[cv].append((cu, eid))
        
    # find path from comp(1) to comp(n)
    start = comp[0]
    target = comp[n - 1]

    parent_edge = [-1] * cid
    visited = [False] * cid
    stack = [start]
    visited[start] = True

    while stack:
        u = stack.pop()
        if u == target:
            break
        for v, eid in tree[u]:
            if not visited[v]:
                visited[v] = True
                parent_edge[v] = eid
                stack.append(v)

    # collect bridge edges on the path
    ans = []
    cur = target
    while cur != start:
        eid = parent_edge[cur]
        ans.append(eid + 1) # convert to 1-indexed
        u, v = halls[eid]
        cur = comp[u - 1] if comp[v - 1] == cur else comp[v - 1]

    ans.sort()
    return ans 


# removing (1, 2) and (3, 5) disconnects node 1 and node n from the graph respectively
res1 = trappable_halls(5, [
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 4),
    (3, 5),
])

exp1 = [1, 5]

# there is no such edge you can remove that disconnect node 1 and node n from the component
res2 = trappable_halls(5, [
    (1, 3), 
    (3, 5),
    (5, 2),
    (5, 1),
    (3, 4),
])

exp2 = []

assert res1 == exp1, f"got {res1}"
assert res2 == exp2, f"got {res2}"