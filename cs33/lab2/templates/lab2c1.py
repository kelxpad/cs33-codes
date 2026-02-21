"""
subway network is a tree
LCA looks good, euler tour + segtree
if a == b, ans = 0 because lecnotes
riding an edge with weight 0 gives no benefit

for path a ---> b,
run everything = 2 * total_weight
ride best edge once = save max_edge
"""
from collections.abc import Sequence
from bocchi import Route # pyright: ignore and shut the fuck up

class CommuteTracker:
    def __init__(self, n: int, routes: Sequence[Route]) -> None:
        self.log = (n).bit_length()
        self.adj = self.edgelist_to_adj(n, routes)

        self.depth = [0] * (n + 1)
        self.pref = [0] * (n + 1)
        self.parent = [[0] * (n + 1) for _ in range(self.log)]
        self.max_edge = [[0] * (n + 1) for _ in range(self.log)]

        self.dfs(1)
        self.build_lifting(n) # precompute higher ancestors and max edges
        super().__init__()
    
    def edgelist_to_adj(self, n, routes) -> list[list[tuple[int, int]]]:
        adj = [[] for _ in range(n + 1)]
        for r in routes: 
            adj[r.u].append((r.v, r.w))
            adj[r.v].append((r.u, r.w))
        return adj
    
    def dfs(self, root=1) -> None: 
        """precompute depth of nodes, parent, prefix sum of weights from root, weight of edge to parent"""
        stack = [(root, 0)]
        while stack:
            v, p = stack.pop()
            for to, w in self.adj[v]:
                if to == p:
                    continue
                self.depth[to] = self.depth[v] + 1
                self.parent[0][to] = v
                self.max_edge[0][to] = w # edge weight to parent
                self.pref[to] = self.pref[v] + w # prefix sum of weights from root
                stack.append((to, v))
    
    def build_lifting(self, n: int) -> None:
        """binary lifting, precompute 2^k-th ancestor and max edge on jumps"""
        for k in range(1, self.log):
            for v in range(1, n + 1):
                p = self.parent[k - 1][v]
                self.parent[k][v] = self.parent[k - 1][p]
                self.max_edge[k][v] = max(
                    self.max_edge[k - 1][v],
                    self.max_edge[k - 1][p]
                )

    def lift(self, v: int, diff: int) -> tuple[int, int]:
        """raise node v by diff levels, return new node and max edge on path"""
        best = 0
        k = 0
        while diff:
            if diff & 1:
                best = max(best, self.max_edge[k][v])
                v = self.parent[k][v]
            diff >>= 1
            k += 1
        return v, best
    
    def lca(self, a: int, b: int) -> int:
        """get lowest common ancestor of a and b"""
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        
        a, _ = self.lift(a, self.depth[a] - self.depth[b])

        if a == b:
            return a
        
        # lift both nodes until parents match
        for k in reversed(range(self.log)):
            if self.parent[k][a] != self.parent[k][b]:
                a = self.parent[k][a]
                b = self.parent[k][b]

        return self.parent[0][a]
    
    def path_max(self, a, b) -> int:
        """find lca, max edge weight along path"""
        best = 0

        if self.depth[a] < self.depth[b]:
            a, b = b, a
        
        # bring a up to b's depth and track max edge
        a, mx = self.lift(a, self.depth[a] - self.depth[b])
        best = max(best, mx)

        if a == b:
            return best
        
        # lift both until reach LCA
        for k in reversed(range(self.log)):
            if self.parent[k][a] != self.parent[k][b]:
                best = max(
                    best,
                    self.max_edge[k][a],
                    self.max_edge[k][b],
                )
                a = self.parent[k][a]
                b = self.parent[k][b]
        
        return max(best, self.max_edge[0][a], self.max_edge[0][b])
        
    def distance(self, a, b):
        """compute sum of weights on path"""
        lca = self.lca(a, b)
        return self.pref[a] + self.pref[b] - 2*self.pref[lca]

    def compute_commute_time(self, a: int, b: int) -> int:
        if a == b: return 0 # cost to go from node to a = 0

        path_sum = self.distance(a, b)
        best_edge = self.path_max(a, b)

        # run everywhere (2w) but ride the best edge once (save w)
        return 2 * path_sum - best_edge 
        
if __name__ == "__main__":
    c = CommuteTracker(7, (
    Route(u=1, v=2, w=11),
    Route(u=2, v=3, w=12),
    Route(u=4, v=5, w=30),
    Route(u=5, v=3, w=31),
    Route(u=3, v=6, w=32),
    Route(u=6, v=7, w=33),
))

    assert c.compute_commute_time(1, 1) == 0
    assert c.compute_commute_time(1, 7) == 143
    assert c.compute_commute_time(4, 7) == 219
#procrastinating on 2c2 