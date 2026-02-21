#ifndef JVL_H
#define JVL_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct jvl_node jvl_node;
typedef struct jvl_tree jvl_tree;

struct jvl_node {
    int64_t tastiness;
    int32_t height;
    int32_t size;
    jvl_node *left;
    jvl_node *right;
};

struct jvl_tree {
    int32_t size;
    jvl_node *root;
};

jvl_tree *jvl_init(void);
void jvl_insert(jvl_tree *tree, int64_t tastiness);
bool jvl_search(const jvl_tree *tree, int64_t tastiness);
uint32_t jvl_size(const jvl_tree *tree);
int64_t jvl_get_min(const jvl_tree *tree);
int64_t jvl_get_max(const jvl_tree *tree);
int64_t jvl_get_kth_after(const jvl_tree *tree, int64_t tastiness, int32_t k);

#endif
