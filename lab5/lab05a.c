/*
this is the reductions problem, will digest later
TODO: Put more comments about how the solution uses hey_ya significantly.
*/
#include "superstition.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>


#define VERIFY(b) do {\
    bool _b = (b);\
    fprintf(stderr, "verifying: " #b "\n");\
    if (!_b) {\
        fprintf(stderr, "verification failed!\n");\
        exit(1);\
    }\
} while (0)

typedef struct Pocoloco {
    int n;
    int **odd; // [5][n]
    int **even; // [5][n]
} Pocoloco;

char *build_binary(const char *s, int n, int bit) {
    char *t = malloc(n + 1);
    for (int i = 0; i < n; i++) {
        t[i] = ((s[i] - 'a') >> bit & 1) ? '1' : '0';
    }
    t[n] = '\0';
    return t;
}

char *build_even_transform(char *t, int n) {
    char *res = malloc(2*n+2);
    int idx = 0;
    for (int i = 0; i < n; i++) {
        res[idx++] = '#';
        res[idx++] = t[i];
    }
    res[idx++] = '#';
    res[idx] = '\0';
    return res;
}

Pocoloco *init_p(const char *s) {
    int n = strlen(s);

    Pocoloco *p = malloc(sizeof(Pocoloco));
    p->n = n;

    p->odd = malloc(5 * sizeof(int*));
    p->even = malloc(5 * sizeof(int*));

    for (int b = 0; b < 5; b++) {
        char *t = build_binary(s, n, b);
        
        // odd
        p->odd[b] = hey_ya(t);

        // even
        char *t2 = build_even_transform(t, n);
        int *tmp = hey_ya(t2);

        // map back to original indices
        p->even[b] = malloc(n * sizeof(int));
        for (int i = 0; i < n-1; i++) {
            // center between i and i+1 so position 2*i+1
            p->even[b][i] = tmp[2*i+2] / 2;
        }
        p->even[b][n-1] = 0; // no valid center
    }
    return p;
}

bool is_lucky_substring(const Pocoloco *p, int i, int j) {
    i--; j--;

    int len = j - i + 1;

    if (len <= 1) { return true; } // single char/empty strings are palindromes by default

    if (len % 2 == 1) {
        int mid = (i + j) / 2;
        int need = (len + 1) / 2;

        for (int b = 0; b < 5; b++) {
            if (p->odd[b][mid] < need) {
                return false;
            }
        }
    } else {
        int mid = (i + j) / 2;
        int need = len / 2;

        for (int b = 0; b < 5; b++) {
            if (p->even[b][mid] < need) {
                return false;
            }
        }
    }
    return true;
}


int *hey_ya(const char *t) {
    if (!t) { return NULL; }

    int n = strlen(t);
    int *d = malloc(n * sizeof(int));
    if (!d) { return NULL; }

    int l = 0;
    int r = -1;

    for (int i = 0; i < n; i++) {
        int k = 1;

        if (i <= r) {
            int mirror = l + r - i;
            k = d[mirror] < (r - i + 1) ? d[mirror] : (r - i + 1);
        }

        while (i - k >= 0 && i + k < n && t[i - k] == t[i + k]) {
            k++;
        }

        d[i] = k; // palindrome spans

        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }

    return d;
}

int main() {
    char *s = "abbaabbca";
    Pocoloco *p = init_p(s);

    VERIFY(is_lucky_substring(p, 1, 4));
    VERIFY(!is_lucky_substring(p, 1, 5));
    VERIFY(is_lucky_substring(p, 2, 7));
    VERIFY(is_lucky_substring(p, 2, 2));
    printf("%s", "All tests passed!\n");
}

