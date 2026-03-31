# Exercise 21: Implement prime_factorize using find_prime_factor.

def _find_prime_factor(n):
    # assumes n >= 2
    for p in range(2, n + 1):
        if n % p == 0:
            return p
        
def find_prime_factor(n):
    if n < 0:
        return find_prime_factor(-n)
    elif n in (0, 1):
        raise ValueError("No prime factor exists.")
    else:
        return _find_prime_factor(n)
    
def prime_factorize(n):
    if n == 0:
        raise ValueError("0 has infinitely many factors.")
    
    factors = []

    if n < 0:
        factors.append(-1)
        n = -n
    
    while n > 1:
        p = find_prime_factor(n)
        factors.append(p)
        n //= p

    return factors