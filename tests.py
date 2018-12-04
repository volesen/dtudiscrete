import pytest
from math import gcd
from random import randint


from extended_euclidean import egcd

testdata = [(randint(0,2^16), randint(0,2^16)) for i in range(0,100)]

print('hello')

@pytest.mark.parametrize('a,b', testdata)
def test_gcd(a, b):
    table = egcd(a,b)
    for row in table:
        k, r, s, t = row

        # Assert Bezouts identity for each row
        assert s*a + t*b == r

    # Get second-to-last row
    k, r, s, t = table[-2]

    # Assert gcd(a,b) is correct
    assert r == gcd(a,b)

#@pytest.mark.parametrize('a,b', testdata)
#def test_polynomial(a, b):
        