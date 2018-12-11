from numpy.polynomial.polynomial import Polynomial as poly

class Polynomial(poly):
    '''
        A representation of a Polynomial.
        
        Class Attributes
			coefs: Coefficients.
			degree: The degree of the polynomial.
    '''
    
 from numpy.polynomial.polynomial import Polynomial as poly

class Polynomial(poly):
    def __ne__(self, other):
        return self.degree() != other

    def __str__(self):
        result = []

        for power, coef in enumerate(self.coef):
            if coef == 0:
                continue

            sign = '+' if coef > 0 else '-'
            coef = abs(coef)

            if power == 0:
                result.append(str(coef))
            elif power == 1:
                result.append(f'{coef}*x')
            else:
                result.append(f'{coef}*x^{power}')

            result.append(sign)
            
        # To avoid plus as first sign
        if result[-1] == '+':
            result = result[:-1] 

        return ' '.join(reversed(result)) or '0'