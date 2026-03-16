"""
ONE-INDEXED PROBLEM
locations = nodes
roads = edges = bidirectional = undirected
max # of uses = capacity
basta cycle siya lmao

given a graph, whats the maximum number of times 
you can come from h, visit exactly one haunted house,
then return to h, if you can only use edges a certain 
amount of times?

idea: h -> network -> haunted_i -> super_sink
each unit of flow reaching a haunted node represents one traversal
from h to that haunted house
an investigation needs two such traversals: one to go, one to return
meaning, we need to pair paths afterwards
"""
from collections.abc import Sequence
from collections import deque

class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph = [[] for _ in range(n + 1)]
    
    def add_edge(self, u: int, v: int, cap: int, directed: bool = True) -> None:
        forward_cap = cap
        backward_cap = cap if not directed else 0
        u_idx = len(self.graph[u]) # index of forward edge in graph[u]
        v_idx = len(self.graph[v]) # index of back edge in graph[v]
        self.graph[u].append([v, v_idx, forward_cap])
        self.graph[v].append([u, u_idx, backward_cap])
    
    def bfs(self, s: int, t: int) -> tuple[list[int], list[int]]:
        # return parent nodes and parent edge indices
        parent_node = [-1] * (self.n + 1)
        parent_edge = [-1] * (self.n + 1)
        parent_node[s] = s
        q = deque([s])
        while q:
            u = q.popleft()
            for i, (v, _, cap) in enumerate(self.graph[u]):
                if parent_node[v] == -1 and cap > 0:
                    parent_node[v] = u
                    parent_edge[v] = i
                    if v == t:
                        return parent_node, parent_edge
                    q.append(v)
        return parent_node, parent_edge
    
    def max_flow_paths(self, s: int, t: int) -> list[list[int]]:
        paths = []
        while True:
            parent_node, parent_edge = self.bfs(s, t)
            if parent_node[t] == -1:
                break

            # augment by 1 unit of flow along path
            v = t
            while v != s:
                u = parent_node[v]
                ei = parent_edge[v]
                if self.graph[u][ei][2] <= 0:
                    break
                self.graph[u][ei][2] -= 1
                rev = self.graph[u][ei][1]
                self.graph[v][rev][2] += 1
                v = u

            # rebuild path from s to t
            path = []
            v = t
            while v != s:
                if v == -1:
                    break
                path.append(v)
                v = parent_node[v]
            path.append(s)
            paths.append(path[::-1])
        
        return paths
    
