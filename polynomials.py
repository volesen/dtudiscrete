import numpy as np

class Polynomial:
    def __init__(self, coefs):
        self.coefs = coefs
    
    def __getitem__(self, key):
        return self.coefs[key]

    def y(self, x):
        result = 0
        for exponent, coef in self.coefs:
            result += coef*(x**exponent)
        return result
    
    def __add__(self, pol):
        result = {}
        for exponent, coef in self.coefs:
            result[exponent] = coef
        for exponent, coef in pol.coefs:
            if exponent in result:
                result[exponent] += coef
            else:
                result[exponent] = coef
        return Polynomial(result)
    
    def __mul__(self, pol):
        resultDegree = self.degree() + pol.degree()
        result = {}
        for i in range(0, resultDegree + 1):
            coef = 0
            for j in range(0, self.degree() + 1):
                coef += self

    def degree(self):
        return max(self.coefs.keys)
