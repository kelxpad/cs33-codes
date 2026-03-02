#include "calc.h"
#include <stdlib.h>
#include <assert.h>
#define MOD 1000000000LL

typedef struct node node;
typedef struct calc calc;
typedef struct dyarr dyarr;

struct node {
    int64_t val;
    struct node *next;
};


struct dyarr {
    calc** arr;
    int s, c;
};

struct calc {
    node *top; // persistent stack
    int depth; // len of anc is relative to depth
    dyarr* anc; 
};

dyarr* dyarr_init(void) {
    dyarr* dy = malloc(sizeof(dyarr));
    dy->arr = malloc(sizeof(calc*));
    dy->s = 0, dy->c = 1;
    return dy;
}


void insert(dyarr* dy, calc* s) {
    if (dy->s == dy->c) {
        int new_cap = 2*dy->c;
        calc** copy = malloc(sizeof(calc*)*new_cap);
        for (int i = 0; i < dy->s; i++) {
            copy[i] = dy->arr[i];
        }
        free(dy->arr);
        dy->arr = copy;
        dy->c = new_cap;
    }

    dy->arr[dy->s++] = s;
}

void get_anc(calc* c) {
    int n = 1;
    // This should not index error by virture of depth based pre-comp
    while ((1 << n) <= c->depth) {
        calc* anc = (c->anc->arr[n-1])->anc->arr[n-1];
        assert (anc != NULL);
        insert(c->anc, anc);
        n++;
    }
}

calc *calc_init(void) {
    calc *c = malloc(sizeof(calc));
    c->top = NULL;
    c->depth = 0;
    c->anc = NULL; 
    return c;
}

calc *calc_push(calc *s, int64_t x) {
    calc *c = malloc(sizeof(calc));

    node *n = malloc(sizeof(node));
    n->val = x;
    n->next = s->top;

    c->top = n;
    c->anc = dyarr_init();
    c->depth = s->depth + 1;
    insert(c->anc, s);
    get_anc(c);
    return c;
}

calc *calc_apply(calc *s, char op) {
    calc *c = malloc(sizeof(calc));

    node *a = s->top;
    node *b = a->next;

    int64_t x = b->val;
    int64_t y = a->val;
    int64_t result;

    if (op == '+') {
        result = (x + y) % MOD;
    }
    else if (op == '-') {
        result = (x - y + MOD) % MOD;
    }
    else { // '*' 
        result = (x * y) % MOD;
    }

    node *n = malloc(sizeof(node));
    n->val = result;
    n->next = b->next;

    c->top = n;
    c->anc = dyarr_init();
    c->depth = s->depth + 1;
    insert(c->anc, s);
    get_anc(c);
    return c;
}

//MOST LIKELY GOING TO BE THE BOTTLENECK
calc *calc_undo(calc *s, int k) {
    calc *cur = s;
    int target = k <= cur->depth ? cur->depth - k:0;
    
    if (!cur->anc) {
        return cur;
    }

    for (int i = cur->anc->s - 1; i >= 0; i--) {
        if (!cur->anc) {
            break;
        }
        if (i >= cur->anc->s) {
            continue;
        }

        if (cur->anc->arr[i]->depth < target) {
            continue;
        }

        cur = cur->anc->arr[i];
    }
    return cur;
}

int64_t calc_peek(calc *s) {
    return s->top->val;

}
