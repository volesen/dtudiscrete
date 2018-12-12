from math import gcd
from .extended_euclidean import egcd
from .pretty_print import pretty_print_table

# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency
def inverse_mod(a, n, steps=True, explanation =''):
    '''
    Solves for the multiplicative inverse of :math:`a \mod n` by showing the steps.
    
    :param int a: Parameter of the equation.
    :param int n: Parameter of the equation.
    :param int steps: Boolean flag deciding whether to return the steps of the operation, or just the solution.
    
    :return: Multiplicative inverse of the equation.
    :rtype: str or int
    '''

    if gcd(a, n) != 1:
        explanation += f'As gcd({a}, {n}) =/= 1, there does not exist a multiplicative inverse of {a} modulus {n} by per "Theorem 5.6"\n'
        return explanation if steps else None

    # If gcd(a, n) = 1, then the muliplicative inverse is given t from Bezouts identity
    table = egcd(a, n)

    explanation += pretty_print_table(a, n) + '\n'

    # Get second-to-last row
    k, r, s, t = table[-2]

    explanation += f'As {s}*{a} + {t}*{n} = {1} it follows that {s}*{a} ≡ 1 (mod {n})\n'

    return explanation if steps else s
