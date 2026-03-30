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

    def aug_l(self, start: int, vis_l: list[bool]) -> bool:
        n = len(self.adj)
        parent = [-1] * n
        via = [-1] * n

        vis_l[start] = True
        stack = [(start, 0)] # (left node, nxt edge idx)

        while stack:
            u, idx = stack[-1]

            if idx == len(self.adj[u]):
                stack.pop()
                continue
                
            v = self.adj[u][idx]
            stack[-1] = (u, idx + 1)

            w = self.match_r[v]
            if w == -1:
                cur_u = u
                cur_v = v
                while True:
                    self.match_l[cur_u] = cur_v
                    self.match_r[cur_v] = cur_u
                    if parent[cur_u] == -1:
                        break
                    cur_v = via[cur_u] # curve pls
                    cur_u = parent[cur_u]
                return True
            
            if not vis_l[w]:
                vis_l[w] = True
                parent[w] = u
                via[w] = v
                stack.append((w, 0))
        
        return False

    def aug_r(self, start: int, vis_l: list[bool], vis_r: list[bool]) -> bool:
        n = len(self.radj)
        parent = [-1] * n
        via = [-1] * n
        
        vis_r[start] = True
        stack = [(start, 0)] # (right node, nxt edge idx)

        while stack:
            v, idx = stack[-1]

            if idx == len(self.radj[v]):
                stack.pop()
                continue

            u = self.radj[v][idx]
            stack[-1] = (v, idx+1)

            if self.match_l[u] == v:
                continue
            if vis_l[u]:
                continue
            
            vis_l[u] = True
            w = self.match_l[u]

            if w == -1:
                cur_r = v
                cur_u = u
                while True:
                    self.match_l[cur_u] = cur_r
                    self.match_r[cur_r] = cur_u
                    if parent[cur_r] == -1:
                        break
                    cur_u = via[cur_r]
                    cur_r = parent[cur_r]
                return True
            
            if not vis_r[w]:
                parent[w] = v
                via[w] = u
                vis_r[w] = True
                stack.append((w, 0))

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
        while ptr < mis:
            res[ptr] = cost
            ptr += 1

    return res

print(immigrants_game((
    (3, 1, 4, 1),
    (5, 9, 2, 6),
)))