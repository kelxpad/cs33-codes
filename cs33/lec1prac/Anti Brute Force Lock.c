/*
author's notes
- detecting that this was an mst problem is not very apparent if not for
the fact that i found this thing on the mst lecnotes
- telltale phrases are: "jumps, wormholes, free movement once unlocked"
- "building connections in any order", "weight matters", etc.
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>

#define MAXN 505 
#define DIGITS 4

typedef struct {
    char code[5]; // 4 digits + null terminator
} Key;

// compute rolling distance between two 4-digit codes
int roll_distance(const char *a, const char *b) {
    int cost = 0;
    for (int i = 0; i < DIGITS; i++) {
        int x = abs(a[i] - b[i]);
        cost += (x < 10 - x) ? x : (10 - x); // get the positive one
    }
    return cost;
}

int prim_mst(Key keys[], int n) {
    int dist[MAXN];
    int used[MAXN];

    for (int i = 0; i < n; i++) {
        dist[i] = INT_MAX;
        used[i] = 0;
    }

    dist[0] = 0; // start from "0000"
    int total = 0;

    for (int i = 0; i < n; i++) {
        int u = -1;
        for (int j = 0; j < n; j++) {
            if (!used[j] && (u == -1 || dist[j] < dist[u])) {
                u = j;
            }
        }

        used[u] = 1;
        total += dist[u];

        for (int v = 0; v < n; v++) {
            if (!used[v]) {
                int w = roll_distance(keys[u].code, keys[v].code);
                if (w < dist[v]) {
                    dist[v] = w;
                }
            }
        }
    }
    return total;
}

int main() {
    int T;
    scanf("%d", &T);

    while (T--) {
        int N;
        scanf("%d", &N);

        Key keys[MAXN];

        // read keys first
        for (int i = 1; i <= N; i++) {
            scanf("%s", keys[i].code);
        }

        // compute minimum start cost from "0000"
        int start = INT_MAX;
        for (int i = 1; i <= N; i++) {
            int d = roll_distance("0000", keys[i].code);
            if (d < start) { start = d; }
        }
    
        // perform MST only among the keys
        int mst = prim_mst(keys + 1, N);
        printf("%d\n", start + mst);
    }
    return 0;
}

/*
SampleInput
4
2 1155 2211
3 1111 1155 5511
3 1234 5678 9090
4 2145 0213 9113 8113
SampleOutput
16
20
26
17
*/