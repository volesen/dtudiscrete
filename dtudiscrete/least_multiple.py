from math import gcd
from extended_euclidean import egcd

# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency

def lcm(a, b, steps = True):
    '''
        This function solves for m in :math:`m = LCM(a, b)`.
        
        :param int a: Parameter of the equation.
        :param int b: Parameter of the equation.
        :param int m: Parameter of the equation.
        :param bool steps: Boolean flag deciding whether to return the steps of the operation.
        
        :return: Steps showing solution for x.
        
        :rtype: str or int
    '''

    d = gcd(a, b) #Use egcd()?
    
    if steps :
        return f'The LCM({a}, {b}) = {(a * b) / d} = ({a} * {b}) / {d}, where {d} is gcd({a}, {b}).'
    else :
        return (a * b) / d
