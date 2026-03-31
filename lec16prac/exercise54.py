import math

def extended_gcd(a,b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def crt(a, m, b, n):
    g, u, v = extended_gcd(m, n)

    if g != 1:
        raise ValueError("m and n must be coprime")
    
    x = (b*m*u + a*n*v) % (m*n)
    return x

def smallest_crt_at_least(a,m,b,n,bound):
    x0 = crt(a,m,b,n)
    mod = m*n
    
    k = math.ceil((bound - x0) / mod)
    return x0 + k * mod

print(smallest_crt_at_least(12, 33, 11, 32, 10**6))