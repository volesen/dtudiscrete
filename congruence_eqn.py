from math import gcd
from extended_euclidean import egcd
from inverse import inverse_mod

# TODO: Notes use egcd(n, a) which switches s, t. Fix consistency

def congruence_eqn(a, b, n):
    ''' Solves for x in "x * a ≡ b (mod n)" with steps '''

    d = gcd(a, n)

    # Base case
    if d == 1:
    	c = inverse_mod(a, n, steps = False)

    	return f'By "Theorem 5.8" the equation is equivalent to x ≡ c*b (mod n) where c={c} is the multiplicative inverse of a modulus n. Thus x ≡ {c * b} ≡ {(c * b) % n} (mod {n})'

    # If d does not divide a, there are no solutions
    if d//b != 0:
    	return f'For d = gcd({a}, {n}), as d does not divide b, there exists no solutions per "Theorem 5.7"'

    # If d divides b, the eqation is equivalent to solving a' ≡ b' (mod n')
    a_prime = a//d
    b_prime = b//d
    n_prime = n//d

    return congruence_eqn(a_prime, b_prime, n_prime)

