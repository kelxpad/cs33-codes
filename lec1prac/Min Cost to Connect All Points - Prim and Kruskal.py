import heapq # prim's
from typing import List

class DSU: # kruskal's 
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr: 
            return False
        # Else, union by rank
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

class Solution:
    def manhattan(self, p1: List[int], p2: List[int]) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def prim_mst(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1: return 0

        visited = [False] * n
        min_heap = [(0, 0)] # (cost, point_index)
        total_cost = 0
        edges_used = 0

        while edges_used < n:
            cost, u = heapq.heappop(min_heap)
            if visited[u]: continue
            visited[u] = True
            total_cost += cost
            edges_used += 1

            # add all edges from u to unvisited vertices
            for v in range(n):
                if not visited[v]:
                    heapq.heappush(min_heap, (self.manhattan(points[u], points[v]), v))
        return total_cost

    def kruskal_mst(self, points: List[List[int]]) -> int:
        n = len(points)
        # generate all edges with their Manhattan distance
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                # so edges is a list of tuples (dist, i, j)
                edges.append((self.manhattan(points[i], points[j]), i, j))
        
        edges.sort()

        dsu = DSU(n)
        total_cost = 0
        edges_used = 0

        for cost, u, v in edges:
            if dsu.union(u, v):
                total_cost += cost
                edges_used += 1
                if edges_used == n - 1:
                    break # MST complete

        return total_cost

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        return self.kruskal_mst(points)