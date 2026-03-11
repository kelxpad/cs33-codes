from collections.abc import Sequence
from collections import deque

class TripTracker:
    def __init__(self, v: Sequence[int], roads: Sequence[tuple[int,int]]):
        self.v = v
        self.n = len(v)
        self.roads = [(u-1, w-1) for u, w in roads]
        self.e = len(roads)
        self.adj = [[] for _ in range(self.n)]
        for i, (u,w) in enumerate(self.roads):
            self.adj[u].append((w,i))
            self.adj[w].append((u,i))

        self.blocked = [False]*self.e

        self.depths = [0]*self.n
        self.parents = [0]*self.n
        self.dist_from_root = [0]*self.n

        visited = [False]*self.n
        for i in range(self.n):
            if not visited[i]:
                self._dfs(i, visited)

        self.log = self.n.bit_length()
        self.anc = [[0]*self.n for _ in range(self.log)]
        self.anc[0] = self.parents[:]
        for k in range(1, self.log):
            for i in range(self.n):
                self.anc[k][i] = self.anc[k-1][self.anc[k-1][i]]

        self.signed_v = [
            self.v[i] if self.depths[i]%2==0 else -self.v[i]
            for i in range(self.n)
        ]

        self.component = list(range(self.n))
        self.next_component = self.n
        self._init_components()

    def _dfs(self, root, visited):
        stack = [(root, root)]
        while stack:
            u,p = stack.pop()
            if visited[u]: continue
            visited[u]=True
            self.parents[u]=p
            if u==p:
                self.depths[u]=0
                self.dist_from_root[u]=self.v[u]
            else:
                self.depths[u]=self.depths[p]+1
                signed = self.v[u] if self.depths[u]%2==0 else -self.v[u]
                self.dist_from_root[u] = self.dist_from_root[p] + signed
            for v,_ in self.adj[u]:
                if v!=p:
                    stack.append((v,u))

    def lca(self, u, v):
        if self.depths[u]<self.depths[v]:
            u,v=v,u
        diff = self.depths[u]-self.depths[v]
        for k in range(self.log):
            if diff>>k &1:
                u = self.anc[k][u]
        if u==v:
            return u
        for k in reversed(range(self.log)):
            if self.anc[k][u]!=self.anc[k][v]:
                u=self.anc[k][u]
                v=self.anc[k][v]
        return self.parents[u]

    def _init_components(self):
        visited = [False]*self.n
        for i in range(self.n):
            if not visited[i]:
                stack = [i]
                while stack:
                    u = stack.pop()
                    if visited[u]: continue
                    visited[u]=True
                    self.component[u]=i
                    for v,eid in self.adj[u]:
                        if not visited[v] and not self.blocked[eid]:
                            stack.append(v)

    def block(self, i:int) -> None:
        idx = i-1
        if self.blocked[idx]:
            return
        self.blocked[idx]=True
        u,v = self.roads[idx]

        old_comp = self.component[u]
        new_comp_id = self.next_component
        self.next_component += 1

        queue = deque([u])
        visited = [False]*self.n
        while queue:
            node = queue.popleft()
            if visited[node]: continue
            visited[node]=True
            self.component[node]=new_comp_id
            for nei,eid in self.adj[node]:
                if not self.blocked[eid] and self.component[nei]==old_comp and not visited[nei]:
                    queue.append(nei)

    def compute_trip_cost(self, a:int, b:int):
        a -= 1; b -= 1
        if self.component[a] != self.component[b]:
            return None
        c = self.lca(a,b)
        total = self.dist_from_root[a] + self.dist_from_root[b] - 2*self.dist_from_root[c] + self.signed_v[c]
        if self.depths[a]%2==1:
            total=-total
        return total

from collections.abc import Sequence
from collections import deque

"""
Link-Cut Tree for dynamic forest path queries.

For path a->b: cost = sum_{i=0}^{k-1} (-1)^i * v[path[i]]
            = sum_at_even_positions - sum_at_odd_positions

LCT stores for each splay subtree:
  sz:   number of nodes
  s0:   sum of v[x] at even 0-indexed positions (from shallow end of path)
  s1:   sum of v[x] at odd positions
Lazy: rev (bool) — reverse path direction, which swaps children and conditionally swaps s0/s1.

To compute cost(a,b): make_root(a), access(b), answer = s0 - s1 of the splay.
"""

