# given a graph, determine if it has an eulerian circuit
# if it does, give the vertex indices traversed, else return None
def check_graph_eulerian(n: int, edges: list[tuple[int, int]]) -> tuple[str, list[int]]:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    odd = [i for i in range(n) if deg[i] % 2]

    if len(odd) == 0:
        return "circuit", odd
    
    elif len(odd) == 2:
        return "walk", odd
    return "none", odd

def make_degrees_even(edges: list[tuple[int, int]], odd_vertices: list[int]):
    if len(odd_vertices) == 2:
        u, v = odd_vertices
        edges.append((u, v)) # add temporary edge
        return (u, v)
    return None 

def hierholzer(n: int, edges: list[tuple[int, int]], start: int) -> tuple[list[int], list[int]]:
    adj = [[] for _ in range(n)]
    used = [False] * len(edges)

    for idx, (u, v) in enumerate(edges):
        adj[u].append((idx, v))
        adj[v].append((idx, u))

    stack = [start]
    vertex_path = [] # store path of vertices traversed
    edge_path = [] # store indices of edges traversed
    
    while stack:
        v = stack[-1]

        # skip used edges
        while adj[v] and used[adj[v][-1][0]]:
            adj[v].pop()
        
        # dead end: add vertex to path
        if not adj[v]:
            vertex_path.append(stack.pop())
        else:
            # traverse unused edge
            idx, u = adj[v].pop()
            used[idx] = True
            stack.append(u)
            edge_path.append(idx)
        
    return vertex_path[::-1], edge_path

def get_eulerian_vertex_path(n: int, edges: list[tuple[int, int]], start: int) -> list[int] | None:
    etype, odd = check_graph_eulerian(n, edges)
    temp_edge = None

    if etype == "none":
        return None
    
    elif etype == "walk":
        temp_edge = make_degrees_even(edges, odd)
    
    start = odd[0] if odd else 0
    v_tour, edges_tour = hierholzer(n, edges, start)

    if temp_edge:
        u, v = temp_edge
        for i in range(len(v_tour) - 1):
                if (v_tour[i], v_tour[i + 1]) in [(u, v), (v, u)]:
                    v_tour = v_tour[i + 1:] + v_tour[1: i + 1] # skip temp edge
                    break
    
    return v_tour