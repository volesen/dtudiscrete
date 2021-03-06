"""
Functions relates to the Extended Euclidean Algorithm.
"""

def egcd(a, b):
    '''
        Generates table with all calculations for Extended Euclidean Algortihm.
        
        :param int a: The first number to run Euclid on.
        :param int b: The second number to run Euclid on.
        
        :return: The GCF (Greatest Common Factor) of the input.
        
        :rtype: list[int]
    '''
    
    table = []

    table.append((0, a, 1, 0))
    table.append((1, b, 0, 1))
    
    k = 1
    while table[k][1]:
        k += 1
        k1, r1, s1, t1 = table[k-2]
        k2, r2, s2, t2 = table[k-1]
        r = r1 % r2
        s = s1 - s2 * (r1 // r2)
        t = t1 - t2 * (r1 // r2)
        table.append((k, r, s, t)) 

    return table
