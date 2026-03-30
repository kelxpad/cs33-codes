"""
separate add_edge into add_left and add_right for 
ensuring left -> right bipartite traversal
"""
from collections.abc import Sequence

class Kuhn:
    def __init__(self) -> None:
        self.adj = [] # left -> right
        self.radj = [] # right -> left
        self.match_l = []
        self.match_r = []
    
    def add_left(self) -> int:
        self.adj.append([])
        self.match_l.append(-1)
        return len(self.adj) - 1
    
    def add_right(self) -> int:
        self.radj.append([])
        self.match_r.append(-1)
        return len(self.match_r) - 1
    
    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)
        self.radj[v].append(u)

    def aug_l(self, u: int, vis_l: list[bool]) -> bool:
        n = len(self.adj)
        parent = [-1] * n; via = [-1]
        if vis_l[u]:
            return False
        vis_l[u] = True
        for v in self.adj[u]:
            if self.match_r[v] == -1 or self.aug_l(self.match_r[v], vis_l):
                self.match_l[u] = v
                self.match_r[v] = u
                return True
        return False
    
    def aug_r(self, v: int, vis_l: list[bool], vis_r: list[bool]) -> bool:
        if vis_r[v]:
            return False
        vis_r[v] = True
        for u in self.radj[v]:
            if self.match_l[u] == v:
                continue
            if vis_l[u]:
                continue
            vis_l[u] = True
            if self.match_l[u] == -1 or self.aug_r(self.match_l[u], vis_l, vis_r):
                self.match_l[u] = v
                self.match_r[v] = u
                return True
        return False
    
def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    if not x or not x[0]:
        return []
    r, c = len(x), len(x[0])
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    # sort cells by cost
    cells = sorted((x[i][j], i, j) for i in range(r) for j in range(c))

    kuhn = Kuhn()

    id_l = {}
    id_r = {}

    matching = 0
    res = [-1] * (r * c)
    ptr = 0 # how many answers filled

    for cost, i, j in cells:
        # add node
        if (i + j) % 2 == 0:
            u = kuhn.add_left()
            id_l[(i, j)] = u

            # add edges
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if (ni, nj) in id_r:
                    kuhn.add_edge(u, id_r[(ni, nj)])
            
            if kuhn.aug_l(u, [False] * len(kuhn.adj)):
                matching += 1

        # but for right this time
        else:
            v = kuhn.add_right()
            id_r[(i, j)] = v

            for di, dj in moves:
                ni, nj = i + di, j + dj
                if (ni, nj) in id_l:
                    kuhn.add_edge(id_l[(ni, nj)], v)
            
            if kuhn.aug_r(v, [False] * len(kuhn.adj), [False] * len(kuhn.radj)):
                matching += 1

        total = len(kuhn.match_l) + len(kuhn.match_r)
        mis = total - matching

        # fill answers
        while ptr < mis:
            res[ptr] = cost
            ptr += 1

    return res

print(immigrants_game((
    (3, 1, 4, 1),
    (5, 9, 2, 6),
)))

