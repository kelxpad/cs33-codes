from lab05c import max_knights
from random import randint, seed, sample, choice
seed(67)

def brute_max_knights(marked):
    r, c = len(marked), len(marked[0])

    def attacks(a, b):
        ai, aj = a
        bi, bj = b
        return (abs(ai - bi), abs(aj - bj)) in [(2,1),(1,2)]

    # collect all free cells
    cells = [(i, j) for i in range(r) for j in range(c) if not marked[i][j]]
    n = len(cells)

    best = 0

    # try all subsets
    for mask in range(1 << n):
        chosen = []
        ok = True

        for i in range(n):
            if (mask >> i) & 1:
                ci, cj = cells[i]

                # check conflict with already chosen
                for pi, pj in chosen:
                    if attacks((pi, pj), (ci, cj)):
                        ok = False
                        break
                
                if not ok: break

                chosen.append((ci, cj))
        if ok:
            best = max(best, len(chosen))
    return best

def checker(marked, ans):
    r, c = len(marked), len(marked[0])
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    def in_bounds(i, j): return 0 <= i < r and 0 <= j < c

    # normalize answer
    if isinstance(ans, int):
        return ans == brute_max_knights(marked)
    
    # validity checks
    seen = set()
    for (i, j) in ans:
        if not in_bounds(i, j): return False
        if marked[i][j]: return False
        if (i,j) in seen: return False
        seen.add((i, j))

    # no attacks
    for (i, j) in ans:
        for di, dj in moves:
            if (i + di, j + dj) in seen:
                return False
    
    print(brute_max_knights(marked)); print(len(ans))
    return len(ans) == brute_max_knights(marked)

for test in range(100000):
    r = randint(1, 5)
    c = randint(1, 5)
    marked  = [[choice([False, True]) for _ in range(c)] for _ in range(r)]

    res = max_knights(marked)
    print(f"Case {test}: marked={marked}, res={res}")
    assert checker(marked, res), f"Failed on {marked}, got {res}"

print("sex")