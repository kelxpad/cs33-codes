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
        self.max_pair = [[0] * (n + 1) for _ in range(self.log)]
        self.first_edge = [[0] * (n + 1) for _ in range(self.log)]
        self.last_edge = [[0] * (n + 1) for _ in range(self.log)]

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
                self.max_pair[0][to] = 0
                self.first_edge[0][to] = w
                self.last_edge[0][to] = w
                stack.append((to, v))
    
    def build_lifting(self, n: int) -> None:
        """binary lifting, precompute 2^k-th ancestor and max edge on jumps"""
        for k in range(1, self.log):
            for v in range(1, n + 1):
                p = self.parent[k - 1][v]
                self.parent[k][v] = self.parent[k - 1][p]
                self.max_edge[k][v] = max(self.max_edge[k - 1][v], self.max_edge[k - 1][p])
                self.max_pair[k][v] = max(
                    self.max_pair[k - 1][v],
                    self.max_pair[k - 1][p],
                    self.last_edge[k - 1][v] + self.first_edge[k - 1][p]
                )
                self.first_edge[k][v] = self.first_edge[k - 1][v]
                self.last_edge[k][v] = self.last_edge[k - 1][p]

    def lift(self, v: int, diff: int) -> tuple[int, int, int]:
        """return node lifted, max single edge, max conc pair along path"""
        best = 0
        best_pair = 0
        last = 0
        k = 0
        while diff:
            if diff & 1:
                best_pair = max(best_pair, self.max_pair[k][v], last + self.first_edge[k][v])
                best = max(best, self.max_edge[k][v])
                last = self.last_edge[k][v]
                v = self.parent[k][v]
            diff >>= 1
            k += 1
        return v, best, best_pair
    
    def lca(self, a: int, b: int) -> int:
        """get lowest common ancestor of a and b"""
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        a, _, _ = self.lift(a, self.depth[a] - self.depth[b])
        if a == b:
            return a
        for k in reversed(range(self.log)):
            if self.parent[k][a] != self.parent[k][b]:
                a = self.parent[k][a]
                b = self.parent[k][b]
        return self.parent[0][a]
    
    def path_best(self, a: int, b: int) -> tuple[int, int]:
        """find best single edge, best consecutive pair on path"""
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        best = best_pair = 0
        last_a = last_b = 0
        a, best_a, pair_a = self.lift(a, self.depth[a] - self.depth[b])
        best = max(best, best_a)
        best_pair = max(best_pair, pair_a)
        if a == b:
            return best, best_pair
        for k in reversed(range(self.log)):
            if self.parent[k][a] != self.parent[k][b]:
                best_pair = max(best_pair,
                                self.max_pair[k][a],
                                last_a + self.first_edge[k][a])
                best = max(best, self.max_edge[k][a])
                last_a = self.last_edge[k][a]
                best_pair = max(best_pair,
                                self.max_pair[k][b],
                                last_b + self.first_edge[k][b])
                best = max(best, self.max_edge[k][b])
                last_b = self.last_edge[k][b]

                a = self.parent[k][a]
                b = self.parent[k][b]

        edge_a = self.max_edge[0][a]
        edge_b = self.max_edge[0][b]
        best = max(best, edge_a, edge_b)
        best_pair = max(
            best_pair,
            self.max_pair[0][a],
            self.max_pair[0][b],
            last_a + edge_a,
            last_b + edge_b, #bruh
            edge_a + edge_b
        )
        return best, best_pair
    
    def distance(self, a, b):
        lca = self.lca(a, b)
        return self.pref[a] + self.pref[b] - 2*self.pref[lca]

    def compute_commute_time(self, a: int, b: int) -> int:
        if a == b: return 0
        path_sum = self.distance(a, b)
        best_single, best_pair = self.path_best(a, b)
        best_saving = max(best_single, best_pair)
        return 2 * path_sum - best_saving