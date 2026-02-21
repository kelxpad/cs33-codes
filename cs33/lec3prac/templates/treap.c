#include <stdlib.h>
#include <assert.h>
#include <limits.h>

typedef struct Node {
    int key; // key
    int priority; // heap priority (random)
    struct Node *l, *r; // left and right children
} Node;

// create a new treap node with given key and random priority
Node* new_node(int key) {
    Node* n = malloc(sizeof(Node));
    n->key = key;
    n->priority = rand(); // we might use oj_rand for this, but it will be provided during lab if ever
    n->l = n->r = NULL;
    return n;
}

/*
split(x, v):
- splits treap x into three parts:
    - l: keys < v
    - m: node with key == v or NULL
    - r: keys > v
all returned trees are valid treaps
*/

void split(Node *x, int v, Node** l, Node** m, Node** r) {
    if (x == NULL) {
        *l = *m = *r = NULL;
        return;
    }

    if (v == x->key) {
        *l = x->l;
        *r = x->r;
        *m = x;
        x->l = x->r = NULL; // detach
    }
    else if (v < x->key) {
        // x belongs to r
        split(x->l, v, l, m, &x->l);
        *r = x;
    }
    else {  // v > x->key
        // x belongs to l
        split(x->r, v, &x->r, m, r);
        *l = x;
    }
}

// assumption: all keys in l are < all keys in r
// merges two treaps where all keys in l are < all keys in r
// root is chosen by comparing priorities to preserve the heap property
Node* merge(Node *l, Node *r) {
    // one-child policy
    if (!l) { return r; }
    if (!r) { return l; }

    if (l->priority > r->priority) {
        l->r = merge(l->r, r);
        return l;
    } else {
        r->l = merge(l, r->l);
        return r;
    }
}

// standard bst search
int search(Node *x, int v) {
    if (!x) { return 0; } // not found
    if (v == x->key) { return 1; } // found
    if (v < x->key) { return search(x->l, v); }
    return search(x->r, v); // v > x->key
}

Node* insert(Node* root, int v) {
    // do nothing if v already exists
    if (search(root, v)) { return root; }

    // split treap around v
    Node *l, *m, *r;
    split(root, v, &l, &m, &r);
    
    // insert new node with random priority
    Node* new = new_node(v);
    // merge everything back
    return merge(merge(l, new), r);
}

Node* delete(Node* root, int v) {
    // do nothing if v does not exist
    if (!search(root, v)) { return root; }

    // split to isolate v
    Node *l, *m, *r;
    split(root, v, &l, &m, &r);

    // free the node containing v
    if (m) { free(m); }
    // merge remaining parts
    return merge(l, r);
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

/* CHECKERS */

int is_bst(Node* x, int min, int max) {
    if (!x) { return 1; }
    if (x->key <= min || x->key >= max) { return 0; }
    return is_bst(x->l, min, x->key) && is_bst(x->r, x->key, max);
}
int is_heap(Node* x) {
    if (!x) { return 1; }
    if (x->l && x->l->priority > x->priority) { return 0; }
    if (x->r && x->r->priority > x->priority) { return 0; }
    return is_heap(x->l) && is_heap(x->r);
}

int is_treap(Node* root) {
    return is_bst(root, INT_MIN, INT_MAX) && is_heap(root);
}

int main() {
    Node* root = NULL;

    root = insert(root, 5);
    assert(search(root, 5));
    assert(is_treap(root));

    root = insert(root, 2);
    root = insert(root, 8);
    root = insert(root, 1);
    assert(is_treap(root));

    root = delete(root, 2);
    assert(!search(root, 2));
    assert(is_treap(root));

    Node* nl = next_larger(root, 5);
    assert(nl && nl->key == 8);

    Node* none = next_larger(root, 8);
    assert(none == NULL);

    return 0;
}
