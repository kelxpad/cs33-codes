#ifndef CALC_H
#define CALC_H

#include <stdint.h>
#include <stdbool.h>

// you need to implement these
typedef struct calc calc;

calc *calc_init(void);
calc *calc_push(calc *s, int64_t x);
calc *calc_apply(calc *s, char op);
calc *calc_undo(calc *s, int k);
int64_t calc_peek(calc *s);

#endif
