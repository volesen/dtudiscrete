from math import gcd
from extended_euclidean import egcd


# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency
def inverse_mod(a, n, steps=True):
    ''' Returns the multiplicative inveres of "a (mod n)" with steps '''

    if gcd(a, n) != 1:
    	return f'As gcd({a}, {n}) =/= 1, there does not exist a multiplicative inverse of {a} modulus {n} by per "Theorem 5.6"' if steps else None

    # If gcd(a, n) = 1, then the muliplicative inverse is given t from Bezouts identity
    table = egcd(a, n)

    # Get second-to-last row
    k, r, s, t = table[-2]

    return f'Da {s}*{a} + {t}*{n} = {1} følger det at {s}*{a} ≡ 1 (mod {n}) ' if steps else s