# include "jvl.h"
# include <stdlib.h>
# include <assert.h>


// a = pivot
// b = root
// c = what will attach to root from pivot
// d = stay with pivot
// e = stay with root

int32_t height(jvl_node* x){
    if (x == NULL){
        return -1;
    }
    return x->height;
}

int32_t reset_height(jvl_node* x){
    if (x == NULL){
        return -1;
    }
    return height(x->left) > height(x->right) ? height(x->left) +1 : height(x->right) + 1;
}

// node->tastiness = key
// node->height = AVL height
// node->size = subtree size (not just duplicates)
// to implement get kth after efficiently, we need subtree sizes
// we treat duplicates as separate nodes, going to the right subtree
/* we maintain the INVARIANT:
node->size = 1 + size(node->left) + size(node->right)
*/ 
int32_t sz(jvl_node* x) {
    return x ? x->size : 0;
}

int32_t count_le(jvl_node* node, int64_t t) {
    if (!node) { return 0; }

    if (node->tastiness <= t) {
        // node + entire left subtree count
        return sz(node->left) + 1 + count_le(node->right, t);
    } else {
        return count_le(node->left, t);
    }
}

int64_t select_kth(jvl_node* node, int32_t k) {
    assert(node && k >= 1 && k <= sz(node));
    int32_t left_sz = sz(node->left);

    if (k <= left_sz) {
        return select_kth(node->left, k);
    }
    else if (k == left_sz + 1) {
        return node->tastiness;
    }
    else {
        return select_kth(node->right, k - left_sz - 1);
    }
}

// any time children cahnge, call pull(x)
void pull(jvl_node* x) {
    if (!x) { return; }
    x->height = 1 + (height(x->left) > height(x->right)
                    ? height(x->left)
                    : height(x->right));
    x->size = 1 + sz(x->left) + sz(x->right);
}
jvl_node *join(jvl_node* l, jvl_node* x, jvl_node* r){
    x->left = l;
    x->right = r;
    pull(x);
    return x;
}
jvl_node *right_rot(jvl_node *x){
    jvl_node* a = x->left;
    jvl_node* b = x;
    jvl_node* c = a->right;
    jvl_node* d = a->left;
    jvl_node* e = x->right;
    return join(d, a, join(c, b, e));
}

jvl_node *left_rot(jvl_node *x){
    jvl_node* a = x->right;
    jvl_node* b = x;
    jvl_node* c = a->left;
    jvl_node* d = a->right;
    jvl_node* e = x->left;
    return join(join(e, b, c), a, d);
}

jvl_node *rebalance(jvl_node* x){ 
    if (!x) { return x; }

    pull(x);
    
    int32_t diff = height(x->right) - height(x->left); 
    
    if (diff <= -2) {
        // then left heavy
        assert(x->left != NULL);
        int32_t l_diff = height(x->left->right) - height(x->left->left);

        if (l_diff <= 0) {
            return right_rot(x);    // LL
        } else {
            x->left = left_rot(x->left);
            return right_rot(x);    // LR
        }
    }

    else if (diff >= 2) {
        // then right heavy
        assert(x->right != NULL);
        int32_t r_diff = height(x->right->left) - height(x->right->right);

        if (r_diff <= 0) {
            return left_rot(x);     // RR
        } else {
            x->right = right_rot(x->right);
            return left_rot(x);
        }
    }
    pull(x);
    return x;
}

jvl_node *_jvl_insert(jvl_node *node, int64_t tastiness, jvl_tree *tree){
    // Insert like typical bst then rebalance
    if (node == NULL){
        node = malloc(sizeof(jvl_node));
        node->tastiness = tastiness;
        node->height = 0;
        node->size = 1;
        node->left = NULL;
        node->right = NULL;
        return node;
    }

    if (tastiness < node->tastiness) {
        node->left = _jvl_insert(node->left, tastiness, tree);
    } else {
        // tastiness >= node->tastiness goes right with duplicates allowed
        node->right = _jvl_insert(node->right, tastiness, tree);
    }

    return rebalance(node);
}

void jvl_insert(jvl_tree *tree, int64_t tastiness){
    // Insert like typical bst then rebalance
    // Insight: no matter what happens, tree size increments by 1
    tree->size++;
    tree->root = _jvl_insert(tree->root, tastiness, tree);
    
}

bool _jvl_search(const jvl_node *root, int64_t tastiness){
    // Regular bst search
    if (root == NULL){
        return false;
    }
    if (root->tastiness == tastiness){
        return true;
    }
    else if (root->tastiness < tastiness){
        return _jvl_search(root->right, tastiness);
    }
    else if (root->tastiness >tastiness){
        return _jvl_search(root->left, tastiness);
    }
    // for completeness sake
    return false;  
}

int64_t _jvl_get_kth_after(const jvl_tree *tree, int64_t tastiness, int32_t k) {
    int32_t c = count_le(tree->root, tastiness);
    int32_t target = c + k;

    if (target > tree->size) {
        return tastiness;   // not enough elements
    }

    return select_kth(tree->root, target);
}
bool jvl_search(const jvl_tree *tree, int64_t tastiness){
    // Regular bst search
    return _jvl_search(tree->root, tastiness);
}

uint32_t jvl_size(const jvl_tree *tree){
    return tree->size;
}

int64_t _jvl_get_min(const jvl_node *node){
    if (node->left == NULL){
        return node->tastiness;
    }
    return _jvl_get_min(node->left);
}
int64_t jvl_get_min(const jvl_tree *tree){
    return _jvl_get_min(tree->root);
}

int64_t _jvl_get_max(const jvl_node *node){
    if (node->right == NULL){
        return node->tastiness;
    }
    return _jvl_get_max(node->right);
}
int64_t jvl_get_max(const jvl_tree *tree){
    return _jvl_get_max(tree->root);
}


int64_t jvl_get_kth_after(const jvl_tree *tree, int64_t tastiness, int32_t k){
    return _jvl_get_kth_after(tree, tastiness, k);
}