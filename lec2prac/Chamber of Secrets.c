#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INF 1000000000

typedef struct {
    int r, c, d;
} State;

/* Deque implementation */
typedef struct {
    State *data;
    int head, tail, size;
} Deque;

void init_deque(Deque *dq, int cap) {
    dq->data = (State *)malloc(sizeof(State) * cap);
    dq->head = dq->tail = 0;
    dq->size = cap;
}

int empty(Deque *dq) {
    return dq->head == dq->tail;
}

void push_front(Deque *dq, State x) {
    dq->head = (dq->head - 1 + dq->size) % dq->size;
    dq->data[dq->head] = x;
}

void push_back(Deque *dq, State x) {
    dq->data[dq->tail] = x;
    dq->tail = (dq->tail + 1) % dq->size;
}

State pop_front(Deque *dq) {
    State x = dq->data[dq->head];
    dq->head = (dq->head + 1) % dq->size;
    return x;
}

int in_bounds(int r, int c, int n, int m) {
    return r >= 0 && r < n && c >= 0 && c < m;
}

int solution(char **grid, int n, int m) {
    // directions: up, right, down, left
    int dirs[4][2] = {{-1,0},{0,1},{1,0},{0,-1}};

    // dist[r][c][dir]
    int ***dist = (int ***)malloc(n * sizeof(int **));
    for (int i = 0; i < n; i++) {
        dist[i] = (int **)malloc(m * sizeof(int *));
        for (int j = 0; j < m; j++) {
            dist[i][j] = (int *)malloc(4 * sizeof(int));
            for (int d = 0; d < 4; d++)
                dist[i][j][d] = INF;
        }
    }

    Deque dq;
    init_deque(&dq, n * m * 4);

    // start at bottom-right going left (dir = 3)
    dist[n-1][m-1][3] = 0;
    push_back(&dq, (State){n-1, m-1, 3});

    while (!empty(&dq)) {
        State cur = pop_front(&dq);
        int r = cur.r, c = cur.c, d = cur.d;
        int cost = dist[r][c][d];

        // move straight
        int nr = r + dirs[d][0];
        int nc = c + dirs[d][1];
        if (in_bounds(nr, nc, n, m) && cost < dist[nr][nc][d]) {
            dist[nr][nc][d] = cost;
            push_front(&dq, (State){nr, nc, d});
        }

        // reflect at column
        if (grid[r][c] == '#') {
            for (int nd = 0; nd < 4; nd++) {
                if (nd == d) continue;
                int new_cost = cost + 1;
                if (new_cost < dist[r][c][nd]) {
                    dist[r][c][nd] = new_cost;
                    push_back(&dq, (State){r, c, nd});
                }
            }
        }
    }

    // answer: reach row 0 going left
    int ans = INF;
    for (int j = 0; j < m; j++) {
        if (dist[0][j][3] < ans)
            ans = dist[0][j][3];
    }

    return (ans == INF ? -1 : ans);
}

int main() {
    int n, m;
    scanf("%d %d", &n, &m);

    char **grid = (char **)malloc(n * sizeof(char *));
    for (int i = 0; i < n; i++) {
        grid[i] = (char *)malloc(m + 1);
        scanf("%s", grid[i]);
    }

    printf("%d\n", solution(grid, n, m));
    return 0;
}
