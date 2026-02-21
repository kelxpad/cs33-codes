"""
BOCCHI ZA ROKKU PLAN OF ATTACK: 
answer = 2 * sum(path) - max(best_single_edge, best_adj_edge_pair)
we treat path like merging segments, since each jump represents a segment of edges
the problem DOES NOT REQUIRE the two rides to be adjacnet
"""
from collections.abc import Sequence
from bocchi import Route

class CommuteTracker:
    def __init__(self, n: int, routes: Sequence[Route]) -> None:
        self.log = (n).bit_length()
        self.adj = self.edgelist_to_adj(n, routes)

        self.depth = [0] * (n + 1)
        self.pref = [0] * (n + 1)

        # for each node, prep their jump info
        self.parent = [[0] * (n + 1) for _ in range(self.log)]
        
        self.mx1 = [[0] * (n + 1) for _ in range(self.log)] # best single edge
        self.mx2 = [[0] * (n + 1) for _ in range(self.log)] # best adjacent pair
        self.first = [[0] * (n + 1) for _ in range(self.log)] # first edge weight
        self.last = [[0] * (n + 1) for _ in range(self.log)] # last edge weight

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
                self.pref[to] = self.pref[v] + w # prefix sum of weights from root

                self.mx1[0][to] = w
                self.mx2[0][to] = 0
                self.first[0][to] = w
                self.last[0][to] = w

                stack.append((to, v))
    
    def merge(self, k, v, p):
        # merge segment v->p and p->anc
        self.first[k][v] = self.first[k-1][v]
        self.last[k][v] = self.last[k-1][p]

        self.mx1[k][v] = max(self.mx1[k-1][v], self.mx1[k-1][p])

        self.mx2[k][v] = max(
            self.mx2[k-1][v],
            self.mx2[k-1][p],
            self.last[k-1][v] + self.first[k-1][p]
        ) 

    def build_lifting(self, n: int) -> None:
        """binary lifting, precompute 2^k-th ancestor and max edge on jumps"""
        for k in range(1, self.log):
            for v in range(1, n + 1):
                p = self.parent[k - 1][v]
                self.parent[k][v] = self.parent[k - 1][p]
                if p:
                    self.merge(k, v, p)

    def combine(self, seg, k, v):
        first, last, mx1, mx2 = seg

        if mx1 == -1:
            return (
                self.first[k][v],
                self.last[k][v],
                self.mx1[k][v],
                self.mx2[k][v],
            )
        new_first = first
        new_last = self.last[k][v]

        new_mx1 = max(mx1, self.mx1[k][v])
        new_mx2 = max(mx2, self.mx2[k][v], last+self.first[k][v])

        return (new_first, new_last, new_mx1, new_mx2)
    
    def lift(self, v: int, diff: int) -> tuple[int, int, int]:
        seg = (0, 0, 0, 0)
        k = 0
        while diff:
            if diff & 1:
                seg = self.combine(seg, k, v)
                v = self.parent[k][v]
            diff >>= 1
            k += 1
        return v, seg
    
    def path_segment(self, a: int, b: int) -> tuple[int, int, int, int]:
        seg_a = seg_b = (0, 0, 0, 0)

        if self.depth[a] < self.depth[b]:
            a, b = b, a

        a, seg_a = self.lift(a, self.depth[a] - self.depth[b])

        if a == b:
            return seg_a
        
        for k in reversed(range(self.log)):
            if self.parent[k][a] != self.parent[k][b]:
                seg_a = self.combine(seg_a, k, a)
                seg_b = self.combine(seg_b, k, b)
                a = self.parent[k][a]
                b = self.parent[k][b]
        
        seg_a = self.combine(seg_a, 0, a)
        seg_b = self.combine(seg_b, 0, b)

        if seg_b[2] != -1:
            seg_b = (seg_b[1], seg_b[0], seg_b[2], seg_b[3])
            seg_a = (seg_a[0], seg_b[1], max(seg_a[2], seg_b[2]), max(seg_a[3], seg_b[3], seg_a[1] + seg_b[0]))
        return seg_a
    
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
        
    def distance(self, a, b):
        """compute sum of weights on path"""
        lca = self.lca(a, b)
        return self.pref[a] + self.pref[b] - 2*self.pref[lca]

    def compute_commute_time(self, a: int, b: int) -> int:
        if a == b: return 0 # cost to go from node to a = 0

        seg = self.path_segment(a, b)
        best_single = seg[2]
        best_pair = seg[3]

        saving = max(best_single, best_pair)

        path_sum = self.pref[a] + self.pref[b] - 2*self.pref[self.lca(a, b)]
        return 2*path_sum - saving
            
if __name__ == "__main__":
    c = CommuteTracker(5, (
        Route(u=1, v=2, w=20),
        Route(u=2, v=3, w=21),
        Route(u=3, v=4, w=140),
        Route(u=4, v=5, w=145),
    ))

    assert c.compute_commute_time(1, 1) == 0
    assert c.compute_commute_time(1, 2) == 20
    assert c.compute_commute_time(1, 3) == 41
    assert c.compute_commute_time(1, 4) == 201
    assert c.compute_commute_time(1, 5) == 367