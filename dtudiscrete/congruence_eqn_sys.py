from math import gcd
from extended_euclidean import egcd

# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency

def chinese_remainder(b1, b2, n1, n2):
    '''
        This function solves for the chinese remainder (TODO: Equation).
    '''

    if gcd(n1, n2) != 1:
    	raise NotImplementedError

    # When gcd(n1, n2) "Chinese Remainder Theorem" can be used
    u1, u2 = egcd(n1, n2)[-2][2:5]

    x_p = u1*n1*b2 + u2*n2*b1

    return f'By the "Chinese Remainder Theorem", as gcd(n1,n2)=1, the equations can be reduced to x ≡ u1*n1*b2 + u2*n2*b1 (mod n1*n2), which is x ≡ {x_p} ≡ {x_p % (n1*n2)} (mod {n1*n2})'
