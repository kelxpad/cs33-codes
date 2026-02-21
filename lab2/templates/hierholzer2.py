# given a graph, determine if it has an eulerian circuit
# if it does, give the edge indices traversed, else return None
def check_graph_eulerian(n: int, edges: list[tuple[int, int]]) -> tuple[str, list[int]]:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    odds = [i for i in range(n) if deg[i] % 2]

    if len(odds) == 0:
        return "circuit", odds
    
    if len(odds) == 2:
        return "walk", odds
    
    return "none", odds

def make_degrees_even(edges: list[tuple[int, int]], odd_vertices: list[int]) -> tuple[int, int]:
    if len(odd_vertices) == 2:
        u, v = odd_vertices
        edges.append((u, v))
        return len(edges) - 1
    return None

def hierholzer(n: int, edges: list[tuple[int, int]], start: int) -> tuple[list[int], list[int]]:
    adj = [[] for _ in range(n)]
    vertex_path = []
    edge_path = []
    used = [False] * len(edges)

    for idx, (u, v) in enumerate(edges):
        adj[u].append((idx, v))
        adj[v].append((idx, u))

    stack = [start]

    while stack:
        v = stack[-1]

        # skip used edges
        while adj[v] and used[adj[v][-1][0]]:
            adj[v].pop()

        if not adj[v]: # dead end: append vertex
            vertex_path.append(stack.pop())
        else:
            idx, u = adj[v].pop()
            used[idx] = True
            stack.append(u)
            edge_path.append(idx)
    
    return vertex_path[::-1], edge_path

def get_eulerian_edges_path(n: int, edges: list[tuple[int, int]], start: int) -> list[int] | None:
    etype, odd = check_graph_eulerian(n, edges)
    temp_edge = None

    if etype == "none":
        return None
    
    elif etype == "walk":
        temp_edge = make_degrees_even(edges, odd)
    
    # else: circuit
    v_tour, e_tour = hierholzer(n, edges, start)

    if temp_edge is not None:
        i = e_tour.index(temp_edge)
        e_tour = e_tour[i + 1:] + e_tour[:i]
    
    return e_tour

def check_if_graph_eulerian(n: int, edges: list[tuple[int, int]]):
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    odds = [i for i in range(n) if deg[i] % 2]
    
    if len(odds) == 0:
        return "circuit", odds
    if len(odds) == 2:
        return "walk", odds
    return "none", odds

def make_degrees_even(edges: list[tuple[int, int]], odds: list[int]):
    if len(odds) == 2:
        u,v = odds
        edges.append((u, v))
        return (u, v)
    return None
    
def hierholzer(n: int, edges: list[tuple[int, int]], start: int):
    used = [False] * len(edges)
    adj = [[] for _ in range(n)]

    for idx, (u, v) in enumerate(edges):
        adj[u].append((idx, v))
        adj[v].append((idx, u))

    vertex_path = []
    edges_path = []

    stack = [start]
    while stack:

        while adj[v] and used[adj[v][-1][0]]:
            adj[v].pop()

        if not adj[v]:
            vertex_path.append(stack.pop())
        
        else:
            idx, u = adj[v].pop()
            used[idx] = True
            edges_path.append(idx)
            stack.append(u)
    
    return vertex_path[::-1], edges_path

def get_eulerian_vertex_path(n: int, edges: list[tuple[int, int]], start: int):
    etype, odds = check_if_graph_eulerian()
    temp_edge = None
    if etype == "none":
        return None
    
    if etype == "walk":
        temp_edge = make_degrees_even(edges, odds)
    
    v_tour, _ = hierholzer(n, edges, start)
    # else, circuit
    if temp_edge:
        u, v = temp_edge
        for i in range(len(v_tour) - 1):
            if (v_tour[i], v_tour[i + 1]) in [(u, v), (v, u)]:
                v_tour = v_tour[i + 1:] + v_tour[1: i + 1]
                break
    return v_tour