"""
usual signals for functional graph cycle-finding:

- repeat until it repeats
- sequences become periodic
- find cycle length
- apply function repeatedly
- recurrence relation
- each node points to exactly one node
- teleporters, portals, next city/room
- pointer to next
- linked list cycle, detect loop in pointers
- large iteration count k <= 10^18 or some shit
- pseudorandom problems

floyd: run fast & slow until they eventually meet
"""

def floyd_cycle_find(f: callable, s0):
    """
    args:
        f: function mapping a state to the next state
        s0: starting state
        
    returns:
        (mu, lam)
        mu = tail length before cycle
        lam = cycle length    
    """
    # phase 1: find intersection point
    tortoise = f(s0)
    hare = f(f(s0))

    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))

    # phase 2: find cycle length l
    cycle_len = 1
    hare = f(tortoise)
    while tortoise != hare:
        hare = f(hare)
        cycle_len += 1

    # phase 3: find tail length m
    mu = 0
    tortoise = s0
    hare = s0

    # move hare l steps ahead
    for _ in range(cycle_len):
        hare = f(hare)

    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1

    return mu, cycle_len

