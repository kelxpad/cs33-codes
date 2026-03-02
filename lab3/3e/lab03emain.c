#include "calc.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define VERIFY(b) do {\
    bool _b = (b);\
    fprintf(stderr, "verifying: " #b "\n");\
    if (!_b) {\
        fprintf(stderr, "verification failed!\n");\
        exit(1);\
    }\
} while (0)

int main() {
    calc* c_0 = calc_init(); // NULL
    calc* c_1a = calc_push(c_0, 100); // 100
    calc* c_1b = calc_push(c_0, 123); // 123
    assert(calc_peek(c_1a) == 100);
    assert(calc_peek(c_1b) == 123);

    calc* c_2a = calc_push(c_1a, 200); // 200 -> 100
    calc* c_3a = calc_push(c_2a, 300); // 300 -> 200 -> 100
    calc* c_4a = calc_apply(c_3a, '-'); // -100 -> 100
    assert(calc_peek(c_4a) == -100);
    assert(calc_peek(c_3a) == 300);

    calc* c_3c = calc_undo(c_4a, 1); // 300 -> 200 -> 100
    calc* c_4c = calc_apply(c_3c, '*'); // 60000 -> 100
    calc* c_5c = calc_apply(c_4c, '+'); // 60100
    assert(calc_peek(c_4c) == 60000);
    assert(calc_peek(c_5c) == 60100);

    calc* c_4d = calc_undo(c_5c, 1); // 60000 -> 100
    calc* c_3e = calc_undo(c_4d, 1); // 300 -> 200 -> 100
    calc* c_0g = calc_undo(c_3e, 5); // NULL
    assert(calc_peek(c_4d) == 60000);
    assert(calc_peek(c_3e) == 300);

    // add more testcases
}
