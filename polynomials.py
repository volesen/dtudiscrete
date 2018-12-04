class Polynomial:
    def __init__(self, coefs):
        self.coefs = coefs
    
    def __getitem__(self, key):
        return self.coefs[key] if key in self.coefs.keys() else 0

    def y(self, x):
        result = 0
        for exponent, coef in self.coefs.items():
            result += coef*(x**exponent)
        return result
    
    def __add__(self, pol):
        result = {}
        for exponent, coef in self.coefs.items():
            result[exponent] = coef
        for exponent, coef in pol.coefs.items():
            if exponent in result:
                result[exponent] += coef
            else:
                result[exponent] = coef
        return Polynomial(result)
    
    def __mul__(self, pol):
        result_degree = self.degree() + pol.degree()
        result = {}
        for i in range(0, result_degree + 1):
            coef = 0
            for j in range(0, max(self.degree() + 1, i)):
                coef += self[j]*pol[i-j]
            result[i] = coef
        return Polynomial(result)

    def degree(self):
        return max(self.coefs.keys())

    def __str__(self):
        result = ''
        for exponent, coef in self.coefs.items():
            if exponent == 0:
                result += " + " + str(coef)
            elif exponent == 1:
                result += " + " + str(coef) + "x"
            else:
                result += " + " + str(coef) + 'x^' + str(exponent)
        return result[3:]
