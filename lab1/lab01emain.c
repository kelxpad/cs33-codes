#include "warehouse.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

void init_oj_rand() {
    srand(time(NULL));
}

int64_t oj_rand() {
    return rand();
}

#define OPS 200000
#define KEY_RANGE 100000
#define VERIFY(b) do {\
    bool _b = (b);\
    fprintf(stderr, "verifying: %s\n", (#b));\
    if (!_b) {\
        fprintf(stderr, "verification failed!\n");\
        exit(1);\
    }\
} while (0)

/* reference model */
typedef struct {
    int64_t key;
    int64_t val;
} ref_entry;

typedef struct {
    ref_entry *a;
    int n;
    int cap;
} ref_wh;

ref_wh *ref_init(void) {
    ref_wh *r = malloc(sizeof(ref_wh));
    r->n = 0;
    r->cap = 16;
    r->a = malloc(sizeof(ref_entry) * r->cap);
    return r;
}

void ref_grow(ref_wh *r) {
    r->cap *= 2;
    r->a = realloc(r->a, sizeof(ref_entry) * r->cap);
}

int ref_find(ref_wh *r, int64_t key) {
    for (int i = 0; i < r->n; i++)
        if (r->a[i].key == key)
            return i;
    return -1;
}

void ref_set(ref_wh *r, int64_t key, int64_t val) {
    int idx = ref_find(r, key);
    if (idx != -1) {
        r->a[idx].val = val;
        return;
    }
    if (r->n == r->cap) ref_grow(r);
    r->a[r->n++] = (ref_entry){ key, val };
}

bool ref_get(ref_wh *r, int64_t key, int64_t *out) {
    int idx = ref_find(r, key);
    if (idx == -1) return false;
    *out = r->a[idx].val;
    return true;
}

void ref_delete(ref_wh *r, int64_t key) {
    int idx = ref_find(r, key);
    if (idx == -1) return;
    r->a[idx] = r->a[--r->n];
}

uint32_t ref_size(ref_wh *r) {
    return r->n;
}

int64_t ref_sum(ref_wh *r, int64_t l, int64_t h) {
    int64_t s = 0;
    for (int i = 0; i < r->n; i++)
        if (r->a[i].key >= l && r->a[i].key <= h)
            s += r->a[i].val;
    return s;
}

/* stress test */
int64_t rand_key(void) {
    return (rand() % (2 * KEY_RANGE)) - KEY_RANGE;
}

int64_t rand_val(void) {
    return (rand() % (2 * KEY_RANGE)) - KEY_RANGE;
}
int main() {
    {
        init_oj_rand();

        warehouse *wh = wh_init();

        VERIFY(wh_size(wh) == 0);

        wh_set(wh, 10, 100);
        wh_set(wh, 20, 200);
        wh_set(wh, 30, 150);
        wh_set(wh, 40, 300);

        VERIFY(wh_size(wh) == 4);
        bool has;
        int64_t ret;
        has = wh_get(wh, 20, &ret);
        VERIFY(has);
        VERIFY(ret == 200);

        VERIFY(wh_sumval(wh, 10, 30) == 450);
        VERIFY(wh_sumval(wh, 20, 40) == 650);
        VERIFY(wh_sumval(wh, 15, 35) == 350);
        wh_set(wh, 20, 250);
        has = wh_get(wh, 20, &ret);
        VERIFY(has);
        VERIFY(ret == 250);
        VERIFY(wh_sumval(wh, 10, 30) == 500);

        wh_delete(wh, 30);
        VERIFY(wh_size(wh) == 3);
        VERIFY(wh_sumval(wh, 10, 40) == 650);

        printf("Jerry's warehouse is well-organized! Test passed!\n");
    }
    {
        init_oj_rand();

        warehouse *wh = wh_init();
        ref_wh *ref = ref_init();

        for (int i = 0; i < OPS; i++) {
            int op = rand() % 4;

            if (op == 0) {
                /* SET */
                int64_t k = rand_key();
                int64_t v = rand_val();
                wh_set(wh, k, v);
                ref_set(ref, k, v);

            } else if (op == 1) {
                /* GET */
                int64_t k = rand_key();
                int64_t v1 = 0, v2 = 0;
                bool b1 = wh_get(wh, k, &v1);
                bool b2 = ref_get(ref, k, &v2);
                VERIFY(b1 == b2);
                if (b1) VERIFY(v1 == v2);

            } else if (op == 2) {
                /* DELETE */
                int64_t k = rand_key();
                wh_delete(wh, k);
                ref_delete(ref, k);

            } else {
                /* SUM */
                int64_t a = rand_key();
                int64_t b = rand_key();
                if (a > b) {
                    int64_t t = a; a = b; b = t;
                }
                int64_t s1 = wh_sumval(wh, a, b);
                int64_t s2 = ref_sum(ref, a, b);
                VERIFY(s1 == s2);
            }

            /* Size invariant */
            VERIFY(wh_size(wh) == ref_size(ref));

            if (i % 20000 == 0)
                fprintf(stderr, "passed %d ops\n", i);
        }

        printf("STRESS TEST PASSED (%d operations)\n", OPS);
        return 0;
    }
}
