from itertools import permutations
from collections import defaultdict
from collections.abc import Sequence

def brute_investigations(
    n: int,
    roads: Sequence[tuple[int, int, int]],
    haunted: Sequence[int],
    h: int,
) -> int | list[tuple[int, list[int]]]:

    adj = defaultdict(list)
    capacities = {}
    for i, (u, v, k) in enumerate(roads):
        adj[u].append((v, i))
        adj[v].append((u, i))
        capacities[i] = k

    def find_round_trips(target):
        results = []
        def dfs(node, path, visited_nodes, edge_counts):
            if node == target:
                full_path = path + list(reversed(path[:-1]))
                round_trip_counts = {eid: cnt * 2 for eid, cnt in edge_counts.items()}
                results.append((target, full_path, round_trip_counts))
                return
            for neighbor, eid in adj[node]:
                if neighbor not in visited_nodes and edge_counts.get(eid, 0) < capacities[eid]:
                    visited_nodes.add(neighbor)
                    edge_counts[eid] = edge_counts.get(eid, 0) + 1
                    path.append(neighbor)
                    dfs(neighbor, path, visited_nodes, edge_counts)
                    path.pop()
                    edge_counts[eid] -= 1
                    if edge_counts[eid] == 0:
                        del edge_counts[eid]
                    visited_nodes.discard(neighbor)

        dfs(h, [h], {h}, {})
        return results

    all_round_trips = []
    for house in haunted:
        all_round_trips.extend(find_round_trips(house))

    if not all_round_trips:
        return []

    best = []

    def can_add(used, edge_counts):
        for eid, cnt in edge_counts.items():
            if used.get(eid, 0) + cnt > capacities[eid]:
                return False
        return True

    def try_combinations(idx, current_trips, used_edges):
        nonlocal best
        if len(current_trips) > len(best):
            best = list(current_trips)

        for i in range(idx, len(all_round_trips)):
            trip = all_round_trips[i]
            _, _, edge_counts = trip
            if can_add(used_edges, edge_counts):
                for eid, cnt in edge_counts.items():
                    used_edges[eid] = used_edges.get(eid, 0) + cnt
                current_trips.append(trip)
                try_combinations(i, current_trips, used_edges)
                current_trips.pop()
                for eid, cnt in edge_counts.items():
                    used_edges[eid] -= cnt
                    if used_edges[eid] == 0:
                        del used_edges[eid]

    try_combinations(0, [], {})

    if not best:
        return 0

    return [(house, path) for house, path, _ in best][::-1]

res1 = brute_investigations(
    3,
    [
        (1, 2, 2),
        (2, 3, 2),
    ],
    [3],
    1,
)

exp1 = [(3, [1, 2, 3, 2, 1])]

res2 = brute_investigations(
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

res3 = brute_investigations(
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