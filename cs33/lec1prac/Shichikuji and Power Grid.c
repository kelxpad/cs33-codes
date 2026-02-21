#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>

typedef long long ll;
typedef struct {
    ll x, y; // coordinates
    ll c; // cost to build power station
    ll k; // wire coefficient
} City;

#define MAXN 2005 // problem constraints

City cities[MAXN];

ll dist[MAXN];    // dist[i] = minimum cost to connect city i to the network
int parent[MAXN]; // parent[i] = city used to connect i (0 means power station)
int used[MAXN];   // used[i] = whether city i is already in the MST

// manhattan distance between two cities
ll manhattan(int i, int j) {
    return llabs(cities[i].x - cities[j].x) +
           llabs(cities[i].y - cities[j].y);
}

// prim's algorithm via virtual node (power station)
ll prim_mst(int n) {
    // initialize: connecting city i directly to node 0 costs c[i]
    for (int i = 1; i <= n; i++) {
        dist[i] = cities[i].c;
        parent[i] = 0;
        used[i] = 0; // false
    }

    ll total_cost = 0;

    // add n cities to MST
    for (int step = 1; step <= n; step++) {
        // find unused city with smallest connection cost
        int v = -1;
        ll best = LLONG_MAX;
        for (int i = 1; i <= n; i++) {
            if (!used[i] && dist[i] < best) {
                best = dist[i];
                v = i;
            }
        }

        // include city v in MST
        used[v] = 1; // true
        total_cost += dist[v];

        // update costs for remaining cities
        for (int u = 1; u <= n; u++) {
            if (!used[u]) {
                ll cost = (cities[v].k + cities[u].k) * manhattan(v, u);
                if (cost < dist[u]) {
                    dist[u] = cost;
                    parent[u] = v;
                }
            }
        }
    }
    return total_cost;
}

int main() {
    int n;
    scanf("%d", &n);

    // read coordinates
    for (int i = 1; i <= n; i++) {
        scanf("%lld %lld", &cities[i].x, &cities[i].y);
    }

    // read power station costs
    for (int i = 1; i <= n; i++) {
        scanf("%lld", &cities[i].c);
    }

    // read wire coefficients
    for (int i = 1; i <= n; i++) {
        scanf("%lld", &cities[i].k);
    }

    // run MST
    ll total_cost = prim_mst(n);

    printf("%lld\n", total_cost);

    // separate stations and connections
    int stations[MAXN];
    int station_count = 0;
    int edges[MAXN][2];
    int edge_count = 0;

    for (int i = 1; i <= n; i++) {
        if (parent[i] == 0) { stations[station_count++] = i; } // build power station
        else {
            edges[edge_count][0] = i;
            edges[edge_count][1] = parent[i];
            edge_count++;
        }
    }

    // output power stations
    printf("%d\n", station_count);
    for (int i = 0; i < station_count; i++) {
        printf("%d ", stations[i]);
    }
    printf("\n");

    // output connections
    printf("%d\n", edge_count);
    for (int i = 0; i < edge_count; i++) {
        printf("%d %d\n", edges[i][0], edges[i][1]);
    }

    return 0;
}