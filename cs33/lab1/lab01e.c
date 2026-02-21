# include "warehouse.h"
# include <stdlib.h>
# include <assert.h>

typedef struct shelves shelves;
struct shelves{
    int64_t shelf_num;
    int64_t chizz_val;
    int64_t priority;
    shelves *l_rack;
    shelves *r_rack;
    int64_t neighbor_shelf_sum; // cache subtree sum for fast range queries
};

struct warehouse {
        shelves *root;
        uint32_t chizz_count;
    };
typedef struct split_res split_res;
struct split_res{
    shelves * left;
    shelves * mid;
    shelves * right;
};
/*
split treaps by two trees:
L: keys < k
R: keys >= k
equality is handled via comparisons
*/
int64_t neighbor_shelf_sums(shelves *x){
    if (x == NULL){
        return 0;
    }
    return x->neighbor_shelf_sum;
}

int64_t recalc_neighbor_shelf_sums(shelves* x){
    return neighbor_shelf_sums(x->l_rack) + neighbor_shelf_sums(x->r_rack) + x->chizz_val;
}


warehouse *wh_init(void){
    warehouse * ret_wh = malloc(sizeof(warehouse));
    ret_wh->root = NULL;
    ret_wh->chizz_count = 0;
    return ret_wh;
}
/*
to preserve bst, heap and correct subtree sums invariants

split(x, k, $l, $r)
- l contains all nodes with shelf_num < k
- r contains all nodes withs shelf_num >= k
*/
void split(shelves *x, int64_t k, shelves **l, shelves **r)
{
    if (!x) {
        *l = NULL;
        *r = NULL;
        return;
    }

    if (x->shelf_num < k) {
        // x belongs to l
        split(x->r_rack, k, &x->r_rack, r);
        x->neighbor_shelf_sum = recalc_neighbor_shelf_sums(x);
        *l = x;
    } else {
        // x belongs to r (includes equality)
        split(x->l_rack, k, l, &x->l_rack);
        x->neighbor_shelf_sum = recalc_neighbor_shelf_sums(x);
        *r = x;
    }
}

// Priority matters here
shelves *merge(shelves *left, shelves *right){
    if (left == NULL){
        return right;   // Maybe NULL
    }
    if (right == NULL){
        return left;  // Sure that it isn't NULL
    }
    if (left->priority > right->priority){
        // Make right a child of left
        left->r_rack = merge(left->r_rack, right);
        left->neighbor_shelf_sum = recalc_neighbor_shelf_sums(left);
        return left;
    } else {
        right->l_rack = merge(left, right->l_rack);
        right->neighbor_shelf_sum = recalc_neighbor_shelf_sums(right);
        return right;
    }
}
/*
wh_set now uses TWO splits instead of using mid case
*/
void wh_set(warehouse *wh, int64_t shelf, int64_t deliciousness)
{
    shelves *a, *b, *c;

    // a: < shelf, b: >= shelf
    split(wh->root, shelf, &a, &b);

    // B1: == shelf, c: > shelf
    split(b, shelf + 1, &b, &c);

    if (b) {
        // update existing
        b->chizz_val = deliciousness;
        b->neighbor_shelf_sum = recalc_neighbor_shelf_sums(b);
    } else {
        // insert new
        b = malloc(sizeof(shelves));
        b->shelf_num = shelf;
        b->chizz_val = deliciousness;
        b->priority = oj_rand();
        b->l_rack = b->r_rack = NULL;
        b->neighbor_shelf_sum = deliciousness;
        wh->chizz_count++;
    }

    wh->root = merge(merge(a, b), c);
}

bool _wh_get(const shelves *x, int64_t shelf, int64_t *ret){
    if (x == NULL){
        return false;
    }
    else if (x->shelf_num == shelf){
        *ret = x->chizz_val;
        return true;
}
    else if (x->shelf_num > shelf){
        return _wh_get(x->l_rack, shelf, ret);
    }
    else {
        assert(x->shelf_num < shelf);
        return _wh_get(x->r_rack, shelf, ret);
    }
}
bool wh_get(const warehouse *wh, int64_t shelf, int64_t *ret){
    return _wh_get(wh->root, shelf, ret);
}

/*
deletion also now uses two-split pattern to isolate node, 
for correctness under randomized prios
 */
void wh_delete(warehouse *wh, int64_t shelf)
{
    shelves *a, *b, *c;

    split(wh->root, shelf, &a, &b);
    split(b, shelf + 1, &b, &c);

    if (b) {
        wh->chizz_count--;
        free(b);
    }

    wh->root = merge(a, c);
}

uint32_t wh_size(const warehouse *wh){
    return wh->chizz_count;
}

int64_t get_sum(shelves *x){
    if (x == NULL){
        return 0;
    }

    return x->chizz_val + get_sum(x->l_rack) + get_sum(x->r_rack);
}
/*
uses subtree sums via split + merge for O(log n) expected time
instead of O(n) recursive traversal
*/
int64_t wh_sumval(const warehouse *wh_, int64_t l, int64_t r)
{
    warehouse *wh = (warehouse *)wh_;

    shelves *a, *b, *c;

    split(wh->root, l, &a, &b);
    split(b, r + 1, &b, &c);

    int64_t ans = neighbor_shelf_sums(b);

    wh->root = merge(a, merge(b, c));
    return ans;
}