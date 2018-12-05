from math import gcd
from extended_euclidean import egcd


# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency
def inverse_mod(a, n, steps=True):
    '''
    Solves for the multiplicative inverse of :math:`a \mod n` by showing the steps.
    
    :param int a: Parameter of the equation.
    :param int n: Parameter of the equation.
    :param int steps: Boolean flag deciding whether to return the steps of the operation, or just the solution.
    
    :return: Multiplicative inverse of the equation.
    :rtype: str or int
    '''

    if gcd(a, n) != 1:
        return f'As gcd({a}, {n}) =/= 1, there does not exist a multiplicative inverse of {a} modulus {n} by per "Theorem 5.6"' if steps else None

    # If gcd(a, n) = 1, then the muliplicative inverse is given t from Bezouts identity
    table = egcd(a, n)

    # Get second-to-last row
    k, r, s, t = table[-2]

    return f'Da {s}*{a} + {t}*{n} = {1} følger det at {s}*{a} ≡ 1 (mod {n}) ' if steps else s
