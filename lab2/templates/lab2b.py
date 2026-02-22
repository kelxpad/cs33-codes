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
