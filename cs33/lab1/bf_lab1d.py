from collections.abc import Sequence
type Gate = tuple[int, int]

def bf_territory_shifts(n: int, gates: Sequence[Gate]) -> int:
    # build graph, 0-indexed
    adj = [[] for _ in range(n)]
    for u, v in gates:
        adj[u - 1].append(v - 1)

    # tarjan scc
    index = 0
    stack = []
    on_stack = [False] * n
    ids = [-1] * n
    low = [0] * n
    scc_id = [-1] * n
    scc_count = 0

    def dfs(u):
        nonlocal index, scc_count
        ids[u] = low[u] = index
        index += 1
        stack.append(u)
        on_stack[u] = True

        for v in adj[u]:
            if ids[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], ids[v])

        if ids[u] == low[u]:
            while True:
                x = stack.pop()
                on_stack[x] = False
                scc_id[x] = scc_count
                if x == u:
                    break
            scc_count += 1

    for i in range(n):
        if ids[i] == -1:
            dfs(i)

    # count pairs from different SCs
    ans = 0
    for u in range(n):
        for v in range(u + 1, n):
            if scc_id[u] != scc_id[v]:
                ans += 1
    
    return ans