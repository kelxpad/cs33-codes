#include "superstition.h"
#include "lab05a.c"
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

// O(n^2) mock hey_ya
int *hey_ya(const char *t) {
    if (!t) return NULL;

    int n = strlen(t);
    int *x = malloc(sizeof(int) * n);
    if (!x) return NULL;

    for (int i = 0; i < n; i++) {
        int len = 1; // at least the center itself

        while (i - len >= 0 && i + len < n && t[i - len] == t[i + len]) {
            len++;
        }

        // total palindrome length = 2*len - 1
        x[i] = 2 * len - 1;
    }

    return x;
}

int main() {
    const char *s = "abbaabbca";
    Pocoloco *p = init_p(s);

    VERIFY(is_lucky_substring(p, 1, 4));
    VERIFY(!is_lucky_substring(p, 1, 5));
    VERIFY(is_lucky_substring(p, 2, 7));
    VERIFY(is_lucky_substring(p, 2, 2));
    printf("%s", "All tests passed!\n");
}
