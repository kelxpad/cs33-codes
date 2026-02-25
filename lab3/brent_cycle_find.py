"""
keywords for brent are mostly the same as floyd except:
- hinting at expensive transitions
- pollard-rho/factorization
- fuckass large search space
- perfomance-sensitive cycle detection
- exponential search window expansion

brent can be faster because floyd may revisit the same
nodes multiple times, while brent reduces repeated
traversal by expanding windows.

search forward in doubling chunks until a loop appears.
"""

def brent_cycle_find(f: callable, s0) -> tuple[int, int]:
    """
    returns (mu, lam):
        mu = tail length before cycle
        lam = cycle length
    """
    # phase 1: find cycle length lam
    power = lam = 1
    tortoise = s0
    hare = f(s0)

    while tortoise != hare:
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1

    # phase 2: find tail length mu
    mu = 0
    tortoise = hare = s0

    # move hare lam steps ahead
    for _ in range(lam):
        hare = f(hare)

    # move both until they meet
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1
    
    return mu, lam