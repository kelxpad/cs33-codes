# WRITE-UP
"""
The problem can be solved using Dijkstra's algorithm on a state-augmented
graph.

Each traveller can be in one of two states at any vertex:
- state 0: not riding a horse
- state 1: riding a horse

Once a horse is mounted, all remaining edges take half the original time,
and the rider stays in state 1 forever.

To model this, for every vertex v, we maintain two distances:
- dist[v][0]: shortest time to reach v w/o horse
- dist[v][1]: shortest time to reach v w horse

The `dijkstra` function computes these distances from a given start vertex.
Transitions are:
- From (u, 0) to (v, 0) with cost w
- From (u, 0) to (v, 0) with cost w/2 if u has a horse
- From (u, 1) to (v, 1) with cost w/2

We run Dijkstra's twice:
- from vertex 1 (Marian)
- from vertex 2 (Robin)

For each vertex v, the earliest time Marian can arrive is 
min(dist_from_1[v][0], dist_from_1[v][1]), and same goes for Robin.

If they meet a vertex v, the meeting time is the maximum of their arrival
times, since the earlier one may wait. The answer is the minimum such
meeting time over all vertices.

If no vertex is reachable by both, the answer is -1.
"""

"""CORRECTNESS PROOF SKETCH
We prove that the algorithm outputs the earliest possible meeting time.

Lemma 1. For a fixed start vertex, dijkstra correctlhy computes the 
shortest travel time to every state (v, s) where s ∈ {0, 1}.

Proof sketch.
The augmented graph has 2n nodes, one for each (vertex, state) pair, and
all edge weights are non-negative. The transitions exactly model the rules
of movement with and without a horse. Since Dijkstra's algorithm is
correct on graphs with non-negative weights, it computes the shortest path
to every reachable state.

Lemma 2. For any vertex v, the earliest arrival time of a traveller at v
is min(dist[v][0], dist[v][1]). 

Proof sketch.
A traveller may arrive either without a horse or after having mounted one
earlier. These are the only possible states, and dijkstra computes the
optimal time for each. Taking the minimum gives the earliest time.

Lemma 3. If Marian and Robin meet at vertex v, the earliest possible time
there is max(t1, t2), where t1 and t2 are their earliest arrival times at
v.

Proof sketch. 
Both must be present at v simultaneously. If one arrives
earlier, they wait at no cost. Therefore, the meeting time is determined
by the later arrival.

Theorem. The algorithm outputs the earliest possible meeting time over
all vertices, or -1 if no meeting is possible.

Proof sketch.
By Lemmas 1 and 2, the algorithm correctly computes each traveller's 
earliest arrival time at every vertex. By Lemma 3, it computes the earliest
meeting time at each vertex. Taking the minimum over all vertices yields
the earliest feasible meeting overall. If no vertex is reachable by both
travellers, no meeting is possible and the algorithm correctly 
outputs -1.
"""

"""TIME COMPLEXITY ANALYSIS
Let n be the number of vertices and e the number of edges.
- The augmented graph has 2n states and at most 2e transitions.
- Each run of Dijkstra takes O((n + e) log n) time.
- The algorithm runs Dijkstra twice.

Dominated terms in time complexity:
- O(e) # building adjacency matrix
- O(n) # trying all vertices for horse and getting the minimum of the two paths

Time Complexity = O((n + e) log n) 
Space Complexity = O(n + e)
"""
# CODE
import sys
import heapq

def dijkstra(start: int, adj: list[list[tuple[int, int]]], has_horse: list[bool], n: int) -> list[list[int]]:
    """
    dist[v][0] = shortest time to reach v w/o horse
    dist[v][1] = shortest time to reach v w horse
    """
    dist = [[float("inf"), float("inf")] for _ in range(n + 1)]
    pq: list[tuple[int, int, int]] = []

    dist[start][0] = 0
    heapq.heappush(pq, (0, start, 0))

    if has_horse[start]: # consider mounting immediately at start
        dist[start][1] = 0
        heapq.heappush(pq, (0, start, 1))

    while pq:
        cur_dist, u, state = heapq.heappop(pq)
        if cur_dist > dist[u][state]:
            continue

        for v, w in adj[u]:
            if state == 0:
                # continue w/o horse
                if dist[v][0] > cur_dist + w:
                    dist[v][0] = cur_dist + w 
                    heapq.heappush(pq, (dist[v][0], v, 0))
                
                # mount horse if available
                if has_horse[u]:
                    half = w // 2
                    if dist[v][1] > cur_dist + half:
                        dist[v][1] = cur_dist + half
                        heapq.heappush(pq, (dist[v][1], v, 1))
            
            else:
                # already riding horse
                half = w // 2
                if dist[v][1] > cur_dist + half:
                    dist[v][1] = cur_dist + half
                    heapq.heappush(pq, (dist[v][1], v, 1))

    return dist

def solution(n: int, m: int, h: int, horses: list[int], edges: list[tuple[int, int, int]]) -> int:
    # initialize adjacency matrix
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    has_horse = [False] * (n + 1)
    for v in horses:
        has_horse[v] = True
    
    dist_from_1 = dijkstra(1, adj, has_horse, n)
    dist_from_n = dijkstra(n, adj, has_horse, n)

    ans = float("inf")
    for v in range(1, n + 1): # try all vertices
        d1 = min(dist_from_1[v])
        d2 = min(dist_from_n[v])
        if d1 < float("inf") and d2 < float("inf"): # graph is connected
            ans = min(ans, max(d1, d2)) # take max of the two mins
    
    return -1 if ans == float("inf") else ans

def main() -> None:
    input = sys.stdin.readline
    t = int(input())

    out = []
    for _ in range(t):
        n, m, h = map(int, input().split())
        horses = list(map(int, input().split()))

        edges = []
        for _ in range(m):
            u, v, w = map(int, input().split())
            edges.append((u, v, w))
        
        out.append(str(solution(n, m, h, horses, edges)))

    print("\n".join(out))

if __name__ == "__main__":
    main()