from extended_euclidean import egcd
from tabulate import tabulate

def get_explanation(table, k):
    return f'Da {table[k-2][1]} = {-1*table[k][3+(k%2)]}*{table[k-1][1]} + {table[k][1]}'


def pretty_print_table(a,b):
    table = egcd(a, b)
    table_with_explanation = [('k', 'r_k', 's_k', 't_k', 'Forklaring')]

    table_with_explanation.append((table[0][0], table[0][1], table[0][2], table[0][3], 'Dette er a'))
    table_with_explanation.append((table[1][0], table[1][1], table[1][2], table[1][3], 'Dette er b'))

    for i in range(2,len(table)):
        table_with_explanation.append((table[i][0], table[i][1], table[i][2], table[i][3], get_explanation([table[i-2], table[i-1], table[i]], i)))

    return tabulate(table_with_explanation)