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
    int64_t neighbor_shelf_sum;
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

split_res *split(shelves *x, int64_t shelf_num){
    split_res * banana_split = malloc(sizeof(split_res));
    if (x == NULL){
        banana_split->left = NULL;
        banana_split->mid = NULL;
        banana_split->right = NULL;
    }
    else if (x->shelf_num == shelf_num){
        banana_split->left = x->l_rack; // Possilby need to recalculate this as well
        banana_split->right = x->r_rack;
        x->l_rack = NULL;
        x->r_rack = NULL;
        x->neighbor_shelf_sum = recalc_neighbor_shelf_sums(x);
        banana_split->mid = x;
    }
    else if (x->shelf_num > shelf_num){
        split_res * temp = split(x->l_rack, shelf_num);
        banana_split->left = temp->left;
        banana_split->mid = temp->mid;
        x->l_rack = temp->right;
        banana_split->right = x;
        free(temp);
    }
    else {
        assert(x->shelf_num < shelf_num);
        split_res * temp = split(x->r_rack, shelf_num);
        banana_split->mid = temp->mid;
        banana_split->right = temp->right;
        x->r_rack = temp->left;
        banana_split->left = x;
        free(temp);
    }
    if (banana_split->left != NULL){
        banana_split->left->neighbor_shelf_sum = recalc_neighbor_shelf_sums(banana_split->left);
    }
    if (banana_split->mid != NULL){
        banana_split->mid->neighbor_shelf_sum = recalc_neighbor_shelf_sums(banana_split->mid);
    }
    if (banana_split->right != NULL){
        banana_split->right->neighbor_shelf_sum = recalc_neighbor_shelf_sums(banana_split->right);
    }
    return banana_split;
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

void wh_set(warehouse *wh, int64_t shelf, int64_t deliciousness){
    split_res *l_m_r = split(wh->root, shelf);
    shelves *m = l_m_r->mid;
    if (m == NULL){
        m = malloc(sizeof(shelves));
        m->chizz_val = deliciousness;
        m->priority = oj_rand();
        m->shelf_num = shelf;
        m->l_rack = NULL;
        m->r_rack = NULL;
        m->neighbor_shelf_sum = deliciousness;
        wh->chizz_count++;
    } else {
        m->chizz_val = deliciousness;
        m->neighbor_shelf_sum = recalc_neighbor_shelf_sums(m);
    }
    wh->root = merge(merge(l_m_r->left, m), l_m_r->right);
    free(l_m_r);
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
void wh_delete(warehouse *wh, int64_t shelf){
    split_res * l_m_r = split(wh->root, shelf);
    shelves *m = l_m_r->mid;
    if (m != NULL ){
        wh->chizz_count--;
        wh->root = merge(merge(l_m_r->left, merge(m->l_rack, m->r_rack)), l_m_r->right);
        free(m);
    } 
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

int64_t wh_sumval(const warehouse *wh, int64_t shelf1, int64_t shelf2)
{ 
    split_res * shelf_fish_1 = split(wh->root, shelf2+1);
    split_res *shelf_fish_2 = split(shelf_fish_1->left, shelf1-1);
    int64_t ret = neighbor_shelf_sums(shelf_fish_2->right);
    shelves *shelf_fless_1 = merge(merge(shelf_fish_2->left, shelf_fish_2->mid), shelf_fish_2->right);
    shelves *shelf_fless_2 = merge(merge(shelf_fless_1, shelf_fish_1->mid), shelf_fish_1->right);
    free(shelf_fish_1);
    free(shelf_fish_2);
    return ret;
}