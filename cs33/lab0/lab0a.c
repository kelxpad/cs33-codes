#include "crusade.h"
#include <stdlib.h>
#include <limits.h>

// not using llong_max directly because additions oveflow kaboom
int64_t inf = (LLONG_MAX / 4);

struct crusader {
    int n;
    int64_t *dist; // where dist[i*n + j] = shortest distance from i to j
};

crusader *c_init(int n, int m, const route *routes) {
    crusader *c = malloc(sizeof(crusader));
    c->n = n;
    c->dist = malloc((size_t)n * n * sizeof(int64_t));

    // initialize distance matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            c->dist[i*n + j] = (i == j) ? 0 : inf;
        }
    }

    // insert direct ferry routes
    for (int i = 0; i < m; i++) {
        int u = routes[i].u - 1;
        int v = routes[i].v - 1;
        c->dist[u*n + v] = routes[i].t;
    }

    // first we floyd, then we warshall, floyd-warshall
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            int64_t dik = c->dist[i*n + k];
            if (dik == 0) { continue; } // skip if cant be reached
            for (int j = 0; j < n; j++) {
                int64_t dkj = c->dist[k*n + j];
                if (dkj == inf) { continue; }
                int64_t nd = dik + dkj;
                if (nd < c->dist[i*n + j]) {
                    c->dist[i*n + j] = nd;
                }
            }
        }
    }
    return c;
}

int64_t min_crusade(crusader *c, int k, const int *s) {
    if (k <= 1) { return 0; } // crusade speedrun

    int64_t total = 0;

    for (int i = 0; i + 1 < k; i++) {
        int u = s[i] - 1;
        int v = s[i + 1] - 1;
        int64_t d = c->dist[u * c->n + v];
        if (d == inf) { return -1; } // unreachable
        total += d;
    }
    return total;
}