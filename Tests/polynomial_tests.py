import pytest
from random import randint


from polynomials import Polynomial


def random_polynomial(min_int, max_int, degree):
    result = {}
    for i in range(0, degree + 1):
        result[i] = randint(min_int, max_int)
    return Polynomial(result)



test_data = [(random_polynomial(-2 ^ 16, 2 ^ 16, 4), random_polynomial(-2 ^ 16, 2 ^ 16, 4)) for i in range(0, 100)]


@pytest.mark.parametrize('a,b', test_data)
def test_polynomial_multiplication(a, b):
    product = a * b
    assert product.y(0) == a.y(0) * b.y(0)
    assert product.y(1) == a.y(1) * b.y(1)
    assert product.y(-50) == a.y(-50) * b.y(-50)


