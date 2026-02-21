import heapq

def prims(n: int, adj: list[list[tuple[int, int]]], start: int = 0) -> int | float:
    """
    adj[u] = list of (v, w)
    returns total weight of MST, or inf if grpah is disconnected
    """
    # step 1: initialize visited array, minheap, mst weight, taken vertices
    visited = [False] * n # track visited vertices
    min_heap = [(0, start, -1)] # (weight, vertex, parent)
    mst_weight = 0 # weight of mst so far
    taken = 0 # taken vertices

    # for rebuilding edges
    parent = [-1] * n

    while min_heap:
        w, u, p = heapq.heappop(min_heap)
        if visited[u]:
            continue
        
        visited[u] = True
        parent[u] = p
        mst_weight += w
        taken += 1

        if taken == n: # termination case: all vertices visited
            return mst_weight, parent
        
        for v, wt in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (wt, v, u))

    return float("inf"), None # graph not connected

"""
In Prim’s algorithm, the termination condition is taken = n because the 
algorithm grows the MST by adding vertices, whereas Kruskal’s grows the 
MST by adding edges and therefore stops at n − 1 edges.
"""

def prims_forest_edge_list(n: int, edges: list[tuple[int, int, float]]) -> tuple[list[float], list[int]]:
    # build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

        inf = float("inf")
        dist = [inf] * n
        parent = [-1] * n
        visited = [False] * n

        # run Prim's for each unvisited vertex
        for start in range(n):
            if visited[start]:
                continue # skip visited

            dist[start] = 0
            heap = [(0, start)]

            while heap:
                w, u = heapq.heappop(heap)
                if visited[u]: # skip visited
                    continue
                visited[u] = True # mark as visited

                for v, weight in adj[u]:
                    if not visited[v] and weight < dist[v]:
                        dist[v] = weight
                        parent[v] = u
                        heapq.heappush(heap, (dist[v], v))
    
    return dist, parent