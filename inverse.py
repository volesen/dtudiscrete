from math import gcd
from extended_euclidean import egcd


# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency

def inverse_mod(a, n):
    ''' Returns the multiplicative inveres of "a (mod n)" with steps '''
    if gcd(a, n) != 1:
    	return f'Da gcd({a}, {n}) =/= 1, er der jvf. "Sætning 5.6" ikke en multiplikativ inveres af {a} modulus {n}'

    # If gcd(a, n) = 1, then the muliplicative inverse is given t from Bezouts identity
    table = egcd(a, n)

    # Get second-to-last row
    k, r, s, t = table[-2]

    return f'Da {s}*{a} + {t}*{n} = {1} følger det at {s}*{a} ≡ 1 (mod {n}) '