class _N:
    def __init__(self, v: int):
        self.v = v
        self.sz = 1
        self.s0 = v   # position 0 is even → goes to s0
        self.s1 = 0
        self.rev = False
        self.par = None
        self.ch = [None, None]

def _is_root(x: _N) -> bool:
    p = x.par
    return p is None or (p.ch[0] is not x and p.ch[1] is not x)

def _sz(x: _N) -> int:
    return x.sz if x else 0

def _pull(x: _N):
    """Recompute x's aggregate from children and x.v."""
    l, r = x.ch
    sl = _sz(l)
    # x is at position sl (0-indexed) in the combined path
    # s0 = l.s0 + (x.v if sl%2==0 else 0) + (r.s0 if (sl+1)%2==0 else r.s1)
    # s1 = l.s1 + (x.v if sl%2==1 else 0) + (r.s0 if (sl+1)%2==1 else r.s1)
    # If (sl+1) is even: right's positions are even-shifted → r.s0 → s0, r.s1 → s1
    # If (sl+1) is odd: right's positions shift by odd → r.s0 → s1, r.s1 → s0
    x.sz = sl + 1 + _sz(r)
    s0 = (l.s0 if l else 0)
    s1 = (l.s1 if l else 0)
    if sl % 2 == 0: s0 += x.v
    else: s1 += x.v
    if r:
        if (sl + 1) % 2 == 0: s0 += r.s0; s1 += r.s1
        else: s0 += r.s1; s1 += r.s0
    x.s0 = s0; x.s1 = s1

def _apply_rev(x: _N):
    """Reverse path direction: swap children, swap s0/s1 iff sz is even."""
    x.ch[0], x.ch[1] = x.ch[1], x.ch[0]
    # Reversing path of length sz: new_pos[i]=sz-1-i.
    # Parities preserved iff sz is odd → swap s0/s1 only when sz is even.
    if x.sz % 2 == 0:
        x.s0, x.s1 = x.s1, x.s0
    x.rev = not x.rev

def _push(x: _N):
    if x.rev:
        if x.ch[0]: _apply_rev(x.ch[0])
        if x.ch[1]: _apply_rev(x.ch[1])
        x.rev = False

def _rot(x: _N):
    p = x.par; g = p.par; d = 1 if p.ch[1] is x else 0
    c = x.ch[1 - d]; p.ch[d] = c
    if c: c.par = p
    if g:
        if g.ch[0] is p: g.ch[0] = x
        elif g.ch[1] is p: g.ch[1] = x
    x.par = g; x.ch[1 - d] = p; p.par = x
    _pull(p); _pull(x)

def _splay(x: _N):
    stk = []; cur = x
    while not _is_root(cur): stk.append(cur); cur = cur.par
    stk.append(cur)
    for nd in reversed(stk): _push(nd)
    while not _is_root(x):
        p = x.par
        if not _is_root(p):
            g = p.par
            if (g.ch[0] is p) == (p.ch[0] is x): _rot(p)
            else: _rot(x)
        _rot(x)

def _access(x: _N) -> _N:
    last = None; cur = x
    while cur:
        _splay(cur)
        cur.ch[1] = last
        _pull(cur)
        last = cur; cur = cur.par
    _splay(x); return last

def _make_root(x: _N):
    """Make x the root of its represented tree."""
    _access(x)
    _apply_rev(x)

def _find_root(x: _N) -> _N:
    _access(x); _push(x)
    while x.ch[0]: x = x.ch[0]; _push(x)
    _splay(x); return x

def _link(u: _N, v: _N):
    """Link two trees by making v a child of u (u is root of its tree)."""
    _make_root(u)
    u.par = v

def _cut(u: _N, v: _N):
    """Cut edge between u and v."""
    _make_root(u)
    _access(v)
    # Now v is splay root, v.ch[0] should be u (u is v's parent since u is tree root)
    if v.ch[0] is u and u.ch[1] is None:
        v.ch[0] = None; u.par = None; _pull(v)
    else:
        # Shouldn't happen if edge exists; try other direction
        _make_root(v); _access(u)
        if u.ch[0] is v and v.ch[1] is None:
            u.ch[0] = None; v.par = None; _pull(u)

def _connected(a: _N, b: _N) -> bool:
    return _find_root(a) is _find_root(b)

