# https://codeforces.com/contest/808/problem/F
"""
authors note: apparently this is wrong?
c = [1, 1, 2]
"""


from collections import deque
import sys
 
inf = 10**18
 
class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = [] # [to_idx, residual cap, reverse_idx]
 
    def add_edge(self, u: int, v: int, cap: int) -> int:
        idx = len(self.edges)
        fwd_idx = idx
        bwd_idx = idx + 1
 
        # forward edge
        self.edges.append([v, cap, bwd_idx])
        # reverse edge with 0 initial cap
        self.edges.append([u, 0, fwd_idx])
 
        self.graph[u].append(fwd_idx)
        self.graph[v].append(bwd_idx)
 
        return fwd_idx
    
    def bfs(self, s: int, t: int, parent: list[int]) -> int:
        # find augmenting path and return its bottleneck capacity,else 0
        parent[:] = [-1] * self.n
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
 
            # walk backward along augmenting path updating residual capacities
            while v != s:
                idx = parent[v]
                rev = self.edges[idx][2]
 
                self.edges[idx][1] -= new_flow
                self.edges[rev][1] += new_flow
 
                v = self.edges[rev][0]
        
        return flow
    
# sieve for primes
maxc = 200000
is_prime = [True] * (maxc + 1)
is_prime[0] = is_prime[1] = False # special case for 0, 1
 
for i in range(2, int(maxc**0.5) + 1):
    if is_prime[i]:
        for j in range(i*i, maxc+1, i):
            is_prime[j] = False
 
def can(cards, k, l):
    valid = [c for c in cards if c[2] <= l]
    if not valid:
        return False
    
    if all(c == 1 for _, c, _ in valid):
        total_power = max(p for p, _, _ in valid)
        return total_power >= k
    
    ones = [c for c in valid if c[1] == 1]
    others = [c for c in valid if c[1] != 1]

    # helper: compute max power from odd-even bipartite min-cut
    def solve_subset(subset):
        m = len(subset)
        if m == 0:
            return 0
        total = sum(p for p, _, _ in subset)

        s = m
        t = m + 1
        ek = EdmondsKarp(m + 2)

        for i, (p, c, _) in enumerate(subset):
            if c % 2 == 1:
                ek.add_edge(s, i, p)
            else:
                ek.add_edge(i, t, p)
        
        for i in range(m):
            for j in range(m):
                if subset[i][1] % 2 == 1 and subset[j][1] % 2 == 0:
                    if is_prime[subset[i][1] + subset[j][1]]:
                        ek.add_edge(i, j, inf)
    
        mincut = ek.max_flow(s, t)
        return total - mincut
    
    # max power without any 1s
    best = solve_subset(others)

    return best >= k

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
 
    cards = [tuple(map(int, input().split())) for _ in range(n)] 
 
    low, high = 1, n
    ans = -1 
 
    while low <= high:
        mid = (low + high) // 2
        if can(cards, k, mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
 
    print(ans)
 
if __name__ == "__main__":
    solve()