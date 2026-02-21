"""
find all strongly-connected components given n and the edge list, 1-indexed
first example:
(1, 2)
second example:
(2,3) (2,4) (2,5)
(3,4) (3,5) (4,5)


fuck me there is something wrong with the way i practice
"""
from collections.abc import Sequence
type Duct = tuple[int, int]
# assumptions: graph[u] contains list of v such that u -> v
# nodes are 0..n-1
def kosaraju_scc(graph: list[list[int]]) -> list[list[int]]:
    n = len(graph)

    # phase 1: DFS on original graph
    visited = [False] * n
    finish_stack = []

    for start in range(n):
        if visited[start]:
            continue
    
    # stack holds (node, next neighbor index)
        stack = [(start, 0)]
        visited[start] = True

        while stack:
            u, idx = stack[-1]

            if idx < len(graph[u]):
                v = graph[u][idx]
                stack[-1] = (u, idx + 1)

                if not visited[v]:
                    visited[v] = True
                    stack.append((v, 0))
            else:
                # all neighbors processed
                stack.pop()
                finish_stack.append(u)

    # phase 2: build reversed graph
    rev_graph = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            rev_graph[v].append(u)

    # phase 3: DFS on reversed graph
    visited = [False] * n
    sccs = []

    while finish_stack:
        start = finish_stack.pop()
        if visited[start]:
            continue

        scc = []
        stack = [start]
        visited[start] = True

        while stack:
            u = stack.pop()
            scc.append(u)

            for v in rev_graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        
        sccs.append(scc)
    
    return sccs

def pointless_chases(n: int, ducts: Sequence[Duct]) -> int:
    # build adjacency list
    graph = [[] for _ in range(n)]
    for u, v in ducts: 
        graph[u - 1].append(v - 1)
    
    sccs = kosaraju_scc(graph)

    ans = 0
    for scc in sccs:
        k = len(scc)
        if k >= 2:
            ans += k * (k - 1) // 2 # count unordered pairs 
        
    return ans

res1 = pointless_chases(4, [ 
    (1, 2), 
    (2, 1),
    (1, 3),
    (2, 3),
    (2, 4),
    (3, 4),
])

exp1 = 1

res2 = pointless_chases(6, [
    (1, 2), 
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 2),
])

exp2 = 6

assert res1 == exp1, f"got {res1}"
assert res2 == exp2, f"got {res2}"