from math import gcd
from .extended_euclidean import egcd
from .pretty_print import pretty_print_table

# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency

def chinese_remainder(b1, b2, n1, n2, steps = True, explanation = ''):
    '''
        This function solves for the chinese remainder.
    '''
    explanation += pretty_print_table(n1, n2) + '\n'

    if gcd(n1, n2) != 1:
        explanation += 'As gcd(n1, n2) =/= 1, this cannot be solved the "Chinese Remainder Theorem"'
    else:
        # When gcd(n1, n2) "Chinese Remainder Theorem" can be used
        u1, u2 = egcd(n1, n2)[-2][2:5]
        
        x_p = u1*n1*b2 + u2*n2*b1

        explanation += f'By the "Chinese Remainder Theorem", as gcd(n1,n2)=1, the equations can be reduced to x ≡ u1*n1*b2 + u2*n2*b1 (mod n1*n2), which is x ≡ {x_p} ≡ {x_p % (n1*n2)} (mod {n1*n2})'

    return explanation
