def other(edge: tuple[int, int], i: int) -> int:
    """get vertex at other end of edge"""
    u, v = edge
    assert i in {u, v}
    return v if i == u else u

def get_degrees(n: int, edges: list[tuple[int, int]]) -> list[int]:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return deg

def dfs_reachable(n: int, adj: list[list[int]], start: int) -> list[bool]:
    """return which vertices are reachable from start using DFS"""
    stack = [start]
    vis = [False] * n
    vis[start] = True

    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not vis[v]:
                vis[v] = True
                stack.append(v)
    
    return vis

def is_bridge(n: int, edges: list[tuple[int, int]], used: list[bool], idx: int, u: int) -> bool:
    """check if the edge in edges[idx] is a bridge in the unused graph"""
    v = other(edges[idx], u)

    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        if i != idx and not used[i]:
            adj[a].append(b)
            adj[b].append(a)

    reachable = dfs_reachable(n, adj, u)
    return not reachable[v]

def fleury_edges(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    """return the Euler path as a sequence of edge indices starting from start"""
    used = [False] * len(edges)
    deg = get_degrees(n, edges)

    path: list[int] = []
    cur = start

    for _ in range(len(edges)):
        if deg[cur] == 0:
            return [] # dead end reached
        
        chosen = None
        for idx, (u, v) in enumerate(edges):
            if used[idx] or cur not in (u, v):
                continue
            # pick non-bridge if possible, or forced if deg[cur] == 1
            if deg[cur] == 1 or not is_bridge(n, edges, used, idx, cur):
                chosen = idx
                break
        
        if chosen is None:
            raise ValueError("No valid edge found")
        
        used[chosen] = True
        path.append(chosen)
        u, v = edges[chosen]
        deg[u] -= 1
        deg[v] -= 1
        cur = other(edges[chosen], cur)

    return path

def find_eul_path(n: int, edges: list[tuple[int, int]]) -> tuple[int, list[int]]:
    deg = get_degrees(n, edges)

    # choose start vertex
    # if the graph has an eulerian path, either all vertices have even degree
    # or there are only 2 vertices with odd degree

    odd = [i for i in range(n) if deg[i] % 2]
    if len(odd) == 0:
        start = next((i for i in range(n) if deg[i] > 0), 0)
    elif len(odd) == 2:
        start = odd[0]
    else:
        raise ValueError("No Euler path exists")
    
    path = fleury_edges(n, edges, start)

    if len(path) != len(edges):
        raise ValueError("Graph disconnected")
    
    return start, path

if __name__ == "__main__":
    edges = [
        (0, 1),
        (1, 2),
        (2, 0),
        (0, 4),
        (4, 3),
        (3, 0),
        (4, 5),
    ]
    print(find_eul_path(6, edges))