def _path_cost(a: _N, b: _N) -> int:
    """Alternating sum starting from a: v[a] - v[...] + ..."""
    _make_root(a)
    _access(b)
    # b is now splay root; path a->b is in splay tree in order
    return b.s0 - b.s1


class TripTracker:
    def __init__(self, v: Sequence[int], roads: Sequence[tuple[int, int]]) -> None:
        n = len(v); r = len(roads)
        self._roads = [(0, 0)] + list(roads)
        self._blocked = [False] * (r + 1)
        self._nodes = [None] + [_N(vi) for vi in v]

        adj = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(roads, 1):
            adj[a].append((b, i)); adj[b].append((a, i))

        # Build forest using BFS (only link edges, no need for rooting)
        visited = [False] * (n + 1)
        for start in range(1, n + 1):
            if visited[start]: continue
            visited[start] = True
            q = deque([start])
            while q:
                u = q.popleft()
                for nb, ri in adj[u]:
                    if visited[nb]: continue
                    visited[nb] = True
                    # Link nb to u
                    self._nodes[nb].par = self._nodes[u]
                    q.append(nb)
        super().__init__()

    def block(self, i: int) -> None:
        if self._blocked[i]: return
        self._blocked[i] = True
        a, b = self._roads[i]
        _cut(self._nodes[a], self._nodes[b])

    def compute_trip_cost(self, a: int, b: int) -> int | None:
        na = self._nodes[a]; nb = self._nodes[b]
        if not _connected(na, nb): return None
        return _path_cost(na, nb)


if __name__ == '__main__':
    t = TripTracker((33, 21, 136, 173), ((1, 2), (2, 3), (3, 4)))
    r1 = t.compute_trip_cost(1, 4); assert r1 == -25, f"got {r1}"
    r2 = t.compute_trip_cost(1, 3); assert r2 == 148, f"got {r2}"
    t.block(2)
    r3 = t.compute_trip_cost(1, 4); assert r3 is None
    print("Sample tests passed!")

    t2 = TripTracker((5,), ()); assert t2.compute_trip_cost(1, 1) == 5
    t3 = TripTracker((1, 2), ()); assert t3.compute_trip_cost(1, 2) is None

    t4 = TripTracker((10, 20, 30), ((1, 2), (2, 3)))
    assert t4.compute_trip_cost(1, 3) == 20
    t4.block(1)
    assert t4.compute_trip_cost(1, 3) is None
    r = t4.compute_trip_cost(2, 3); assert r == -10, f"got {r}"

    t5 = TripTracker((10, 20, 30), ((1, 2), (2, 3)))
    t5.block(2)
    assert t5.compute_trip_cost(1, 3) is None
    assert t5.compute_trip_cost(1, 2) == -10

    t6 = TripTracker((5, 3, 7, 2), ((1, 2), (1, 3), (1, 4)))
    assert t6.compute_trip_cost(2, 3) == 5, f"got {t6.compute_trip_cost(2,3)}"
    assert t6.compute_trip_cost(2, 4) == 0, f"got {t6.compute_trip_cost(2,4)}"
    t6.block(1)
    assert t6.compute_trip_cost(2, 3) is None
    assert t6.compute_trip_cost(3, 4) == 4, f"got {t6.compute_trip_cost(3,4)}"

    t7 = TripTracker((1,2,3,4,5), ((1,2),(2,3),(3,4),(4,5)))
    assert t7.compute_trip_cost(1,5) == 3, f"got {t7.compute_trip_cost(1,5)}"
    assert t7.compute_trip_cost(3,5) == 4, f"got {t7.compute_trip_cost(3,5)}"
    assert t7.compute_trip_cost(2,4) == 3, f"got {t7.compute_trip_cost(2,4)}"
    t7.block(3)
    assert t7.compute_trip_cost(1,5) is None
    r = t7.compute_trip_cost(4,5); assert r == -1, f"got {r}"
    r = t7.compute_trip_cost(5,4); assert r == 1, f"got {r}"

    print("All tests passed!")


if __name__=="__main__":
    t = TripTracker((33, 21, 136, 173), (
        (1,2),
        (2,3),
        (3,4),
    ))

    # online queries
    print(t.compute_trip_cost(1,4))   # -25
    print(t.compute_trip_cost(1,3))   # 148
    t.block(2)
    print(t.compute_trip_cost(1,4))   # None
