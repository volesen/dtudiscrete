import pytest
from math import gcd
from random import randint

from ..inverse import inverse_mod


max_int = 2**16

test_data = [(randint(0, max_int), randint(0, max_int)) for i in range(0, 100)]

@pytest.mark.parametrize('a,n', test_data)
def test_inverse_mod(a, n):
	c = inverse_mod(a, n, steps=False)

	if c == None:
		# Assert that when there is no solution, gcd(a,n) must be different from one
		assert gcd(a,n) != 1
	else:
		assert (a*c) % n == 1
