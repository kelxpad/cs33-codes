# with this treasure i summon, sieve of erastothenes
def sieve(m):
    if m < 2:
        return []
    
    is_prime = [True] * (m + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= m:
        if is_prime[p]:
            for multiple in range(p*p, m+1, p):
                is_prime[multiple] = False
        p += 1
    
    return [i for i in range(2, m+1) if is_prime[i]]