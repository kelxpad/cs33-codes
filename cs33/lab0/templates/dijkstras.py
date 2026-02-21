import heapq

def dijkstras(n: int, adj: list[list[tuple[int, float]]], source: int) -> tuple[list[float], list[int]]:
    # initialize parent and dist arrays
    dist = [float("inf")] * n
    parent = [-1] * n
    dist[source] = 0

    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        # skip outdated entries in heap
        if d > dist[u]:
            continue

        for v, w in adj[u]:
            if dist[u] + w < dist[v]: # if distance of u + w < distance v
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))
    
    return dist, parent