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
                        size += v
            
            self.comp_size.append(size)
            cid += 1
    
    def separates(self, s: int, t: int, banned: int) -> bool:
        if banned == s or banned == t:
            return True
        seen = [False] * self.n
        seen[banned] = True
        q = deque([s])
        seen[s] = True

        while q:
            u = q.popleft()
            for v in self.adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
            
        return not seen[t]
    
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

    def count_quarantinables(self, s: int, t: int) -> int | None:
        s -= 1; t -= 1

        if self.comp_id[s] != self.comp_id[t]:
            return None

        visited = [False] * len(self.bct_adj)
        parent = [-1] * len(self.bct_adj)

        q = deque([s])
        visited[s] = True

        while q:
            u = q.popleft()
            for v in self.bct_adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    q.append(v)

        if not visited[t]:
            return None
                
        bad = 0
        for x in range(self.n):
            if self.separates(s, t, x):
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
