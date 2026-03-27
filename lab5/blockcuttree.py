class BlockCutTree:
    def __init__(self, n: int) -> None:
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

        self.bct_adj = []

        self.node_to_bcc = [[] for _ in range(self.n)]
    
    def add_edge(self, u: int, v: int) -> None:
        if u == v:
            self.bccs.append([(u, u)])
        else:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
    def dfs(self, u: int, parent: int) -> None:
        self.disc[u] = self.low[u] = self.time
        self.time += 1

        for v in self.adj[u]:
            # self.loop
            if v == u:
                continue
            
            if self.disc[v] == -1:
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
                        if e == (u,v) or e == (v,u):
                            break
                    self.bccs.append(bcc)
            
            elif v != parent and self.disc[v] < self.disc[u]:
                # back edge, avoid duplicates
                self.edge_stack.append((u, v))
                self.low[u] = min(self.low[u], self.disc[v])
    
    def build(self):
        """
        computes all BCCs and builds the BCT
        returns adjacency list of the block-cut tree
        """

        # find BCCs by running DFS on all components
        for i in range(self.n):
            if self.disc[i] == -1:
                self.dfs(i, -1)
        
        # build block-cut tree
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
        
        self.bct_adj = bct_adj
        return bct_adj