#include "crusade.h"
#include <assert.h>

void test1() {
    int n = 5;
    int m = 6;
    route routes[] = {
        {.u = 1, .v = 2, .t = 5},
        {.u = 2, .v = 3, .t = 10},
        {.u = 2, .v = 4, .t = 5},
        {.u = 3, .v = 1, .t = 5},
        {.u = 4, .v = 1, .t = 5},
        {.u = 5, .v = 1, .t = 5},
    };
    crusader *c = c_init(n, m, routes);

    int s1[] = {1, 2, 3};
    assert(min_crusade(c, 3, s1) == 15);
    int s2[] = {1, 4, 3};
    assert(min_crusade(c, 3, s2) == 30);
    int s3[] = {5, 1, 5};
    assert(min_crusade(c, 3, s3) == -1);
}

int main() {
    test1();
    // TODO: add more test cases
}
