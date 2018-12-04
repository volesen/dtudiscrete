import pytest
from math import gcd
from random import randint


from extended_euclidean import egcd

min_int = -2 ^ 16
max_int = 2 ^ 16

test_data = [(randint(0, max_int), randint(0, max_int)) for i in range(0, 100)]


@pytest.mark.parametrize('a,b', test_data)
def test_gcd(a, b):
    table = egcd(a, b)
    for row in table:
        k, r, s, t = row

        # Assert Bezouts identity for each row
        assert s*a + t*b == r

    # Get second-to-last row
    k, r, s, t = table[-2]

    # Assert gcd(a,b) is correct
    assert r == gcd(a, b)
