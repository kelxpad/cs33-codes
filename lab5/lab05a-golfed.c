#include "superstition.h"
#include <stdlib.h>
#include <string.h>

typedef struct Pocoloco {
    int *radius[5];
} Pocoloco;

int *build(const char *s, int n, int b) {
    int transformed_len = 6 * n + 3;
    char *t = malloc(transformed_len + 1);

    int j = 0;
    for (int i = 0; i < 2 * n + 1; i++, j += 3) {
        if (i % 2 == 0) {
            t[j] = '0';
            t[j + 1] = '0';
            t[j + 2] = '0';
        } else {
            int idx = i / 2;
            int bit = ((s[idx] - 'a') >> b) & 1;

            if (bit == 0) {
                t[j]     = '0';
                t[j + 1] = '1';
                t[j + 2] = '0';
            } else {
                t[j]     = '1';
                t[j + 1] = '0';
                t[j + 2] = '1';
            }
        }
    }

    t[transformed_len] = '\0';
    int *result = hey_ya(t);
    free(t);
    return result;
}

Pocoloco *init_p(const char *s) {
    int n = strlen(s);

    Pocoloco *p = malloc(sizeof(Pocoloco));

    for (int b = 0; b < 5; b++) {
        p->radius[b] = build(s, n, b);
    }

    return p;
}

bool is_lucky_substring(const Pocoloco *p, int i, int j) {
    int center = 3 * (i + j - 1) + 1;
    int length_needed = 3 * (2 * (j - i + 1) - 1);
    for (int b = 0; b < 5; b++) {
        if (p->radius[b][center] < length_needed) {
            return false;
        }
    }
    return true;
}