"""
We model the movement of the basilisk's gaze as a shortest-path problem on a graph.
Each state is defined as (r,c,d) where
- (r,c) is a cell in the grid, and
- d is the direction the gaze is currently travelling.

We maintain a 3D array dist[r][c][d], which stores
the minimum number of columns turned magic needed
for the gaze to reach cell (r, c) while moving in
direction d.

The algorithm starts from the basilisk's position
at the bottom-right cell, initially facing left.
From any state,
- Move straight in the current direction with cost 0.
- Reflect at a column by changing direction, cost 1

Since all edge costs are either 0 or 1, we use a
BFS with a deque:
- transitions with cost 0 are pushed to front
- transitions with cost 1 are pushed to back

After the BFS finishes, we take the minimum cost
among all states that reach row 0 while moving left,
which corresponds to the gaze reaching the chamber 
entrance.

If no such state is reachable, the answer is -1.
"""

"""
Let the grid have dimensions n x m.
- Number of states: 4nm, each cell with 4 directions
- Each state is processed at most once with its final distance.
Time Complexity  = O(nm)
Space Complexity = O(nm)
for the distance array and deque.
"""
"""
 
reworded problem statement:
what is the MINIMUM number of columns we can make
magic so that the gaze can reach a column in row 0?
 
idea: if walang column on the first row to go left, 
its impossible to secure
 
problem details:
. if empty
# if regular column
"""
import sys
from collections import deque
 
def solution(grid: list[list[str]]) -> int:
    n, m = len(grid), len(grid[0])
    def in_bounds(i: int, j: int) -> bool:
        return 0 <= i < n and 0 <= j < m
    
    # up right down left
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
 
    # dist[r][c][dir] = minimum cost to reach (r, c) going in direction dir
    dist = [[[float("inf")] * 4 for _ in range(m)] for _ in range(n)]
 
    # step 1: start from (n - 1, m - 1) going left
    dist[n - 1][m - 1][3] = 0
    dq = deque()
    dq.append((n - 1, m - 1, 3))
 
    while dq:
        r, c, d = dq.popleft()
        cost = dist[r][c][d]
 
        # move straight
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc) and cost < dist[nr][nc][d]:
                dist[nr][nc][d] = cost
                dq.appendleft((nr, nc, d)) # 0 cost, appendleft
 
        # reflect at any cell
        if grid[r][c] == "#":
            for nd in range(4):
                if nd == d:
                    continue
                # turning at a column or empty cell costs + 1
                new_cost = cost + 1
                if new_cost < dist[r][c][nd]:
                    dist[r][c][nd] = new_cost
                    dq.append((r, c, nd))
         
    # find minimum cost to reach any column on row 0
    ans = float("inf")
    for j in range(m):
        ans = min(ans, dist[0][j][3])
 
    return -1 if ans == float("inf") else ans
 
def main() -> None:
    input = sys.stdin.readline
 
    n, m = map(int, input().split())
 
    grid = [list(input().strip()) for _ in range(n)]
 
    print(solution(grid))    
 
if __name__ == "__main__":
    main()