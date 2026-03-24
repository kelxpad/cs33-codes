import bisect
import sys
sys.setrecursionlimit(10**7)

inf = 10**18

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

class SegmentTree:
    def __init__(self, n: int) -> None:
        self.n = n
        self.seg = [inf] * (4 * n)

    def build(self, arr, idx, l, r):
        if l == r:
            self.seg[idx] = arr[l]
            return
        
        mid = (l + r) // 2
        self.build(arr, idx*2, l, mid)
        self.build(arr, idx*2+1, mid+1, r)
        self.seg[idx] = min(self.seg[idx*2], self.seg[idx*2+1])

    def update(self, idx, l, r, pos, val):
        if l == r:
            self.seg[idx] = val
            return
        mid = (l + r) // 2
        if pos <= mid:
            self.update(idx*2, l, mid, pos, val)
        else:
            self.update(idx*2+1, mid+1, r, pos, val)
        self.seg[idx] = min(self.seg[idx*2], self.seg[idx*2+1])

    def query(self, idx, l, r, ql, qr):
        if qr < l or r < ql:
            return inf
        if ql <= l and r <= qr:
            return self.seg[idx]
        mid = (l + r) // 2
        return min(
            self.query(idx*2, l, mid, ql, qr),
            self.query(idx*2+1, mid+1, r, ql, qr)
        ) 
    
class HLD:
    def __init__(self, adj, values):
        self.n = len(adj)
        self.adj = adj
        self.val = values

        self.parent = [-1] * self.n
        self.depth = [0] * self.n
        self.size = [0] * self.n
        self.heavy = [-1] * self.n

        self.head = [0] * self.n
        self.pos = [0] * self.n

        self.cur = 0

        self.dfs(0)
        self.decompose(0, 0)

        base = [0] * self.n
        for i in range(self.n):
            base[self.pos[i]] = self.val[i]
        
        self.seg = SegmentTree(self.n)
        self.seg.build(base, 1, 0, self.n-1)

    def dfs(self, u):
        self.size[u] = 1
        max_sub = 0
        for v in self.adj[u]:
            if v == self.parent[u]:
                continue
            self.parent[v] = u
            self.depth[v] = self.depth[u] + 1
            self.dfs(v)
            self.size[u] += self.size[v]
            if self.size[v] > max_sub:
                max_sub = self.size[v]
                self.heavy[u] = v
    
    def decompose(self, u, h):
        self.head[u] = h
        self.pos[u] = self.cur
        self. cur += 1

        if self.heavy[u] != -1:
            self.decompose(self.heavy[u], h)
        
        for v in self.adj[u]:
            if v != self.parent[u] and v != self.heavy[u]:
                self.decompose(v, v)
    
    def query(self, u, v):
        res = inf
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            res = min(res, self.seg.query(1, 0, self.n-1, self.pos[self.head[u]], self.pos[u]))
            u = self.parent[self.head[u]]

        if self.depth[u] > self.depth[v]:
            u, v = v, u
        res = min(res, self.seg.query(1, 0, self.n-1, self.pos[u], self.pos[v]))

        return res
    
    def update(self, u, val):
        self.seg.update(1, 0, self.n-1, self.pos[u], val)

def tourists():
    n, m, q = map(int, input().split())
    w = [int(input()) for _ in range(n)]
    
    bct = BlockCutTree(n)

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        bct.add_edge(u, v)
    
    bct_adj = bct.build()
    total = len(bct_adj)

    # BCT values
    bct_val = [inf] * total

    # original nodes
    for i in range(n):
        bct_val[i] = w[i]
    
    # BCC nodes
    bcc_sets = [set() for _ in range(len(bct.bccs))]

    for i, bcc in enumerate(bct.bccs):
        for u, v in bcc:
            bcc_sets[i].add(u)
            bcc_sets[i].add(v)
    
    # maintain sorted values
    bcc_vals = []

    for i, s in enumerate(bcc_sets):
        arr = sorted(w[v] for v in s)
        bcc_vals.append(arr)
        bct_val[n+i] = arr[0]
    
    hld = HLD(bct_adj, bct_val)

    for _ in range(q):
        line = input().split()
        if line[0] == "A":
            a = int(line[1]) - 1
            b = int(line[2]) - 1
            print(hld.query(a, b))
        else:
            a = int(line[1]) - 1
            new_w = int(line[2])

            old = w[a]
            w[a] = new_w

            hld.update(a, new_w)

            for bcc_node in bct.node_to_bcc[a]:
                idx = bcc_node - n
                arr = bcc_vals[idx]

                # remove old
                pos = bisect.bisect_left(arr, old)
                arr.pop(pos)

                # insert new
                bisect.insort(arr, new_w)

                new_min = arr[0]
                hld.update(bcc_node, new_min)

if __name__ == "__main__":
    tourists()