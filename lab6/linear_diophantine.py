def egcd():
    ...
    # TODO: implement
    # extended gcd part

def linear_diophantine(a,b,c):
    # ax + by = c
    # ax + by = g
    # integer solutions only
    # has solution if gcd(a,b) | c
    g, x, y = egcd(a, b)
    if c % g == 0:
        k = c // g
        return (k * x, k * y)
    
def get_prime_factor(n):
    d = 2
    for d in range(2, n + 1):
        if n % d == 0:
            return d
    return d

def get_primes(m):
    primes = [True] * (m + 1) 
    primes[0] = primes[1] = False
    for p in range(2, m + 1):
        for d in range(2 * p, m + 1, p):
            primes[d] = False
    return primes

def get_divisors(m):
    divs = [[] for _ in range(m + 1)]
    for n in range(1, m + 1):
        for d in range(n, m + 1, n):
            divs[d].append(n)
    return divs

def crt(a, b, m, n):
    assert gcd(m, n) == 1
    _, u, v = egcd(m, n)
    x = (a * n * v) + (b * m * u)
    assert x % m == 0
    assert x % n == 0
    return x

"""
system of linear equations
system of linear congruences

x balls in a box
- group balls in groups of 32, 11 leftover
- group balls in groups of 33, 12 leftover
find x

x ≅ a (mod m)
x ≅ b (mod n)

gcd(m, n) = 1 (use bezoeques lemma to make it a linear combination)
mu + nv = 1
mu ≅ 0 mod m

anv ≅ a (mod m)
bmu ≅ b (mod n)

anv + bmu ≅ a (mod m)
anv + bmu ≅ b (mod n)

CRT = Chinese Remainder Theorem = Sunzi's Theorem
"""

