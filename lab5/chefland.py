"""
a pair of nodes u,v is good iff:
there exist two edge-disjoint paths between them

by Menger's theoem:
go u->v and back without reusing edges iff
2 edge-disjoint paths

can we make the graph 2-edge-connected by adding <= 1 edge?

remove all bridges so that the remaining components are 2ECCs, forming
a bridge tree

a tree become 2-edge-connect if number of leaves <= 2 as you can connect
them with one edge

so the number of leaves L in the graph must be <= 2.

plan:
1. find all bridges (dfs + low-link)
2. build 2eccs
3. construct bridge tree
4. count number of leaf components
if l <= 2: "YES"
else: "NO"
"""

def chefland():
    # parse input
    n, m = map(int, input().split())
    adj = [[] for _ in range(n)]

    edges = []

    for i in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append((v, i))
        adj[v].append((u, i))
        edges.append((u, v))

    # find all bridges
    tin = [-1] * n
    low = [-1] * n
    visited = [False] * n
    is_bridge = [False] * m

    timer = 0

    def dfs(u, parent_edge) -> None:
        nonlocal timer
        visited[u] = True
        tin[u] = low[u] = timer
        timer += 1

        for v, eid in adj[u]:
            if eid == parent_edge:
                continue
            if visited[v]:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    is_bridge[eid] = True

    dfs(0, -1)

    # build 2ECCs

    comp = [-1] * n
    comp_id = 0

    def dfs_comp(u):
        stack = [u]
        comp[u] = comp_id
        while stack:
            x = stack.pop()
            for y, eid in adj[x]:
                if comp[y] == -1 and not is_bridge[eid]:
                    comp[y] = comp_id
                    stack.append(y)
    
    for i in range(n):
        if comp[i] == -1:
            dfs_comp(i)
            comp_id += 1
    
    # if there is only one component, it is already 2-edge-connected
    if comp_id == 1:
        print("YES")
        return

    # count degrees in bridge tree
    deg = [0] * comp_id

    for i, (u, v) in enumerate(edges):
        if is_bridge[i]:
            cu = comp[u]
            cv = comp[v]
            deg[cu] += 1; deg[cv] += 1

    # count leaves
    leaves = sum(1 for d in deg if d == 1)

    if leaves <= 2:
        print("YES")
        return
    
    print("NO")

if __name__ == "__main__":
    chefland()