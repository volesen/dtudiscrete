import pytest
from random import randint


from polynomials import Polynomial


def random_polynomial(min_int, max_int, degree):
    result = {}
    for i in range(0, degree + 1):
        result[i] = randint(min_int, max_int)
    return Polynomial(result)


min_int = -2 ^ 16
max_int = 2 ^ 16
degree = 4
test_data = [(random_polynomial(min_int, max_int, degree), random_polynomial(min_int, max_int, degree))
             for i in range(0, 100)]


@pytest.mark.parametrize('a,b', test_data)
def test_polynomial_multiplication(a, b):
    product = a * b
    assert product.y(0) == a.y(0) * b.y(0)
    assert product.y(1) == a.y(1) * b.y(1)
    assert product.y(-50) == a.y(-50) * b.y(-50)


