# Exercise 20: Implement is_prime using find_prime_factor.

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

def is_prime(n):
    if n in (0, 1, -1):
        return False
    if n < 0:
        n = -n
    return find_prime_factor(n) == n