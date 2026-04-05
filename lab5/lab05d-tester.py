from lab05d_golfed import immigrants_game
from random import randint, seed

seed(67)

# Precompute knight moves
MV = (
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2),
)


def build_attacks(r: int, c: int) -> list[list[bool]]:
    """attacks[u][v] = True if u attacks v"""
    n = r * c
    attacks = [[False] * n for _ in range(n)]

    for i in range(r):
        for j in range(c):
            u = i * c + j
            for di, dj in MV:
                ni, nj = i + di, j + dj
                if 0 <= ni < r and 0 <= nj < c:
                    v = ni * c + nj
                    attacks[u][v] = True
                    attacks[v][u] = True
    return attacks


def brute_immigrants_game(x):
    """Brute force solution via all subsets"""
    r, c = len(x), len(x[0])
    n = r * c

    attacks = build_attacks(r, c)
    res = [None] * (n + 1)

    for mask in range(1 << n):
        nodes = [i for i in range(n) if (mask >> i) & 1]
        k = len(nodes)

        if k == 0:
            continue

        ok = True
        for i in range(k):
            for j in range(i + 1, k):
                if attacks[nodes[i]][nodes[j]]:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue

        cost = max(x[u // c][u % c] for u in nodes)

        if res[k] is None or cost < res[k]:
            res[k] = cost

    out = []
    for k in range(1, n + 1):
        out.append(res[k] if res[k] is not None else -1)

    return out

# def brute_immigrants_game(x):
#     from collections.abc import Sequence

#     class Kuhn:
#         def __init__(self) -> None:
#             self.adj = []      # left -> right
#             self.radj = []     # right -> left
#             self.match_l = []
#             self.match_r = []
#             self.seen_l = []
#             self.seen_r = []
#             self.stamp = 0

#         def add_left(self) -> int:
#             self.adj.append([])
#             self.match_l.append(-1)
#             self.seen_l.append(0)
#             return len(self.adj) - 1

#         def add_right(self) -> int:
#             self.radj.append([])
#             self.match_r.append(-1)
#             self.seen_r.append(0)
#             return len(self.radj) - 1

#         def add_edge(self, u: int, v: int) -> None:
#             self.adj[u].append(v)
#             self.radj[v].append(u)

#         def aug_l(self, s: int) -> bool:
#             self.stamp += 1
#             st = self.stamp
#             pre = [-1] * len(self.adj)
#             via = [-1] * len(self.adj)

#             self.seen_l[s] = st
#             stack = [(s, 0)]

#             while stack:
#                 u, i = stack[-1]
#                 if i == len(self.adj[u]):
#                     stack.pop()
#                     continue

#                 v = self.adj[u][i]
#                 stack[-1] = (u, i + 1)
#                 w = self.match_r[v]

#                 if w == -1:
#                     while True:
#                         self.match_l[u] = v
#                         self.match_r[v] = u
#                         if pre[u] == -1:
#                             return True
#                         v, u = via[u], pre[u]

#                 elif self.seen_l[w] != st:
#                     self.seen_l[w] = st
#                     pre[w] = u
#                     via[w] = v
#                     stack.append((w, 0))

#             return False

#         def aug_r(self, s: int) -> bool:
#             self.stamp += 1
#             st = self.stamp
#             pre = [-1] * len(self.radj)
#             via = [-1] * len(self.radj)

#             self.seen_r[s] = st
#             stack = [(s, 0)]

#             while stack:
#                 v, i = stack[-1]
#                 if i == len(self.radj[v]):
#                     stack.pop()
#                     continue

#                 u = self.radj[v][i]
#                 stack[-1] = (v, i + 1)
#                 w = self.match_l[u]

#                 if w == -1:
#                     while True:
#                         self.match_l[u] = v
#                         self.match_r[v] = u
#                         if pre[v] == -1:
#                             return True
#                         u, v = via[v], pre[v]

#                 elif self.seen_r[w] != st:
#                     self.seen_r[w] = st
#                     pre[w] = v
#                     via[w] = u
#                     stack.append((w, 0))

#             return False


#     def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
#         if not x or not x[0]:
#             return []

#         r, c = len(x), len(x[0])
#         moves = (
#             (2, 1), (2, -1), (-2, 1), (-2, -1),
#             (1, 2), (1, -2), (-1, 2), (-1, -2),
#         )

#         cells = sorted((x[i][j], i, j) for i in range(r) for j in range(c))

#         k = Kuhn()
#         lid = {}
#         rid = {}

#         ans = [-1] * (r * c)
#         ptr = 0
#         matched = 0

#         for cost, i, j in cells:
#             if (i + j) & 1:
#                 v = k.add_right()
#                 rid[(i, j)] = v
#                 for di, dj in moves:
#                     p = (i + di, j + dj)
#                     if p in lid:
#                         k.add_edge(lid[p], v)
#                 if k.match_r[v] == -1 and k.aug_r(v):
#                     matched += 1
#             else:
#                 u = k.add_left()
#                 lid[(i, j)] = u
#                 for di, dj in moves:
#                     p = (i + di, j + dj)
#                     if p in rid:
#                         k.add_edge(u, rid[p])
#                 if k.match_l[u] == -1 and k.aug_l(u):
#                     matched += 1

#             total = len(k.match_l) + len(k.match_r)
#             best = total - matched  # max independent set size
#             while ptr < best:
#                 ans[ptr] = cost
#                 ptr += 1

#         return ans
    
#     return immigrants_game(x)


# stress test
for test in range(100000):
    def checker():
        r = randint(1, 4)
        c = randint(1, 4)

        x = [[randint(-5, 5) for _ in range(c)] for _ in range(r)]

        fast = immigrants_game(x)
        brute = brute_immigrants_game(x)

        print(f"Case {test}: x={x} fast={fast}, brute={brute}")
        try:
            assert fast == brute
        except AssertionError:
            print("Mismatch! Grid:")
            for row in x:
                print(row)
            print("Fast :", fast)
            print("Brute:", brute)
            return False

        return True

    if not checker():
        break
