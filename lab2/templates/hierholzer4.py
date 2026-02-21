def check_if_graph_eulerian(n: int, edges: list[tuple[int, int]]) -> tuple[str, list[int]]:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    odds = [i for i in range(n) if deg[i] % 2]

    if len(odds) == 0:
        return "circuit", odds
    
    elif len(odds) == 2:
        return "walk", odds
    return "none", odds
    
def make_degrees_even(edges: list[tuple[int, int]], odds):
    if len(odds) == 2:
        u, v = odds
        edges.append((u, v))
        return len(edges) - 1
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
            u, idx = adj[v].pop()
            used[idx] = True
            stack.append(u)
            edges_path.append(idx)
    
    return vertex_path[::-1], edges_path

def get_eulerian_edges_path(n: int, edges: list[tuple[int, int]], start: int) -> tuple[list[int], list[int]]:
    etype, odds = check_if_graph_eulerian(n, edges)
    temp_edge = None

    if etype == "none":
        return None
    
    elif etype == "walk":
        temp_edge = make_degrees_even(edges, odds)
    
    _, e_tour = hierholzer(n, edges, start)

    # else, circuit
    if temp_edge is not None:
        i = e_tour.index(temp_edge)
        e_tour = e_tour[i + 1:] + e_tour[:i]
        
    return e_tour