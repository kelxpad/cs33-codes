class UnionFind:
    def __init__(self, n: int) -> None:
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
        # else, union by rank
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

def kruskals(n: int, edges: list[tuple[int, int, int]]) -> int:
    edges.sort(key=lambda x: x[2]) # where an edge is (u,v,w) and w is weight
    uf = UnionFind(n)
    mst_weight = 0
    edges_used = 0
    connected = False

    # you can also keep track of the mst's edges by putting them in a list
    for u, v, w in edges:
        if uf.union(u, v):
            mst_weight += w
            edges_used += 1
            connected = edges_used == n - 1
            if connected:
                break
    
    return mst_weight if connected else float("inf")


