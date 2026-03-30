"""
separate add_edge into add_left and add_right for 
ensuring left -> right bipartite traversal
"""
from collections.abc import Sequence

class Kuhn:
    def __init__(self) -> None:
        self.adj = []; self.radj = []; self.radj = []; self.match_l = []; self.match_r = []; self.seen_l = []; self.seen_r = []; self.par_l = []; self.par_r = []; self.via_l = []; self.via_r = []; self.stamp = 0

    def add_left(self) -> int:
        self.adj.append([]); self.match_l.append(-1); self.seen_l.append(0); self.par_l.append(-1); self.via_l.append(-1); return len(self.adj) - 1

    def add_right(self) -> int:
        self.radj.append([]); self.match_r.append(-1); self.seen_r.append(0); self.par_r.append(-1); self.via_r.append(-1); return len(self.radj) - 1

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)
        self.radj[v].append(u)

    def aug_l(self, start: int) -> bool:
        self.stamp += 1; st = self.stamp; adj = self.adj; ml = self.match_l; mr = self.match_r; seen_l = self.seen_l; par = self.par_l; via = self.via_l

        seen_l[start] = st; par[start] = -1; stack_u = [start]; stack_i = [0]

        while stack_u:
            u = stack_u[-1]
            i = stack_i[-1]
            if i == len(adj[u]):
                stack_u.pop()
                stack_i.pop()
                continue

            stack_i[-1] = i + 1
            v = adj[u][i]
            w = mr[v]

            if w == -1:
                cur_u = u
                cur_v = v
                while True:
                    ml[cur_u] = cur_v
                    mr[cur_v] = cur_u
                    pu = par[cur_u]
                    if pu == -1:
                        return True
                    cur_v = via[cur_u]
                    cur_u = pu

            elif seen_l[w] != st:
                seen_l[w] = st; par[w] = u; via[w] = v; stack_u.append(w); stack_i.append(0)

        return False

    def aug_r(self, start: int) -> bool:
        self.stamp += 1; st = self.stamp; adj = self.radj; ml = self.match_l; mr = self.match_r; seen_l = self.seen_l; seen_r = self.seen_r; par = self.par_r; via = self.via_r

        seen_r[start] = st
        par[start] = -1
        stack_v = [start]
        stack_i = [0]

        while stack_v:
            v = stack_v[-1]
            i = stack_i[-1]
            if i == len(adj[v]):
                stack_v.pop()
                stack_i.pop()
                continue

            stack_i[-1] = i + 1
            u = adj[v][i]

            if ml[u] == v or seen_l[u] == st:
                continue

            seen_l[u] = st
            w = ml[u]

            if w == -1:
                cur_r = v
                cur_u = u
                while True:
                    ml[cur_u] = cur_r
                    mr[cur_r] = cur_u
                    pr = par[cur_r]
                    if pr == -1: return True
                    cur_u = via[cur_r]
                    cur_r = pr

            elif seen_r[w] != st:
                seen_r[w] = st; par[w] = v; via[w] = u; stack_v.append(w); stack_i.append(0)

        return False


def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    if not x or not x[0]:
        return []

    r, c = len(x), len(x[0])
    cells = sorted((x[i][j], i, j) for i in range(r) for j in range(c))
    mv = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))

    lid = [[-1] * c for _ in range(r)]
    rid = [[-1] * c for _ in range(r)]

    kuhn = Kuhn()
    res = [-1] * (r * c)

    added = matching = ptr = 0

    for cost, i, j in cells:
        if (i + j) & 1:
            v = kuhn.add_right()
            rid[i][j] = v
            for di, dj in mv:
                ni, nj = i + di, j + dj
                if 0 <= ni < r and 0 <= nj < c:
                    u = lid[ni][nj]
                    if u != -1:
                        kuhn.add_edge(u, v)
            if kuhn.aug_r(v):
                matching += 1
        else:
            u = kuhn.add_left()
            lid[i][j] = u
            for di, dj in mv:
                ni, nj = i + di, j + dj
                if 0 <= ni < r and 0 <= nj < c:
                    v = rid[ni][nj]
                    if v != -1:
                        kuhn.add_edge(u, v)
            if kuhn.aug_l(u):
                matching += 1

        added += 1
        mis = added - matching
        while ptr < mis:
            res[ptr] = cost
            ptr += 1

    return res

print(immigrants_game((
    (3, 1, 4, 1),
    (5, 9, 2, 6),
)))

