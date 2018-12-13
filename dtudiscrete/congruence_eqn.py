from math import gcd
from .extended_euclidean import egcd
from .inverse import inverse_mod
from .pretty_print import pretty_print_table
# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency

def congruence_eqn(a, b, n, steps = True,  explanation = ''):
    '''
        This function solves for x in :math:`x \cdot a \equiv b \mod n`.
        
        :param int a: Parameter of the equation.
        :param int b: Parameter of the equation.
        :param int n: Parameter of the equation.
        :param bool steps: Boolean flag deciding whether to return the steps of the operation.
        
        :return: Steps showing solution for x.
        
        :rtype: str
    '''
    d = gcd(a, n)

    # Base case
    if d == 1:
        explanation += 'Determining gcd(a, n):\n'

        explanation += pretty_print_table(a, n) + '\n'

        c = inverse_mod(a, n, steps = False)

        explanation +=  f'By "Theorem 5.8" the equation is equivalent to x ≡ c*b (mod n) where c={c} is the multiplicative inverse of a modulus n. Thus x ≡ {c}*{b} ≡ {c * b} ≡ {(c * b) % n} (mod {n}) \n'
        
        return explanation if steps else c


    # If d does not divide a, there are no solutions
    if b//d != 0:
        explanation += f'For d = gcd({a}, {n}), as d does not divide b, there exists no solutions per "Theorem 5.7"\n'
        return explanation if steps else None

    # If d divides b, the eqation is equivalent to solving a' ≡ b' (mod n')
    a_prime = a//d
    b_prime = b//d
    n_prime = n//d

    explanation += f'As d = gcd(a, n) = {d} divides b, the eqation is equivalent to solving, a* ≡ b* (mod n*), where a* = a/d = {a}/{d} = {a//d}, b* = b/d = {b}/{d} = {b//d}, n* = n/d = {n}/{d} = {n//d}. \n - Trying to solve for {a_prime} ≡ {b_prime} (mod {n_prime}):\n'

    return congruence_eqn(a_prime, b_prime, n_prime, steps=steps, explanation = explanation)
