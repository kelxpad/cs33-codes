/* strategy: use hey_ya to do the following:
- precompute all palindrome radii in O(n)
- handle all substrings implicitly
for each of the 5 bit-planes:
-  we transform the string into a special binary string, 
- call hey_ya on it,
- then returns, for every possible cnter, the maximum palindrome length centered there


*/

#include "superstition.h"
#include <stdlib.h>
#include <string.h>

// we store 5 arrays (one per bit of each character)
// with each array being the result of hey_ya on the
// transformed binary string
typedef struct Pocoloco {
    int *radius[5]; // radius[b][i] = pal length centered at i for bit b
} Pocoloco;

/*
build the transformed string for a specific bit b from
0 to 4.

let the original string be s[0..n-1]

1. convert to binary using bit b
2. insert separators (#) to make the length 2n+1
3. encode each symbol into 3 characters:
# = 000
0 = 010
1 = 101

so the final length = 3 * (2n+1) = 6n+3
*/
int *build(const char *s, int n, int b) {
    int transformed_len = 6*n+3;
    char *t = malloc(transformed_len + 1);

    int j = 0; // ptr in transformed string

    for (int i = 0; i < 2*n+1; i++, j += 3) {
        if (i % 2 == 0) {
            t[j]     = '0';
            t[j + 1] = '0';
            t[j + 2] = '0';
        } else {
            // this corresponds to a character from s
            int idx = i / 2;

            // extract bit b from s[idx]
            int bit = ((s[idx] - 'a') >> b) & 1;

            if (bit == 0) {
                // encode 0 as 010
                t[j]     = '0';
                t[j + 1] = '1';
                t[j + 2] = '0';
            } else {
                // encode 1 as 101
                t[j]     = '1';
                t[j + 1] = '0';
                t[j + 2] = '1';
            }
        }
    }
    t[transformed_len] = '\0';

    // run hey_ya on the transformed string
    int *result = hey_ya(t);

    free(t);
    return result;
}

/*
initialize the structure
for each of the 5 bits, build a transformed string and
store its hey_ya result.
*/
Pocoloco *init_p(const char *s) {
    int n = strlen(s);

    Pocoloco *p = malloc(sizeof(Pocoloco));

    for (int b = 0; b < 5; b++) {
        p->radius[b] = build(s, n, b);
    }

    return p;
}

/*
check if substring s[i..j] is a palindrome

map original indices into the transformed string
the center of substring [i..j] becomes:

center = 3*(i+j-1)+1

required palindrome length:
need = 3 * (2*(j-i+1) - 1)

check for all 5 bits, if any fails, not a palindrome
*/
bool is_lucky_substring(const Pocoloco *p, int i, int j) {
    // compute center in transformed string
    int center = 3 * (i+j-1) + 1;

    // required palindrome length
    int length_needed = 3 * (2*(j-i+1)-1);

    // check for all 5 bits
    for (int b = 0; b < 5; b++) {
        if (p->radius[b][center] < length_needed) {
            return false;
        }
    }

    return true;
}