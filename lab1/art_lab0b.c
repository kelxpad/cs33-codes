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

int32_t size(jvl_node* x){
    if (x == NULL){
        return 0;
    }
    return x->size;
}   

int32_t reset_height(jvl_node* x){
    if (x == NULL){
        return -1;
    }
    return height(x->left) > height(x->right) ? height(x->left) +1 : height(x->right) + 1;
}

int32_t reset_size(jvl_node* x){
    if (x == NULL){
        return 0;
    }
    return size(x->left) +size(x->right) +1;
}

jvl_node *join(jvl_node* l, jvl_node* x, jvl_node* r){
    x->left = l;
    x->right = r;
    x->height = reset_height(x);
    x->size = reset_size(x);
    return x;
}
jvl_node *right_rot(jvl_node *x){
    jvl_node* a = x->left;
    jvl_node* b = x;
    jvl_node* c = x->left->right;
    jvl_node* d = x->left->left;
    jvl_node* e = x->right;
    return join(d, a, join(c, b, e));
}

jvl_node *left_rot(jvl_node *x){
    jvl_node* a = x->right;
    jvl_node* b = x;
    jvl_node* c = x->right->left;
    jvl_node* d = x->right->right;
    jvl_node* e = x->left;
    return join(join(e, b, c), a, d);
}

jvl_node *rebalance(jvl_node* x){ // Possible bugs here
    if (x->right == NULL && x->left == NULL){
        return x;
    }
    int32_t diff = height(x->right) - height(x->left); 
    if (abs(diff) >= 2){
        if (diff < 0){
            // left is taller
            // right rotation/pull
            assert(x->left != NULL);
            int32_t l_diff = height(x->left->right) - height(x->left->left); 
            if (l_diff <= 0){
                return right_rot(x);
            } else{
                x->left = left_rot(x->left);
                x->height = reset_height(x);
                return right_rot(x);
                
            }
        }
        else {
            int32_t r_diff = height(x->right->left) - height(x->right->right);
            if (r_diff <= 0){
                return left_rot(x);
            } else{
                x->right = right_rot(x->right);
                x->height = reset_height(x);
                return left_rot(x);
                
            }
        }
    }
    x->height = reset_height(x);
    x->size = reset_size(x);
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
    }
    else if (node->tastiness >= tastiness){
    node->left = _jvl_insert(node->left, tastiness, tree);
    
    }
    else if (node->tastiness < tastiness){
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
int32_t count_valid_nodes(jvl_node* x, int64_t tastiness){
    if (x == NULL){
        return 0;
    }
    if (x->tastiness > tastiness){
        return 1 + size(x->right) + count_valid_nodes(x->left, tastiness);
    }
    return count_valid_nodes(x->right, tastiness);
}
int64_t _jvl_get_kth_after(jvl_node *x, int64_t tastiness, int32_t k){
    if (x == NULL){
        return tastiness;
    }
    if (x->tastiness <= tastiness){
        return _jvl_get_kth_after(x->right, tastiness, k);
    }
    else {
        // Insight: We only need to consider the left child
        // To calc num_valid, there are 3 cases:
        // - If the left child is null, the number of valid is 0
        // - If the left child tastiness is > the tastiness val, then 
        //   we can con conclude that the entire left subtree is up for grabs
        // - If the left child tastiness is <= the tastiness val, then, 
        //   we go right, but use k -= (num_valid + 1)
        int32_t num_valid = count_valid_nodes(x->left, tastiness);
        

        if (num_valid + 1 == k){
            return x->tastiness;
        }
        else if (num_valid >= k){
            return _jvl_get_kth_after(x->left, tastiness, k);
        }
        else {
            assert(num_valid < k);
            return _jvl_get_kth_after(x->right, tastiness, k - (num_valid + 1) );
        }
    }
}

// Possible bug: we need to consider duplicates

int64_t jvl_get_kth_after(const jvl_tree *tree, int64_t tastiness, int32_t k){
    // Find the next larger
    // go to the right k-1
    // - if there is no right children, traverse upwards until there is or we cant go more than k

    // Insight: We could use inorder traversal to make a flat list and just get the kth largest from there O(n)

    // Insight: What if we use the size attr to refer to the number of nodes that are in that subtree
    // We can then just go to a node with node.t > tastiness and count how many valid nodes are to the left
    // Valid node: a node whose value is > tastiness

    // Find a possible node candidate
    return _jvl_get_kth_after(tree->root, tastiness, k);
}
