def check_graph_eulerian(n: int, edges: list[tuple[int, int]]) -> tuple[str, list[int]]:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
        
    odds = [i for i in range(n) if deg[i] % 2]

    if len(edges) == 0:
        return "circuit", odds
    elif len(edges) == 2:
        return "walk", odds
    return "none", odds

def make_graph_eulerian(odds: list[int], edges: list[tuple[int, int]]) -> tuple[int, int]:
    if len(odds) == 2:
        u, v = odds
        edges.append((u, v))
        return (u, v)
    return None

def hierholzer(n: int, edges: list[tuple[int, int]], start: int) -> tuple[list[int], list[int]]:
    used = [False] * len(edges)
    adj = [[] for _ in range(n)]
    vertex_path = []
    edges_path = []

    for idx, (u, v) in enumerate(edges):
        adj[u].append((idx, v))
        adj[v].append((idx, u))

    stack = [start]
    while stack:
        v = stack[-1]
        while adj[v] and used[adj[v][-1][0]]:
            adj[v].pop()

        if not adj[v]:
            vertex_path.append(stack.pop())
        
        else:
            # traverse unused edge
            idx, u = adj[v].pop()
            used[idx] = True
            stack.append(u)
            edges_path.append(idx)

    return vertex_path[::-1], edges_path

def get_eulerian_vertex_path(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    etype, odd = check_graph_eulerian(n, edges)
    temp_edge = None

    if etype == "none":
        return None
    
    elif etype == "walk":
        temp_edge = make_graph_eulerian(odd, edges)

    v_tour, e_tour = hierholzer(n, edges, start)
    if temp_edge:
        u, v = temp_edge
        for i in range(len(v_tour) - 1):
            if (v_tour[i], v_tour[i + 1]) in [(u, v), (v, u)]:
                v_tour = v_tour[i + 1:] + v_tour[1:i + 1]
                break

    return v_tour