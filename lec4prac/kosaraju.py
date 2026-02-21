# assumptions: graph[u] contains list of v such that u -> v
# nodes are 0..n-1
def kosaraju_scc(graph: list[list[int]]) -> list[list[int]]:
    n = len(graph)

    # phase 1: DFS on original graph
    visited = [False] * n
    finish_stack = []

    for start in range(n):
        if visited[start]:
            continue
    
    # stack holds (node, next neighbor index)
    stack = [(start, 0)]
    visited[start] = True

    while stack:
        u, idx = stack[-1]

        if idx < len(graph[u]):
            v = graph[u][idx]
            stack[-1] = (u, idx + 1)

            if not visited[v]:
                visited[v] = True
                stack.append((v, 0))
            else:
                # all neighbors processed
                stack.pop()
                finish_stack.append(u)

    # build reversed graph
    rev_graph = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            rev_graph[v].append(u)

    # DFS on reversed graph
    visited = [False] * n
    sccs = []

    while finish_stack:
        start = finish_stack.pop()
        if visited[start]:
            continue

        scc = []
        stack = [start]
        visited[start] = True

        while stack:
            u = stack.pop()
            scc.append(u)

            for v in rev_graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        
        sccs.append(scc)
    
    return sccs

