def bellman_ford(n: int, edges: list[tuple[int, int, int]],
                 source: int) -> tuple[None, None] | tuple[list[int], list[int]]:
    # step 1: initialize dist, parent, and source
    dist = [float("inf")] * n
    parent = [-1] * n
    dist[source] = 0 # set source vertex to 0

    # step 2: relax edges n - 1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]: # if distance of u + w is less than v
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break # no edges relaxed, cannot improve anymore

    # step 3: detect negative cycle
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
        # if shortest path could be made "shorter",
        # there is a negative cycle
            return None, None
        
    return dist, parent