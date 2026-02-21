"""
roads = edges, towns = nodes
A, B, C = source, dest, weight
reworded problem statement:
visit R special towns in any order,
only the road distances beteen consecutive visited towns count

choose the visiting order that minimizes total road distance

CHOOSE AN ORDER OF TOWNS AND SUM THE SHORTEST PATHS BETWEEN THEM
other details:
- source will not be the same as the destination
- graph is undirected and complete (every town can be reached from every town by road)
- no negative cycles (all positive weights)
receive input

maybe we can use dijkstra? floyd-warshall better we are doing APSP
"""
import sys
import itertools

def get_path(u, v, nxt):
    if nxt[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path

def solution(n, edges, r_towns):
    # initialize distance matrix
    dist = [[float("inf")] * n for _ in range(n)]
    nxt = [[-1] * n for _ in range(n)]

    # distance between a node and itself is 0
    for i in range(n):
        dist[i][i] = 0
        nxt[i][i] = i
    
    for a, b, c in edges:
        if c < dist[a][b]:
            dist[a][b] = c
            dist[b][a] = c
            nxt[a][b] = b
            nxt[b][a] = a
    
    # floyd-warshall with path tracking
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    
    # find best visiting order
    best_cost = float("inf")
    best_perm = None

    for perm in itertools.permutations(r_towns):
        cost = 0
        for i in range(len(perm) - 1):
            cost += dist[perm[i]][perm[i + 1]]
        if cost < best_cost:
            best_cost = cost
            best_perm = perm
    
    # reconstruct full path
    full_path = []
    for i in range(len(best_perm) - 1):
        u = best_perm[i]
        v = best_perm[i + 1]
        segment = get_path(u, v, nxt)
        if i > 0:
            segment = segment[1:] # avoid duplicate town
        full_path.extend(segment)
    
    return best_cost, best_perm, full_path

def main():
    input = sys.stdin.readline

    n, m, r = map(int, input().split())
    r_towns = list(map(lambda x: int(x) - 1, input().split())) # convert to 0 based as you read

    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a - 1, b - 1, c))
    
    cost, order, path = solution(n, edges, r_towns)

    print(f"Minimum road distance: {cost}")
    print(f"Best visiting order: {[x + 1 for x in order]}")
    print(f"Full road path: {[x + 1 for x in path]}")
if __name__ == "__main__":
    main()