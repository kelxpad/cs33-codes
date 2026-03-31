"""
1. compute (g, u, v) = extended_gcd(m, n)
2. check: g must be 1
3. compute: x = (b*m*u + a*n*v) % (m*n)
"""

def extended_gcd(a,b):
    if b == 0:
        return (a,1,0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def crt(a, m, b, n):
    g, u, v = extended_gcd(m, n)

    if g != 1:
        raise ValueError("m and n must be coprime")
    
    x = (b*m*u+a*n*v) % (m*n)
    return x

print(crt(12, 33, 11, 32))  # 1035