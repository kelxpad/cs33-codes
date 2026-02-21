#ifndef WAREHOUSE_H
#define WAREHOUSE_H

#include <stdint.h>
#include <stdbool.h>

// a high-quality random number generator
int64_t oj_rand(void);

// you need to implement these
typedef struct warehouse warehouse;

warehouse *wh_init(void);
void wh_set(warehouse *wh, int64_t shelf, int64_t deliciousness);
bool wh_get(const warehouse *wh, int64_t shelf, int64_t *ret);
void wh_delete(warehouse *wh, int64_t shelf);
uint32_t wh_size(const warehouse *wh);
int64_t wh_sumval(const warehouse *wh, int64_t shelf1, int64_t shelf2);

#endif
