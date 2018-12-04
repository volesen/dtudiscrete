import numpy as np


def egcd(a, b):
    table = []

    table.append((0, a, 1, 0))
    table.append((1, b, 0, 1))

    k = 1
    while table[k][1] != 0:
        k += 1
        k1, r1, s1, t1 = table[k-2]
        k2, r2, s2, t2 = table[k-1]
        r = r1 % r2
        s = s1 - s2 * (r1 // r2)
        t = t1 - t2 * (r1 // r2)
        table.append((k, r, s, t)) 

    return table
