from collections.abc import Sequence

def build_neighbors(r: int, c: int) -> list[list[int]]:
    def in_bounds(i, j): return 0 <= i < r and 0 <= j < c
    mv = (
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2),
    )
    n = r * c
    neighbors = [[] for _ in range(n)]

    for u in range(n):
        i = u // c
        j = u - i * c
        nu = neighbors[u]
        for di, dj in mv:
            ni = i + di
            nj = j + dj
            if in_bounds(ni, nj):
                nu.append(ni * c + nj)

    return neighbors

def build_partition(n: int, c: int) -> list[bool]:
    return [((u // c) + (u - (u // c) * c)) % 2 == 0 for u in range(n)]

def augment_left(
    start: int,
    neighbors: list[list[int]],
    added: list[bool],
    match: list[int],
    seen_l: list[int],
    par_l: list[int],
    via_l: list[int],
    stamp: int,
) -> bool:
    seen_l[start] = stamp
    par_l[start] = -1

    stack_u = [start]
    stack_i = [0]

    while stack_u:
        u = stack_u[-1]
        i = stack_i[-1]
        nu = neighbors[u]

        if i == len(nu):
            stack_u.pop()
            stack_i.pop()
            continue

        stack_i[-1] = i + 1
        v = nu[i]

        if not added[v] or match[v] == u:
            continue

        w = match[v]
        if w == -1:
            cu, cv = u, v
            while True:
                match[cu] = cv
                match[cv] = cu
                pu = par_l[cu]
                if pu == -1:
                    return True
                cv = via_l[cu]
                cu = pu
        elif seen_l[w] != stamp:
            seen_l[w] = stamp
            par_l[w] = u
            via_l[w] = v
            stack_u.append(w)
            stack_i.append(0)

    return False

def augment_right(
    start: int,
    neighbors: list[list[int]],
    added: list[bool],
    match: list[int],
    seen_r: list[int],
    par_r: list[int],
    via_r: list[int],
    stamp: int,
) -> bool:
    seen_r[start] = stamp
    par_r[start] = -1

    stack_v = [start]
    stack_i = [0]

    while stack_v:
        v = stack_v[-1]
        i = stack_i[-1]
        nv = neighbors[v]

        if i == len(nv):
            stack_v.pop()
            stack_i.pop()
            continue

        stack_i[-1] = i + 1
        u = nv[i]

        if not added[u] or match[u] == v:
            continue

        w = match[u]
        if w == -1:
            cv, cu = v, u
            while True:
                match[cv] = cu
                match[cu] = cv
                pv = par_r[cv]
                if pv == -1:
                    return True
                cu = via_r[cv]
                cv = pv
        elif seen_r[w] != stamp:
            seen_r[w] = stamp
            par_r[w] = v
            via_r[w] = u
            stack_v.append(w)
            stack_i.append(0)

    return False

def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    if not x or not x[0]:
        return []

    r = len(x)
    c = len(x[0])
    n = r * c

    vals = [(x[i][j], i * c + j) for i in range(r) for j in range(c)]
    vals.sort()

    neighbors = build_neighbors(r, c)
    is_left = build_partition(n, c)

    added = [False] * n
    match = [-1] * n

    seen_l = [0] * n
    seen_r = [0] * n
    par_l = [-1] * n
    par_r = [-1] * n
    via_l = [-1] * n
    via_r = [-1] * n
    stamp = 0

    res = [-1] * n
    ptr = 0
    added_cnt = 0
    matching = 0

    for cost, u in vals:
        added[u] = True
        added_cnt += 1

        if match[u] == -1:
            stamp += 1
            if is_left[u]:
                if augment_left(u, neighbors, added, match, seen_l, par_l, via_l, stamp):
                    matching += 1
            else:
                if augment_right(u, neighbors, added, match, seen_r, par_r, via_r, stamp):
                    matching += 1

        mis = added_cnt - matching
        while ptr < mis:
            res[ptr] = cost
            ptr += 1

    return res