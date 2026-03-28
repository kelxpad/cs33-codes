#ifndef SUPERSTITION_H
#define SUPERSTITION_H

#include <stdint.h>
#include <stdbool.h>

typedef struct Pocoloco Pocoloco;

Pocoloco *init_p(const char *s);
bool is_lucky_substring(const Pocoloco *p, int i, int j);

int *hey_ya(const char *t);

#endif
