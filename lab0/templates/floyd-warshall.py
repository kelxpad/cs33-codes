def floyd_warshall(adj) -> None:
    n = len(adj)
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if adj[i][k] + adj[k][j] < adj[i][j]:
                    adj[i][j] = adj[i][k] + adj[k][j]
    
    # detect negative cycles
    for i in range(n):
        if adj[i][i] < 0:
            raise ValueError("Negative cycle detected!")