from typing import List

class UF:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr: return False
        # else, union by rank
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

def get_weight(e: List[int]): return e[2]

class Solution:
    def kruskal_mst(self, n: int, edges: List[List[int]], skip: int = None, force: int = None) -> int:
        uf = UF(n)
        cost = 0
        used = 0

        # force include an edge first
        if force is not None:
            u, v, w, _ = edges[force]
            if uf.union(u, v):
                cost += w
                used += 1

        for i, (u, v, w, _) in enumerate(edges):
            if i == skip: continue
            if uf.union(u, v):
                cost += w
                used += 1
                if used == n - 1:
                    break

        return cost if used == n - 1 else float("inf") # return inf when graph is disconnected

    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # attach original index to edges
        edges = [(u, v, w, i) for i, (u, v, w) in enumerate(edges)]
        edges.sort(key=get_weight)

        base_mst = self.kruskal_mst(n, edges)
        critical, pseudo = [], []

        for i in range(len(edges)):
            # test if edge i is critical (appears in all MST)
            if self.kruskal_mst(n, edges, skip=i) > base_mst:
                critical.append(edges[i][3])
            # test if edge i is pseudo-critical (appears in some MST, but not all)
            elif self.kruskal_mst(n, edges, force=i) == base_mst:
                pseudo.append(edges[i][3])
        
        return [critical, pseudo]


