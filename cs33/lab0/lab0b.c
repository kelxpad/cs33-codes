#include "marble_game.h"
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

// find the unvisited vertex with the smallest key value
int find_min_vertex(int n, int64_t *key, bool *used) {
    int idx = -1;
    int64_t best = LLONG_MAX;

    for (int i = 0; i < n; i++) {
        if (!used[i] && key[i] < best) {
            best = key[i];
            idx = i;
        }
    }
    return idx;
}

// compute mst via prim's
int64_t prims(int n, int64_t **a) {
    // initialize used and key arrays
    bool used[n]; 
    int64_t key[n];

    for (int i = 0; i < n; i++) {
        used[i] = false;
        key[i] = LLONG_MAX;
    }

    key[0] = 0;

    int64_t total_cost = 0;

    for (int iter = 0; iter < n; iter++) {
        int u = find_min_vertex(n, key, used);

        used[u] = true;
        total_cost += key[u];

        // relax edges from u
        for (int v = 0; v < n; v++) {
            if (!used[v] && a[u][v] < key[v]) {
                key[v] = a[u][v];
            } 
        }
    }

    return total_cost;
}

int64_t min_cost(int n, int64_t **a) {
    return prims(n, a);
}