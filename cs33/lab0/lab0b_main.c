#include "marble_game.h"

#include <assert.h>

void test1() {
    int n = 4;
    int64_t row1[] = {5, 10, 5, 5,};
    int64_t row2[] = {10, 5, 5, 10,};
    int64_t row3[] = {5, 5, 10, 5,};
    int64_t row4[] = {5, 10, 5, 10,};

    int64_t *a[] = {row1, row2, row3, row4};

    assert(min_cost(n, a) == 15);
}

int main() {
    test1();
    // TODO: add more test cases
}
