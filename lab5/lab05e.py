"""
nangangamoy bipartite
we cant use kuhn's for this problem because hindi one-to-one yung mapping, it would need 5 copies of each to fit the problem
therefore, we can model this as a flow problem, edmonds-karp should do the trick

source -> horse -> race -> jockey -> sink

in rebuilding, detect flow using:
backward edge capacity >= 0: flow was used
"""

from collections import deque
from collections.abc import Sequence
from derby import Participation # pyright: ignore take out later after restarting vsc

inf = 10**18
class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = [] # [to_idx, res_cap, rev_idx]
    
    def add_edge(self, u: int, v: int, cap: int) -> None:
        idx = len(self.edges)
        fwd_idx = idx
        bwd_idx = idx + 1

        self.edges.append([v, cap, bwd_idx])
        self.edges.append([u, 0, fwd_idx]) # no flow yet, nothing to undo

        self.graph[u].append(fwd_idx)
        self.graph[v].append(bwd_idx)

        return fwd_idx

    def bfs(self, s: int, t: int, parent: list[int]) -> int:
        # find augmenting path and return its bottleneck cap else 0
        parent[:] = [-1] * self.n # reset to find fresh augmenting path
        parent[s] = -2
        q = deque([(s, inf)])

        while q:
            u, flow = q.popleft()

            for idx in self.graph[u]:
                v, cap, _ = self.edges[idx]

                # traverse only edges with remaining capacity
                if parent[v] == -1 and cap > 0:
                    parent[v] = idx
                    new_flow = min(flow, cap)
                    
                    if v == t:
                        return new_flow

                    q.append((v, new_flow))
        
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        parent = [-1] * self.n

        while True:
            new_flow = self.bfs(s, t, parent)
            if new_flow == 0:
                break

            flow += new_flow
            v = t

            # walk backward along augmenting path updating residual capacity
            while v != s: # bfs modified parent, we use it
                idx = parent[v]
                rev = self.edges[idx][2]

                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow

                v = self.edges[rev][0]
        
        return flow

def plan_races(m: int, k: int, 
    x: Sequence[frozenset[int]], 
    y: Sequence[frozenset[int]]
    ) -> int | list[list[Participation]]:
    r = len(x) # races
    slots_per_race = 8
    total_slots = r * slots_per_race

    source = 0
    horse_start = 1
    slot_start = horse_start + m
    jockey_start = slot_start + total_slots
    sink = jockey_start + k

    nodes = sink + 1
    ek = EdmondsKarp(nodes)

    # map slot_id to race index
    slot_to_race = [0] * total_slots

    # store edes for reconstruction
    horse_slot_edges = [[] for _ in range(total_slots)]
    slot_jockey_edges = [[] for _ in range(total_slots)]

    # source -> horses
    for horse in range(m):
        ek.add_edge(source, horse_start + horse, 5)

    # build slots
    slot_id = 0
    for race in range(r):
        for _ in range(slots_per_race):
            slot_node = slot_start + slot_id
            slot_to_race[slot_id] = race

            # horse -> slot
            for horse in x[race]:
                idx = ek.add_edge(horse_start + horse, slot_node, 1)
                horse_slot_edges[slot_id].append((horse, idx))

            # slot -> jockey
            for jockey in y[race]:
                idx = ek.add_edge(slot_node, jockey_start + jockey, 1)
                slot_jockey_edges[slot_id].append((jockey, idx))

            slot_id += 1
    
    # jockey -> sink
    for jockey in range(k):
        ek.add_edge(jockey_start + jockey, sink, 5)

    # max flow
    flow = ek.max_flow(source, sink)
    print(flow)

    # reconstruct
    result = [[] for _ in range(r)]

    for slot_id in range(total_slots):
        race = slot_to_race[slot_id]

        chosen_horse = -1
        chosen_jockey = -1

        # find horse used
        for horse, idx in horse_slot_edges[slot_id]:
            rev = ek.edges[idx][2]
            if ek.edges[rev][1] > 0:
                chosen_horse = horse
                break
        
        # find jockey used
        for jockey, idx in slot_jockey_edges[slot_id]:
            rev = ek.edges[idx][2]
            if ek.edges[rev][1] > 0:
                chosen_jockey = jockey
                break
        
        if chosen_horse != -1 and chosen_jockey != -1:
            result[race].append(Participation(horse=chosen_horse, jockey=chosen_jockey))
    
    return result

def check(ans, m, k, x, y):
    horse_cnt = [0] * m
    jockey_cnt = [0] * k

    for i, race in enumerate(ans):
        assert len(race) <= 8

        for p in race:
            h, j = p.horse, p.jockey
            assert h in x[i]
            assert j in y[i]

            horse_cnt[h] += 1
            jockey_cnt[j] += 1
    
    assert all(c <= 5 for c in horse_cnt)
    assert all(c <= 5 for c in jockey_cnt)
    
res1 = plan_races(3, 3, (
    frozenset({0, 1}), 
    frozenset({1, 2}),
), (
    frozenset({0, 1}),
    frozenset({0, 2}),
))

res2 = plan_races(4, 4, (
    frozenset({0, 1}), 
    frozenset({1, 2}),
), (
    frozenset({0, 1}),
    frozenset({0, 2}),
))

check(res1, 3, 3,
    (frozenset({0, 1}), frozenset({1, 2})),
    (frozenset({0, 1}), frozenset({0, 2}))
)
# assert total_participations(res1) == 15

check(res2, 4, 4,
    (frozenset({0, 1}), frozenset({1, 2})),
    (frozenset({0, 1}), frozenset({0, 2}))
)

print("warframe time")