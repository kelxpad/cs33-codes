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
type Road = tuple[int, int]

class Quarantiner:
    def __init__(self, n: int, roads: Sequence[Road]) -> None:
        self.n = n
        self.adj = [[] for _ in range(n)] # (to, eid)

        # Tarjan / BCC state
        self.disc = [-1] * n
        self.low = [0] * n
        self.time = 0
        self.edge_count = 0

        self.edge_stack = [] # (u, v, eid)
        self.bccs = [] # list of list of edges
        self.is_art = [False] * n

        self.comp_id = [-1] * n
        self.bct_adj = []

        for x, y in roads:
            self.add_edge(x-1, y-1)

        self.build()
        self.build_components()
        self.build_lca()
        super().__init__()

    def add_edge(self, u: int, v: int) -> None:
        if u == v:
            self.bccs.append([(u, v, -1)])
            return
        
        eid = self.edge_count
        self.edge_count += 1
        self.adj[u].append((v, eid))
        self.adj[v].append((u, eid))

    def dfs(self, u: int, parent: int) -> None:
        self.disc[u] = self.low[u] = self.time
        self.time += 1

        child_count = 0
        for v, eid in self.adj[u]:
            if eid == parent:
                continue

            if self.disc[v] == -1:
                child_count += 1
                # tree edge
                self.edge_stack.append((u, v, eid))

                self.dfs(v, eid)

                self.low[u] = min(self.low[u], self.low[v])

                # BCC condition
                if self.low[v] >= self.disc[u]:
                    if parent != -1:
                        self.is_art[u] = True

                    bcc = []
                    while True:
                        e = self.edge_stack.pop()
                        bcc.append(e)
                        if e[2] == eid:
                            break
                    self.bccs.append(bcc)
                
            elif self.disc[v] < self.disc[u]:
                # back edge
                self.edge_stack.append((u, v, eid))
                self.low[u] = min(self.low[u], self.disc[v])
                
        # is root a cut node?
        if parent == -1 and child_count > 1:
            self.is_art[u] = True

    def build_components(self) -> None:
        cid = 0
        for i in range(self.n):
            if self.comp_id[i] != -1:
                continue

            stack = [i]
            self.comp_id[i] = cid
            while stack:
                u = stack.pop()
                for v, _ in self.adj[u]:
                    if self.comp_id[v] == -1:
                        self.comp_id[v] = cid
                        stack.append(v)
            cid += 1
        
    def build(self) -> None:
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

        total = self.n + len(self.bccs)
        bct = [[] for _ in range(total)]

        for i, bcc in enumerate(self.bccs):
            node = self.n + i
            verts = set()
            for u, v, _ in bcc:
                verts.add(u)
                verts.add(v)

            for v in verts:
                bct[v].append(node)
                bct[node].append(v)
        
        self.bct_adj = bct

    def build_lca(self) -> None:
        n = len(self.bct_adj)
        self.log = n.bit_length()
        self.up = [[-1]*n for _ in range(self.log)]
        self.depth = [-1]*n
        self.art_pref = [0]*n

        for i in range(n):
            if self.depth[i] == -1:
                self.dfs_lca(i, -1)
        
        for k in range(1, self.log):
            prev = self.up[k - 1]
            cur = self.up[k]
            for v in range(n):
                p = prev[v]
                if p != -1:
                    cur[v] = prev[p]
    
    def dfs_lca(self, u: int, p: int) -> None:
        self.up[0][u] = p
        self.depth[u] = 0 if p == -1 else self.depth[p] + 1

        # count cut nodes
        add = 1 if (u < self.n and self.is_art[u]) else 0
        self.art_pref[u] = add if p == -1 else self.art_pref[p] + add

        for v in self.bct_adj[u]:
            if v != p:
                self.dfs_lca(v, u)
        
    def lca(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        diff = self.depth[u] - self.depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = self.up[bit][u]
            diff >>= 1
            bit += 1
        
        if u == v:
            return u
        
        for k in range(self.log - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        
        return self.up[0][u]

    def count_quarantinables(self, s: int, t: int) -> int | None:
        s -= 1; t -= 1

        if self.comp_id[s] != self.comp_id[t]:
            return None
        
        if s == t:
            return self.n - 1
        
        l = self.lca(s, t)

        # articulation points on path
        arts_on_path = self.art_pref[s] + self.art_pref[t] - 2 * self.art_pref[l]
        if l < self.n and self.is_art[l]:
            arts_on_path += 1
        
        bad = arts_on_path
        if not self.is_art[s]:
            bad += 1
        if not self.is_art[t]:
            bad += 1
        
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
