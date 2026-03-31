# O(sqrt(n)) trial division
def prime_factorize(n):
    if n == 0:
        raise ValueError("0 has infinitely many factors")
    
    factors = []

    if n < 0:
        factors.append(-1)
        n = -n
    
    # factor out 2
    while n % 2 == 0:
        factors.append(2)

    # factor odd numbers
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # remaining prime:
    if n > 1:
        factors.append(n)
    
    return factors