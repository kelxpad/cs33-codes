"""
tree problem, between any two ports there is a 
unique simple path

3 pairwise distances = dist(l,z)+dist(z,n)+dist(n,l)//2
because each edge in the minimal subtree is counted twice during comp

"""
from collections.abc import Sequence
from pirate import Route # pyright: ignore until this gets resolved in my machine


class PiratePorts:
    def __init__(self, p: int, routes: Sequence[Route]) -> None:
        self.p = p
        self.routes = list(routes)
        self.adj = self.edgelist_to_adj()
        self.weights = [0] * (p)
        for idx, r in enumerate(routes, start=1):
            self.weights[idx-1] = r.d
        
        super().__init__()

    def edgelist_to_adj(self):
        adj = [[] for _ in range(self.p+1)]
        for idx, r in enumerate(self.routes, start=1):
            adj[r.p].append((r.q, idx))
            adj[r.q].append((r.p, idx))
        return adj

    def update_danger(self, i: int, d: int) -> None:
        self.weights[i-1] = d

    def dist(self, start):
        dist = [-1] * (self.p+1)
        dist[start] = 0
        stack = [start]

        while stack: 
            u = stack.pop()
            for v, idx in self.adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + self.weights[idx-1]
                    stack.append(v)
        return dist


    def get_meetup_danger(self, l: int, z: int, n: int) -> int:
        dist_l = self.dist(l)
        dist_z = self.dist(z)

        return (dist_l[z] + dist_l[n] + dist_z[n]) // 2

if __name__ == "__main__":
    ports = PiratePorts(6, (
    Route(p=1, q=2, d=40),
    Route(p=3, q=2, d=20),
    Route(p=4, q=5, d=80),
    Route(p=6, q=5, d=60),
    Route(p=5, q=2, d=35),
))

    assert ports.get_meetup_danger(1, 3, 5) == 95
    assert ports.get_meetup_danger(5, 3, 1) == 95
    assert ports.get_meetup_danger(4, 2, 5) == 115
    ports.update_danger(3, 64)
    assert ports.get_meetup_danger(4, 2, 5) == 99
    assert ports.get_meetup_danger(4, 3, 1) == 159
