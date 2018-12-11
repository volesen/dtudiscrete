import pytest
from random import randint
from dtudiscrete.polynomials import Polynomial


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

div_test_data = [(Polynomial({0: 16, 2: -2, 3: 8, 4: 1}), Polynomial({0: 1, 1: -4, 2: 2}), Polynomial({0: 35/4, 1: 5, 2: 1/2}), Polynomial({0: 29/4, 1: 30}))]


@pytest.mark.parametrize('a,b', test_data)
def test_polynomial_multiplication(a, b):
    product = a * b
    assert product.y(0) == a.y(0) * b.y(0)
    assert product.y(1) == a.y(1) * b.y(1)
    assert product.y(-50) == a.y(-50) * b.y(-50)


@pytest.mark.parametrize('a,b,quo,mod', div_test_data)
def test_polynomial_division(a, b, quo, mod):
    calc_quo, calc_mod = a.divide(b)
    assert calc_quo == quo
    assert calc_mod == mod


