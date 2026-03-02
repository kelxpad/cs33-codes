"""
tree problem, between any two ports there is a 
unique simple path

3 pairwise distances = dist(l,z)+dist(z,n)+dist(n,l)//2
because each edge in the minimal subtree is counted twice during comp

we need to support edge weight updates, path distance queries
we achieve this via hld and segtree

goes like:
1. build adj list
2. dfs #1 computes subtree sizes, depth, parent, determines heavy child
3. dfs #2 (decomposition) assigns head of heavy chain and assigns position in base array
4. assign each edge's weight to the deeper node
bas[pos[node]] = edge_weight
5. build segtree over base array
6. path query decomposed with hld into O(log n) segs
"""

from collections.abc import Sequence
from pirate import Route

class PiratePorts:
    def __init__(self, p: int, routes: Sequence[Route]) -> None:
        self.n = p
        self.routes = list(routes)
        self.adj = self.edgelist_to_adj()

        self.parent = [0] * (p + 1)
        self.depth = [0] * (p + 1)
        self.size = [0] * (p + 1)
        self.heavy = [0] * (p + 1)

        self.head = [0] * (p + 1) # top node of heavy chain
        self.pos = [0] * (p + 1) # position in base arr
        self.cur_pos = 0

        # maps edge index to deeper endpoint node
        self.edge_to_node = [0] * p

        # dfs 1 and dfs 2 (decompose)
        self.dfs(1, 0)
        self.decompose(1, 1)

        # build segtree
        self.segsize = 1
        while self.segsize < p:
            self.segsize <<= 1
        self.seg = [0] * (2 * self.segsize)

        # intiialize segtree with edge weights
        for idx, r in enumerate(self.routes, start=1):
            node = self.edge_to_node[idx - 1]
            self.seg_update(self.pos[node], r.d)
        super().__init__()

    def edgelist_to_adj(self):
        adj = [[] for _ in range(self.n+1)]
        for idx, r in enumerate(self.routes, start=1):
            adj[r.p].append((r.q, idx))
            adj[r.q].append((r.p, idx))
        return adj

    def dfs(self, u: int, par: int) -> None:
        # compute subtree sizes, depth, parent, identify heavy child
        # assign edge->deeper node mapping
        self.size[u] = 1
        self.parent[u] = par
        max_size = 0

        for v, idx in self.adj[u]:
            if v == par: continue
            self.depth[v] = self.depth[u] + 1
            self.edge_to_node[idx - 1] = v
            self.dfs(v, u)

            self.size[u] += self.size[v]
            if self.size[v] > max_size:
                max_size = self.size[v]
                self.heavy[u] = v
    
    def decompose(self, u: int, h: int) -> None:
        # assign head of current heavy chain, assign pos in flat arr
        self.head[u] = h
        self.pos[u] = self.cur_pos
        self.cur_pos += 1

        # continue heavy chain
        if self.heavy[u]:
            self.decompose(self.heavy[u], h)
        
        # start new chains for light children
        for v, _ in self.adj[u]:
            if v != self.parent[u] and v != self.heavy[u]:
                self.decompose(v, v)
    
    def seg_update(self, i: int, value: int) -> None:
        # point update at index i
        i += self.segsize
        self.seg[i] = value
        i //= 2
        while i:
            self.seg[i] = self.seg[2*i] + self.seg[2*i+1]
            i //= 2
    
    def seg_query(self, l: int, r: int) -> int:
        # range sum query on [l, r]
        l += self.segsize
        r += self.segsize
        res = 0
        while l <= r:
            if l & 1:
                res += self.seg[l]
                l += 1
            if not (r & 1):
                res += self.seg[r]
                r -= 1
            l //= 2
            r //= 2
        return res
    
    def dist(self, a: int, b: int) -> int:
        res = 0

        # climb chains until both nodes are in same chain
        while self.head[a] != self.head[b]:
            if self.depth[self.head[a]] < self.depth[self.head[b]]:
                a,b = b, a
            res += self.seg_query(self.pos[self.head[a]], self.pos[a])
            a = self.parent[self.head[a]]

        # now same chain
        if self.depth[a] > self.depth[b]:
            a,b = b, a
        
        # skip lca node
        res += self.seg_query(self.pos[a] + 1, self.pos[b])
        return res
    
    def update_danger(self, i: int, d: int) -> None:
        node = self.edge_to_node[i - 1]
        self.seg_update(self.pos[node], d)

    def get_meetup_danger(self, l: int, z: int, n: int) -> int:
        return (self.dist(l, z) + self.dist(z, n) + self.dist(n, l)) // 2

if __name__ == "__main__":
    ports = PiratePorts(6, (
    Route(p=1, q=2, d=40),
    Route(p=3, q=2, d=20),
    Route(p=4, q=5, d=80),
    Route(p=6, q=5, d=60),
    Route(p=5, q=2, d=35),
))

    assert ports.get_meetup_danger(1, 3, 5) == 95, f"got {ports.get_meetup_danger(1, 3, 5)}"
    assert ports.get_meetup_danger(5, 3, 1) == 95
    assert ports.get_meetup_danger(4, 2, 5) == 115
    ports.update_danger(3, 64)
    assert ports.get_meetup_danger(4, 2, 5) == 99
    assert ports.get_meetup_danger(4, 3, 1) == 159