"""
If he starts his attack on a city x
, he will be able to infect all cities connected to x
via a sequence of roads.
really sounds like a block cut tree problem

once we do get a block-cut tree:
well it is a tree, so if x is on the path from s to t AND x is an articulation point (since bcc have 2 edge-disjoint paths), 
then the answer is None
"""
from collections.abc import Sequence
from collections import deque
type Road = tuple[int, int]

class Quarantiner:
    def __init__(self, n: int, roads: Sequence[Road]) -> None:
        self.n = n
        self.adj = [[] for _ in range(n)]

        # DFS state
        self.disc = [-1] * n
        self.low = [0] * n
        self.time = 0

        # stack of edges (u, v)
        self.edge_stack = []

        # results
        self.bccs = [] # list of list of edges
        self.is_art = [False] * n
        self.bct_adj = []

        self.comp_id = [-1] * n
        self.comp_size = []

        self.node_to_bcc = [[] for _ in range(self.n)]

        for road in roads:
            x, y = road
            self.add_edge(x-1, y-1)

        self.build()
        self.build_components()
        self.build_lca()
        
        super().__init__()

    def add_edge(self, u: int, v: int) -> None:
        if u == v:
            self.bccs.append([(u, u)])
        else:
            self.adj[u].append(v)
            self.adj[v].append(u)

    def dfs(self, u: int, parent: int) -> None:
        self.disc[u] = self.low[u] = self.time
        self.time += 1

        child_count = 0
        for v in self.adj[u]:
            if v == u: # self loop
                continue

            if self.disc[v] == -1:
                child_count += 1
                # tree edge
                self.edge_stack.append((u, v))

                self.dfs(v, u)

                self.low[u] = min(self.low[u], self.low[v])

                # BCC condition
                if self.low[v] >= self.disc[u]:
                    bcc = []
                    while True:
                        e = self.edge_stack.pop()
                        bcc.append(e)
                        if e == (u, v) or e == (v, u):
                            break
                    self.bccs.append(bcc)
                
                # articheck (pls dont artichoke)
                if parent != -1 and self.low[v] >= self.disc[u]:
                    self.is_art[u] = True

            elif v != parent and self.disc[v] < self.disc[u]:
                # back edge, avoid duplicates
                self.edge_stack.append((u, v))
                self.low[u] = min(self.low[u], self.disc[v])

        # is the root a cut node?
        if parent == -1 and child_count > 1:
            self.is_art[u] = True

    def build_components(self) -> None:
        cid = 0
        for i in range(self.n):
            if self.comp_id[i] != -1:
                continue

            stack = [i]
            self.comp_id[i] = cid
            size = 1

            while stack:
                u = stack.pop()
                for v in self.adj[u]:
                    if self.comp_id[v] == -1:
                        self.comp_id[v] = cid
                        stack.append(v)
                        size += 1
            
            self.comp_size.append(size)
            cid += 1
        
    def build(self):
        """
        computes all BCCs and builds the BCT
        returns adjacency list of the BCT
        """

        # find BCCs by running DFS on all components
        for i in range(self.n):
            if self.disc[i] == -1:
                self.dfs(i, -1)
        
        # build bct, let:
        # nodes 0..n-1: original nodes
        # n..n+len(bccs)-1: BCC nodes

        total_nodes = self.n + len(self.bccs)
        bct_adj = [[] for _ in range(total_nodes)]

        for i, bcc in enumerate(self.bccs):
            bcc_node = self.n + i
            vertices = set()

            for u, v in bcc:
                vertices.add(u)
                vertices.add(v)

            for v in vertices:
                bct_adj[v].append(bcc_node)
                bct_adj[bcc_node].append(v)
                self.node_to_bcc[v].append(bcc_node)
        
        self.bct_adj =  bct_adj
        return bct_adj

    def build_lca(self) -> None:
        n = len(self.bct_adj)
        self.log = (n).bit_length()
        self.up = [[-1]*n for _ in range(self.log)]
        self.depth = [-1]*n
        self.art_pref = [0]*n

        for i in range(n):
            if self.depth[i] != -1:
                continue
            self.dfs_lca(i, -1)
        
        for k in range(1, self.log):
            for v in range(n):
                if self.up[k-1][v] != -1:
                    self.up[k][v] = self.up[k-1][self.up[k-1][v]]
    
    def dfs_lca(self, u: int, p: int) -> None:
        self.up[0][u] = p
        self.depth[u] = 0 if p == -1 else self.depth[p] + 1

        # count cut nodes
        add = 1 if (u < self.n and self.is_art[u]) else 0
        self.art_pref[u] = add if p == -1 else self.art_pref[p] + add

        for v in self.bct_adj[u]:
            if v == p:
                continue
            self.dfs_lca(v, u)
        
    def lca(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        diff = self.depth[u] - self.depth[v]
        for k in range(self.log):
            if diff & (1 << k):
                u = self.up[k][u]
        
        if u == v: return u

        for k in reversed(range(self.log)):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        
        return self.up[0][u]

    def count_quarantinables(self, s: int, t: int) -> int | None:
        s -= 1; t -= 1

        if self.comp_id[s] != self.comp_id[t]:
            return None
        
        l = self.lca(s, t)

        # articulation points on path
        bad = self.art_pref[s] + self.art_pref[t] - 2 * self.art_pref[l]
        if l < self.n and self.is_art[l]:
            bad += 1
        
        # endpoints bad, but avoid double counting
        bad += 2

        if self.is_art[s]:
            bad -= 1
        
        if self.is_art[t]:
            bad -= 1
        
        return self.n - bad
    
q = Quarantiner(10, (
    (5, 6),
    (6, 7),
    (6, 9),
    (9, 10),
    (7, 10),
))

assert q.count_quarantinables(5, 6) == 8, f"{q.count_quarantinables(5,6)}"  # 1, 2, 3, 4, 7, 8, 9, 10
assert q.count_quarantinables(5, 10) == 7  # 1, 2, 3, 4, 7, 9, 10
assert q.count_quarantinables(7, 9) == 8  # 1, 2, 3, 4, 5, 6, 8, 10
