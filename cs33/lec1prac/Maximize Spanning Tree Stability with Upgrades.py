from typing import List
"""
- sort the edges in descending order of weights 
- try doing binary search on ans
- return -1 if cannot form an MST
- essentially trying to get the MINIMUM edge weight of the MAXIMUM spanning tree
- reading comp skillcheck
"""
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
    
    def is_connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

class Solution:
    def maxStability(self, n: int, edges: List[List[int]], k: int) -> int:
        # step 0: preprocess must-have edges
        initial_uf = UF(n)
        min_must_s = float("inf")

        for u, v, s, m in edges:
            if m == 1:
                min_must_s = min(min_must_s, s)
                if not initial_uf.union(u, v):
                    return -1 # if must-have edges form a cycle, then it is impossible to create an MST

        # check if we can build MST with min_stability >= mid
        def can_build(mid: int) -> bool:
            # step 1: mid cannot exceed min must-have edge strength
            if mid > min_must_s:
                return False
            
            # step 2: copy initial UF state
            uf = UF(n)
            uf.parent = initial_uf.parent[:]
            uf.rank = initial_uf.rank[:]
            upgrades_left = k

            # step 3: process optional edges
            upgrades_edges = []
            for u, v, s, m in edges:
                if m == 1:
                    continue # already handled at step 0
                if s >= mid:
                    uf.union(u, v)
                elif s * 2 >= mid:
                    upgrades_edges.append((u,v))
            
            # step 4: use upgrades greedily to connect components
            for u, v in upgrades_edges:
                if uf.is_connected(u, v):
                    continue # would form cycle, skip
                if upgrades_left == 0:
                    return False # cannot upgrade, cannot connect
                uf.union(u, v)
                upgrades_left -= 1 # upgrade successful
            
            # step 5: check connectivity
            root = uf.find(0)
            for i in range(n):
                if uf.find(i) != root: return False
            return True

        # step 6: binary search on min_stability
        low, high = -1, max(e[2] for e in edges) * 2
        while low < high:
            mid = low + (high - low + 1) // 2
            if can_build(mid):
                low = mid
            else:
                high = mid - 1
        return low