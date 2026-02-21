from collections.abc import Sequence
type Point = tuple[int, int]

class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr: 
            return False
        # else, union by rank
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True
    
class DoritosGame:
    def __init__(self, initial_locations: Sequence[Point]) -> None:
        self.uf = UnionFind(0) # start empty
        self.vertex_id = {}
        self.edges = set()
        self.triangles = set()

        self.v = 0
        self.e = 0
        self.c = 0

        for p in initial_locations:
            self.place_dorito(p)
        
        super().__init__()

    # grow union-find storage when adding a vertex
    def _add_vertex(self, p: Point) -> int:
        if p in self.vertex_id:
            return self.vertex_id[p]
        
        vid = self.v
        self.vertex_id[p] = vid

        self.uf.parent.append(vid)
        self.uf.rank.append(0)

        self.v += 1
        self.c += 1

        return vid
    
    def _add_edge(self, a: Point, b: Point) -> None:
        if a > b:
            a, b = b, a
        if (a, b) in self.edges:
            return # already there

        self.edges.add((a, b))
        self.e += 1

        va = self._add_vertex(a)
        vb = self._add_vertex(b)

        if self.uf.union(va, vb):
            self.c -= 1 # two components joined together into one


    def place_dorito(self, p: Point) -> None:
        if p in self.triangles:
            return
        self.triangles.add(p)

        x, y = p
        a = (x,y)
        b = (x + 1, y)
        c = (x, y + 1)

        self._add_edge(a, b)
        self._add_edge(a, c)
        self._add_edge(b, c)

    def count_regions(self) -> int:
        # regions = e - v + c
        return self.e - self.v + self.c