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

def solution(n, edges, r_towns):
    # initialize distance matrix
    dist = [[float("inf")] * n for _ in range(n)]

    # distance between a node and itself is 0
    for i in range(n):
        dist[i][i] = 0
    
    for a, b, c in edges:
        dist[a][b] = min(dist[a][b], c)
        dist[b][a] = min(dist[b][a], c)
    
    # floyd-warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    # try all visit orders (figure out which order joisino should visit the required town)
    ans = float("inf")
    for perm in itertools.permutations(r_towns):
        cost = 0
        for i in range(len(perm) - 1):
            cost += dist[perm[i]][perm[i + 1]]
        ans = min(ans, cost)
    
    return ans

def main():
    input = sys.stdin.readline

    n, m, r = map(int, input().split())
    r_towns = list(map(lambda x: int(x) - 1, input().split())) # convert to 0 based as you read

    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a - 1, b - 1, c))
    
    print(solution(n, edges, r_towns))

if __name__ == "__main__":
    main()