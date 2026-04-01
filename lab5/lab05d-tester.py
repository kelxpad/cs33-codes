from lab05d_fucking_end_my_suffering import immigrants_game
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
