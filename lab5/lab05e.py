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
from derby import Participation, RaceTrack 

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
        self.edges.append([u, 0, fwd_idx])

        self.graph[u].append(fwd_idx)
        self.graph[v].append(bwd_idx)

        return fwd_idx

    def bfs(self, s: int, t: int, parent: list[int]) -> int:
        parent[:] = [-1] * self.n
        parent[s] = -2
        q = deque([(s, 10**18)])

        while q:
            u, flow = q.popleft()

            for idx in self.graph[u]:
                v, cap, _ = self.edges[idx]

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

            while v != s:
                idx = parent[v]
                rev = self.edges[idx][2]

                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow

                v = self.edges[rev][0]
        
        return flow


def plan_races(m: int, k: int, 
    tracks: Sequence[RaceTrack]
) -> int | list[list[Participation]]:    

    r = len(tracks)

    source = 0
    horse_start = 1
    race_in_start = horse_start + m
    race_out_start = race_in_start + r
    jockey_start = race_out_start + r
    sink = jockey_start + k

    nodes = sink + 1
    ek = EdmondsKarp(nodes)

    horse_edges = [[[] for _ in range(m)] for _ in range(r)]
    jockey_edges = [[[] for _ in range(k)] for _ in range(r)]

    # source -> horses
    for horse in range(m):
        ek.add_edge(source, horse_start + horse, 5)

    # race_in -> race_out (capacity 8 per race)
    for race in range(r):
        ek.add_edge(race_in_start + race, race_out_start + race, 8)

    # horse -> race_in
    for race in range(r):
        for horse in tracks[race].horses:
            idx = ek.add_edge(horse_start + horse, race_in_start + race, 5)
            horse_edges[race][horse].append(idx)

    # race_out -> jockey
    for race in range(r):
        for jockey in tracks[race].jockeys:
            idx = ek.add_edge(race_out_start + race, jockey_start + jockey, 5)
            jockey_edges[race][jockey].append(idx)

    # jockey -> sink
    for jockey in range(k):
        ek.add_edge(jockey_start + jockey, sink, 5)
    
    flow = ek.max_flow(source, sink)
    # print(flow)
    # reconstruction
    result = [[] for _ in range(r)]

    for race in range(r):
        hs = []
        js = []

        for horse in tracks[race].horses:
            for idx in horse_edges[race][horse]:
                hs.extend([horse] * (5 - ek.edges[idx][1]))

        for jockey in tracks[race].jockeys:
            for idx in jockey_edges[race][jockey]:
                js.extend([jockey] * (5 - ek.edges[idx][1]))

        for horse, jockey in zip(hs, js):
            result[race].append(Participation(horse=horse, jockey=jockey))
    return result

def check(ans, m, k, tracks):
    horse_cnt = [0] * m
    jockey_cnt = [0] * k

    for i, race in enumerate(ans):
        assert len(race) <= 8

        for p in race:
            h, j = p.horse, p.jockey
            assert h in tracks[i].horses
            assert j in tracks[i].jockeys
            horse_cnt[h] += 1
            jockey_cnt[j] += 1
    
    assert all(c <= 5 for c in horse_cnt)
    assert all(c <= 5 for c in jockey_cnt)
    
res1 = plan_races(3, 3, (
    RaceTrack(horses=frozenset({0, 1}), jockeys=frozenset({0, 1})),
    RaceTrack(horses=frozenset({1, 2}), jockeys=frozenset({0, 2})),
))


res2 = plan_races(4, 4, (
    RaceTrack(horses=frozenset({0, 1}), jockeys=frozenset({0, 1})),
    RaceTrack(horses=frozenset({1, 2}), jockeys=frozenset({0, 2})),
))


check(res1, 3, 3, (
    RaceTrack(horses=frozenset({0, 1}), jockeys=frozenset({0, 1})),
    RaceTrack(horses=frozenset({1, 2}), jockeys=frozenset({0, 2})),
))

# assert total_participations(res1) == 15

check(res2, 4, 4, (
    RaceTrack(horses=frozenset({0, 1}), jockeys=frozenset({0, 1})),
    RaceTrack(horses=frozenset({1, 2}), jockeys=frozenset({0, 2})),
))