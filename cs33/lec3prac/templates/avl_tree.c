#include <stdlib.h>
#include <assert.h>
#include <limits.h>

typedef struct Node {
    int key;
    int height;
    struct Node *l, *r;
} Node;

// height helper
int height(Node* x) {
    return x ? x->height : -1;
}

int max(int a, int b) {
    return a > b ? a : b;
}

void reset_height(Node* x) {
    x->height = max(height(x->l), height(x->r)) + 1;
}

// actual avl tree code
Node* new_node(int key) {
    Node* n = malloc(sizeof(Node));
    n->key = key;
    n->height = 0; // leaf
    n->l = n->r = NULL;
    return n;
}

/*
    x               y
     \             / \
      y    --->   x   c
     / \           \
    b   c           b
*/
Node* left_rotate(Node* x) {
    Node* y = x->r;
    Node* b = y->l;

    y->l = x;
    x->r = b;
    
    reset_height(x);
    reset_height(y);

    return y;
}

/*
        x           y
       /           / \
      y    --->   a   x
     / \             /
    a   b           b
*/
Node* right_rotate(Node* x) {
    Node* y = x->l;
    Node* b = y->r;

    y->r = x;
    x->l = b;

    reset_height(x);
    reset_height(y);

    return y;
}

// rebalance only when height difference is 2
Node* rebalance(Node* x) {
    if (!x) { return x; }

    reset_height(x);

    // left heavy
    if (height(x->l) >= height(x->r) + 2) {
        if (height(x->l->r) > height(x->l->l)) {
            x->l = left_rotate(x->l); // LR case
        }
        return right_rotate(x);       // LL case
    }

    // right heavy
    if (height(x->r) >= height(x->l) + 2) {
        if (height(x->r->l) > height(x->r->r)) {
            x->r = right_rotate(x->r); // RL case
        }
        return left_rotate(x);         // RR case
    }

    return x;
}

int search(Node *x, int v) {
    if (!x) { return 0; }
    if (v == x->key) { return 1; }
    if (v < x->key) { return search(x->l, v); }
    return search(x->r, v);
}

// usual bst insert + rebalance on the way up
Node* insert(Node* x, int v) {
    if (!x) { return new_node(v); }

    if (v < x->key) {
        x->l = insert(x->l, v);
    } else if (v > x->key) {
        x->r = insert(x->r, v);
    } else {
        return x; // do nothing if duplicate
    }

    return rebalance(x);
}

Node* delete_leftmost(Node* x, int* min_key) {
    if (x->l == NULL) {
        *min_key = x->key;
        Node* r = x->r;
        free(x);
        return r;
    }

    x->l = delete_leftmost(x->l, min_key);
    return rebalance(x);
}

Node* delete(Node* x, int v) {
    if (!x) { return NULL; }

    if (v < x->key) {
        x->l = delete(x->l, v);
    }
    else if (v > x->key) {
        x->r = delete(x->r, v);
    }
    else {
        // found node to delete
        if (!x->r) {
            Node* l = x->l;
            free(x);
            return l;
        } else {
            int succ;
            x->r = delete_leftmost(x->r, &succ);
            x->key = succ;
        }
    }
    return rebalance(x);
}

Node* next_larger(Node* root, int v) {
    Node* curr = root;
    Node* ans = NULL; // best candidate so far

    while (curr != NULL) {
        if (curr->key > v) {
            ans = curr; // possible answer
            curr = curr->l; // try to find a smaller one
        } else {
            curr = curr->r; // must go right
        }
    }

    return ans; // may be NULL
}

/* INVARIANT TESTERS */

int is_bst(Node* x, int min, int max) {
    if (!x) return 1;
    if (x->key <= min || x->key >= max) return 0;
    return is_bst(x->l, min, x->key) &&
           is_bst(x->r, x->key, max);
}

int is_avl(Node* x) {
    if (!x) return 1;

    int hl = height(x->l);
    int hr = height(x->r);

    if (abs(hl - hr) > 1) return 0;
    if (x->height != max(hl, hr) + 1) return 0;

    return is_avl(x->l) && is_avl(x->r);
}

int is_valid_avl(Node* root) {
    return is_bst(root, INT_MIN, INT_MAX) && is_avl(root);
}


int main() {
    Node* root = NULL;

    root = insert(root, 5);
    root = insert(root, 2);
    root = insert(root, 8);
    root = insert(root, 1);

    root = delete(root, 2);

    Node* nl = next_larger(root, 5);
    assert(nl && nl->key == 8);
    {
        root = insert(root, 5);
        assert(is_valid_avl(root));

        root = insert(root, 2);
        assert(is_valid_avl(root));

        root = insert(root, 8);
        assert(is_valid_avl(root));

        root = insert(root, 1);
        assert(is_valid_avl(root));

        root = delete(root, 2);
        assert(is_valid_avl(root));
    }
    { // LL case
        Node* root = NULL;
        root = insert(root, 3);
        root = insert(root, 2);
        root = insert(root, 1);
        assert(is_valid_avl(root));
        assert(root->key == 2);
    }
    { // stress test
        Node* root = NULL;
        srand(1);

        for (int i = 0; i < 10000; i++) {
            int v = rand() % 5000;
            root = insert(root, v);
            assert(is_valid_avl(root));
        }

        for (int i = 0; i < 5000; i++) {
            int v = rand() % 5000;
            root = delete(root, v);
            assert(is_valid_avl(root));
        }
    }
    return 0;
}
