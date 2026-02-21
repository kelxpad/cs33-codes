#include "jvl.h"
#include "art_lab0b.c"
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define VERIFY(b) do {\
    bool _b = (b);\
    fprintf(stderr, "verifying: %s\n", (#b));\
    if (!_b) {\
        fprintf(stderr, "verification failed!\n");\
        exit(1);\
    }\
} while (0)

jvl_tree *jvl_init() {
    jvl_tree *tree = (jvl_tree*)malloc(sizeof(jvl_tree));
    tree->size = 0;
    tree->root = NULL;
    return tree;
}

/* INVARIANT TESTERS */

int is_bst_inorder_rec(jvl_node* x, int64_t *prev, int *first) {
    // base case: empty subtree is invalid
    if (!x) { return 1; }
    // traverse left subtree
    if (!is_bst_inorder_rec(x->left, prev, first)) { return 0; }

    // visit current node
    if (*first) {
        // very first node, initialize prev and first
        *prev = x->tastiness;
        *first = 0;
    } else {
        // check non-decreasing order
        if (*prev > x->tastiness) { // if strictly decreasing, then illegal
            { return 0; }
        }
        *prev = x->tastiness;
    }
    // traverse right subtree
    return is_bst_inorder_rec(x->right, prev, first);
}

int is_bst_inorder(jvl_node* root) {
    int first = 1;
    int64_t prev = 0;
    return is_bst_inorder_rec(root, &prev, &first);
}

int is_size_correct(jvl_node* x) {
    if (!x) { return 1; }

    int expected =
        1 +
        (x->left ? x->left->size : 0) +
        (x->right ? x->right->size : 0);

    if (x->size != expected) { return 0; }

    return is_size_correct(x->left) &&
           is_size_correct(x->right);
}



int is_avl_jvl(jvl_node* x) {
    if (!x) return 1;

    int hl = x->left ? x->left->height : -1;
    int hr = x->right ? x->right->height : -1;

    if (abs(hl - hr) > 1) { return 0; }
    if (x->height != (hl > hr ? hl : hr) + 1) { return 0; }

    return is_avl_jvl(x->left) &&
           is_avl_jvl(x->right);
}

int main() {
    {
        jvl_tree *vault = jvl_init();

        VERIFY(jvl_size(vault) == 0);
        VERIFY(!jvl_search(vault, 30));
        VERIFY(!jvl_search(vault, 100));

        jvl_insert(vault, 50);
        jvl_insert(vault, 25);
        jvl_insert(vault, 75);
        jvl_insert(vault, 10);
        jvl_insert(vault, 30);
        jvl_insert(vault, 60);
        jvl_insert(vault, 80);

        VERIFY(jvl_size(vault) == 7);
        VERIFY(jvl_search(vault, 30));
        VERIFY(!jvl_search(vault, 100));
        VERIFY(jvl_search(vault, 10));
        VERIFY(jvl_get_min(vault) == 10);
        VERIFY(jvl_get_max(vault) == 80);

        jvl_insert(vault, 10);
        VERIFY(jvl_size(vault) == 8);

        // Right->left heavy
        jvl_tree *vault_2 = jvl_init();
        jvl_insert(vault_2, 50);
        jvl_insert(vault_2, 25);
        jvl_insert(vault_2, 10);
        assert(vault_2->root->tastiness == 25);
        assert(vault_2->root->right->tastiness == 50);
        jvl_insert(vault_2, 63);
        jvl_insert(vault_2, 75);
        jvl_insert(vault_2, 49);
        jvl_insert(vault_2, 48);
        //  WITH REBALANCE
        //        25
        //        / \
        //       10  63
        //      /\   / \
        //          50  75
        //          /
        //         49
        VERIFY(jvl_search(vault_2, 49));
        VERIFY(jvl_size(vault_2) == 7);
        VERIFY(jvl_get_max(vault_2) == 75);
        VERIFY(jvl_get_min(vault_2) == 10);
        VERIFY(vault_2->root->tastiness == 50);
        VERIFY(vault_2->root->left->tastiness == 25);

        VERIFY(vault_2->root->left->left->tastiness == 10);
        VERIFY(vault_2->root->left->left->left == NULL);
        VERIFY(vault_2->root->left->left->right == NULL);

        VERIFY(vault_2->root->left->right->tastiness == 49);
        VERIFY(vault_2->root->left->right->right == NULL);
        VERIFY(vault_2->root->left->right->left->tastiness == 48);
        VERIFY(vault_2->root->left->right->left->left == NULL);
        VERIFY(vault_2->root->left->right->left->right == NULL);

        VERIFY(vault_2->root->right->tastiness == 63);
        VERIFY(vault_2->root->right->left == NULL);
        VERIFY(vault_2->root->right->right->tastiness == 75);
        VERIFY(vault_2->root->right->right->right == NULL);
        VERIFY(vault_2->root->right->right->left == NULL);

        
        
        
        // Right-Right heavy
        jvl_tree *vault_3 = jvl_init();
        jvl_insert(vault_3, 25);
        jvl_insert(vault_3, 50);
        jvl_insert(vault_3, 75);

        VERIFY(jvl_size(vault_3) == 3);
        VERIFY(jvl_get_max(vault_3) == 75);
        VERIFY(jvl_get_min(vault_3) == 25);
        VERIFY(jvl_search(vault_3, 50));
        VERIFY(jvl_search(vault_3, 75));
        VERIFY(jvl_search(vault_3, 25));
        VERIFY(!jvl_search(vault_3, 100));
        VERIFY(!jvl_search(vault_3, 69));
        VERIFY(!jvl_search(vault_3, 67));
        VERIFY(vault_3->root->tastiness == 50);
        VERIFY(vault_3->root->left->tastiness == 25);
        VERIFY(vault_3->root->left->right == NULL);
        VERIFY(vault_3->root->left->left == NULL);
        VERIFY(vault_3->root->right->tastiness == 75);
        VERIFY(vault_3->root->right->right == NULL);
        VERIFY(vault_3->root->right->left == NULL);

        jvl_tree *vault_4 = jvl_init();
        jvl_insert(vault_4, 50);
        jvl_insert(vault_4, 25);
        jvl_insert(vault_4, 75);
        jvl_insert(vault_4, 63);
        jvl_insert(vault_4, 82);
        jvl_insert(vault_4, 91);
        VERIFY(jvl_size(vault_4) == 6);
        VERIFY(jvl_get_max(vault_4) == 91);
        VERIFY(jvl_get_min(vault_4) == 25);
        VERIFY(jvl_search(vault_4, 50));
        VERIFY(jvl_search(vault_4, 25));
        VERIFY(jvl_search(vault_4, 75));
        VERIFY(jvl_search(vault_4, 63));
        VERIFY(jvl_search(vault_4, 82));
        VERIFY(jvl_search(vault_4, 91));
        VERIFY(!jvl_search(vault_4, 67));
        VERIFY(!jvl_search(vault_4, 69));
        VERIFY(vault_4->root->tastiness == 75);
        VERIFY(vault_4->root->left->tastiness == 50);

        VERIFY(vault_4->root->left->left->tastiness == 25);
        VERIFY(vault_4->root->left->left->left == NULL);
        VERIFY(vault_4->root->left->left->right == NULL);

        VERIFY(vault_4->root->left->right->tastiness == 63);
        VERIFY(vault_4->root->left->right->right == NULL);
        VERIFY(vault_4->root->left->right->left == NULL);

        VERIFY(vault_4->root->right->tastiness == 82);
        VERIFY(vault_4->root->right->left == NULL);
        VERIFY(vault_4->root->right->right->tastiness == 91);
        VERIFY(vault_4->root->right->right->left == NULL);
        VERIFY(vault_4->root->right->right->right == NULL);

        // Left-Right heavy
        jvl_tree* vault_5 = jvl_init();
        jvl_insert(vault_5, 16);

        // Left-Left heavy

        // With duplicates

        // With negative numbers

        // Only the root exist
        jvl_tree* vault_k = jvl_init();
        jvl_insert(vault_k, 67);
        VERIFY(jvl_size(vault_k) == 1);
        VERIFY(jvl_get_max(vault_k) == 67);
        VERIFY(jvl_get_min(vault_k) == 67);
        VERIFY(jvl_search(vault_k, 67));
        VERIFY(!jvl_search(vault_k, -76));

        
        printf("Jerry's cheese vault is secure!\n");
    }
    { // get kth after testing
        jvl_tree *t = jvl_init();

        jvl_insert(t, 10);
        jvl_insert(t, 20);
        jvl_insert(t, 30);
        jvl_insert(t, 40);
        jvl_insert(t, 50);

        VERIFY(jvl_get_kth_after(t, 10, 2) == 30);
        VERIFY(jvl_get_kth_after(t, 10, 4) == 50);
        VERIFY(jvl_get_kth_after(t, 10, 1) == 20);
        VERIFY(jvl_get_kth_after(t, 10, 5) == 10); // not enough then return t
        jvl_insert(t, 30);
        jvl_insert(t, 30);

        VERIFY(jvl_get_kth_after(t, 20, 1) == 30);
        VERIFY(jvl_get_kth_after(t, 20, 1) == 30);
        VERIFY(jvl_get_kth_after(t, 20, 1) == 30);

        printf("get kth after works!\n");
        printf("\n");
    }
    {
        // stress test (diagnostic mode)
        jvl_tree *t = jvl_init();
        srand(1);

        int ops = 20000;
        int range = 5000;

        for (int i = 0; i < ops; i++) {
            int v = (rand() % range) - (range / 2);
            jvl_insert(t, v);

            VERIFY(is_avl_jvl(t->root));
            VERIFY(is_size_correct(t->root));
            VERIFY(t->root->size == t->size);
            VERIFY(is_bst_inorder(t->root));
        }
        printf("jerry no longer stressed tf out!\n");
    }
}