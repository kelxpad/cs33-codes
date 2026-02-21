from collections.abc import Sequence
type Hall = tuple[int, int]

class UnionFind:
    def __init__(self, n: int):
        self.rank = [0] * n
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) 
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        # else, union by rank
        if self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        elif self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        else:
            self.rank[xr] += 1
            self.parent[yr] = xr
        return True


def bf_trappable_halls(n: int, halls: Sequence[Hall]) -> list[int]:
    # bruteforce idea: try removing the edge, check connectivity

    ans = []
    
    len_h = len(halls)

    for i in range(len_h):
        _halls = halls[:i] + halls[i + 1:]

        uf = UnionFind(n)
        for hall in _halls:
            x, y = hall
            uf.union(x - 1, y - 1)

        if uf.find(0) != uf.find(n - 1):
            ans.append(i + 1)
            
    return ans
