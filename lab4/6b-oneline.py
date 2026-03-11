"""
S = source
D = sink
. = nodes
# = no node
"""

from collections import deque

def edmonds_karp():
    ...

def place_traps(alleyways: str) -> str:
    def in_range(i: int, j: int) -> bool:
        return 0 <= i < r and 0 <= j < c
    
    grid = alleyways.splitlines()
    grid = [list(row) for row in grid]
    r = len(grid)
    c = len(grid[0])
    q: deque[tuple[int, int]] = deque([])
    parent = {}
    visited = set()

    for i in range(r):
        for j in range(c):
            if grid[i][j] == "S":
                q.append((i, j))
                visited.add((i, j))
                break
        if q:
            break

    dest = None

    while q:
        x, y = q.popleft()

        if grid[x][y] == "D":
            dest = (x, y)
            break

        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for nx, ny in neighbors:
            ux, uy = x + nx, y + ny
            if in_range(ux, uy) and grid[ux][uy] != "#" and (ux, uy) not in visited:
                visited.add((ux, uy))
                parent[(ux, uy)] = (x, y)
                q.append((ux, uy))
        
    if dest is None: 
        return alleyways
    
    # path reconstruction
    path = []
    cur = dest
    while cur in parent:
        path.append(cur)
        cur = parent[cur]
    path.append(cur)
    path.reverse()

    for x, y in path:
        if grid[x][y] == ".":
            grid[x][y] = "X"
            break

    return "\n".join("".join(row) for row in grid)
    
    

    # if it is impossible to reach D from S, then no traps need to be placed