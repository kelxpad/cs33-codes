#ifndef CRUSADE_H
#define CRUSADE_H

#include <stdint.h>

typedef struct route {
    int u;
    int v;
    int64_t t;
} route;

typedef struct crusader crusader;

crusader *c_init(int n, int m, const route *routes);
int64_t min_crusade(crusader *c, int k, const int *s);

#endif