def max_investigations(
        n: int,
        roads: Sequence[tuple[int, int, int]],
        haunted: Sequence[int],
        h: int,
    ) -> int | list[tuple[int, list[int]]]:

    if not haunted:
        return []
    
    if not (1 <= h <= n):
        return []
    
    inf = 10**9
    m = len(roads)
    base_super = n + 2*m + 1

    def make_base_ek() -> EdmondsKarp:
        ek = EdmondsKarp(base_super)
        for i, (u, v, k) in enumerate(roads):
            ein = n + 2*i + 1
            eout = n + 2*i + 2
            ek.add_edge(u, ein, inf, directed=True)
            ek.add_edge(v, ein, inf, directed=True)
            ek.add_edge(ein, eout, k, directed=True)
            ek.add_edge(eout, u, inf, directed=True)
            ek.add_edge(eout, v, inf, directed=True)
        return ek

    base_ek = make_base_ek()

    def clone_ek_with_size(total_nodes: int) -> EdmondsKarp:
        ek = make_base_ek()
        ek.n = total_nodes

        if len(ek.graph) < total_nodes + 1:
            ek.graph.extend([[] for _ in range(total_nodes + 1 - len(ek.graph))])
        
        return ek
    
    pair_cap = {}
    for t in haunted:
        ek = clone_ek_with_size(base_super)
        ek.add_edge(t, base_super, inf, directed=True)
        raw = ek.max_flow_paths(h, base_super)
        pair_cap[t] = len(raw) // 2

    upper_bounds = sum(pair_cap.values())
    if upper_bounds == 0:
        return []

    def feasible_for_mid(mid: int):
        ts = list(haunted)
        caps = [min(pair_cap[t], mid) for t in ts]
        prefix_max = [0] * (len(ts) + 1)
        for i in range(len(ts)-1, -1, -1):
            prefix_max[i] = prefix_max[i+1] + caps[i]

        stack = [(0, mid, [])] # (i, remaining, assignment)

        while stack:
            i, rem, assign = stack.pop()

            if rem < 0:
                continue

            if i == len(ts):
                if rem == 0:
                    total_slots = sum(assign)
                    final_sink = base_super + total_slots + 1
                    if final_sink < base_super:
                        continue
                    try:
                        ek = clone_ek_with_size(final_sink)
                    except Exception:
                        continue
                    placeholder_idx = base_super + 1
                    if placeholder_idx + total_slots - 1 >= final_sink:
                        continue
                    for idx, t in enumerate(ts):
                        for _ in range(assign[idx]):
                            ek.add_edge(t, placeholder_idx, 2, directed=True)
                            ek.add_edge(placeholder_idx, final_sink, 2, directed=True)
                            placeholder_idx += 1
                    
                    raw = ek.max_flow_paths(h, final_sink)

                    if len(raw) >= 2 * mid:
                        return {ts[idx]: assign[idx] for idx in range(len(ts))}
                continue

            if rem > prefix_max[i]:
                continue

            low_choice = max(0, rem - prefix_max[i + 1])
            high_choice = min(caps[i], rem)

            if low_choice > high_choice:
                continue

            # push in reverse so dfs matches recursion sex
            for take in range(high_choice, low_choice - 1, -1):
                stack.append((i + 1, rem - take, assign + [take]))
        
        return None
    
    low, high = 0, upper_bounds
    best_m = 0
    best_assign = None
    while low <= high:
        mid = (low + high) // 2
        assign = feasible_for_mid(mid)
        if assign is not None:
            best_m = mid
            best_assign = assign
            low = mid + 1
        else:
            high = mid - 1

    if best_m == 0 or best_assign is None:
        return []

    slots_total = sum(best_assign.get(t, 0) for t in haunted)
    final_sink = base_super + slots_total + 1
    ek = clone_ek_with_size(final_sink)
    placeholder_idx = base_super + 1
    placeholder_to_haunted = {}
    for t in haunted:
        count = best_assign.get(t, 0)
        for _ in range(count):
            ek.add_edge(t, placeholder_idx, 2, directed=True)
            ek.add_edge(placeholder_idx, final_sink, 2, directed=True)
            placeholder_to_haunted[placeholder_idx] = t
            placeholder_idx += 1

    raw_paths = ek.max_flow_paths(h, final_sink)

    slot_groups = {}
    for pth in raw_paths:
        if len(pth) < 3:
            continue
        slot = pth[-2]
        p_no_sink = pth[:-1]
        forward = [x for x in p_no_sink if 1 <= x <= n]
        if len(forward) >= 2 and slot in placeholder_to_haunted:
            slot_groups.setdefault(slot, []).append(forward)

    investigations = []
    for slot, ps in slot_groups.items():
        t = placeholder_to_haunted.get(slot)
        if t is None:
            continue
        for i in range(0, len(ps) - 1, 2):
            fwd = ps[i]
            bwd = ps[i + 1]
            cycle = fwd + list(reversed(bwd[:-1]))            
            investigations.append((t, cycle))

    return investigations[:best_m]
    
res1 = max_investigations(
    3,
    [
        (1, 2, 2),
        (2, 3, 2),
    ],
    [3],
    1,
)

exp1 = [(3, [1, 2, 3, 2, 1])]

res2 = max_investigations(
    5,
    [
        (1, 2, 2),
        (2, 5, 2),
        (1, 3, 2),
        (3, 5, 2),
    ],
    [5],
    1,
)

exp2 = [(5, [1, 2, 5, 2, 1]), (5, [1, 3, 5, 3, 1])]

res3 = max_investigations(
    6,
    [
        (1, 2, 4),
        (2, 3, 2),
        (3, 4, 2),
        (2, 5, 2),
        (5, 6, 2),
    ],
    [4, 6],
    1,
)

exp3 = [
    (4, [1, 2, 3, 4, 3, 2, 1]),
    (6, [1, 2, 5, 6, 5, 2, 1]),
]

assert res1 == exp1, f"{res1}"
assert res2 == exp2, f"{res2}"
assert res3 == exp3, f"{res3}"