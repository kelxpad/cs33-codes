# WRITE-UP
"""
The key difficulty of the problem is that we are not minimizing distance as usual shortest-path problems do, but the number of times the fuel tank is refilled, given a maximum distance `L` that can be travelled on one full tank.

To solve this, we separate the problem into two stages:
1. Determine which pairs of towns can be reached using one full tank.
2. Treat each such reachable pair as a single step and minimze the number of such steps needed.

This is achieved by constructing two graphs (distance and fuel) and applying Floyd-Warshall on both.

The core idea is transforming the problem from minimizing distance to minimizing refueling operations by compressing feasible routes into single steps: a layered graph approach.
"""

"""SKETCH PROOF
We prove that the algorithm correctly computes the minimum number of refuels.

Lemma 1. After the first Floyd-Warshall, dist[i][j] equals the shortest path distance between i and j.
- Floyd-Warshall correctly computes all-pairs shortest paths in weighted graphs with nonnegative edge weights.

Lemma 2. fuel[i][j] = 1 iff town j can be reached from town i without refueling.
- By definition, one liter of fuel is consumed per unit distance. Therefore, a route from i to j is feasible on one full tank exactly when dist[i][j] <= L.

Lemma 3. After the second Floyd-Warshall, fuel[i][j] equals the minimum number of full tanks needed to travel from i to j.
- The fuel graph treats each one-tank journey as an edge of weight 1. Floyd-Warshall computes the shortest path, which corresponds to the minimum number of tank segments.

Theorem. For any query (s, t), the algorithm outputs the minimum number of refuels required to travel from s to t.
- By Lemma 3, fuel[s][t] gives the minimum number of tanks used. Since the initial tank is already full, the number of refuels is exactly fuel[s][t] - 1.
- If no path exists, the algorithm correctly outputs -1.

"""

"""TIME COMPLEXITY ANALYSIS
Let N be the number of towns.
Distance matrix initialization    = O(N^2)
Floyd-Warshalls O(N^3)  + O(N^3)  = O(N^3)
Fuel matrix construction          = O(N^2)
Query answering                   = O(Q)

So, O(N^3 + Q)
"""

# CODE
"""
nodes = towns, towns are 1-indexed

reworded problem statement:
given a full tank L at the start, whats the MINIMUM
number of times he needs to full his tank going from
town s_i to town t_i?

possible insights from constraints:
- edges' upper bound is N(N - 1)/2, which could
mean the graph is dense

- maybe floyd-warshall? 300 nodes lang eh, which is fine for cubic
"""
import sys

def solution(n: int, l: int, edges: list[tuple[int, int, int]], queries: list[tuple[int, int]]) -> list[int]:
    # step 1: build distance matrix
    dist = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    for a, b, c in edges: # undirected graph naman, so we set both ways to c
        dist[a][b] = c
        dist[b][a] = c
    
    # step 2: floyd-warshall
    for k in range(n):
        for i in range(n):
            if dist[i][k] == float("inf"): # unreachable, no edge exists between them
                continue
            for j in range(n):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    
    # step 3: build "fuel-distance" matrix
    fuel = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        fuel[i][i] = 0
        for j in range(n):
            if dist[i][j] <= l: # you can go from town i to town j using exactly one full tank
                fuel[i][j] = 1 
    
    # step 4: floyd-warshall on the fuel "graph"
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if fuel[i][k] + fuel[k][j] < fuel[i][j]:
                    fuel[i][j] = fuel[i][k] + fuel[k][j]

    # answer queries in O(1)
    answers = []
    for s, t in queries:
        if fuel[s][t] == float("inf"):
            answers.append(-1)
        else:
            answers.append(max(0, fuel[s][t] - 1))            
    return answers

def main() -> None:
    input = sys.stdin.readline

    n, m, l = map(int, input().split())

    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a - 1, b - 1, c))
    
    q = int(input())
    queries = []
    for _ in range(q):
        s, t = map(int, input().split())
        queries.append((s - 1, t - 1))
    
    ans = solution(n, l, edges, queries)

    for x in ans:
        print(x)

if __name__ == "__main__":
    main()