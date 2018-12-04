from extended_euclidean import egcd
from tabulate import tabulate

def get_explanation(table, k):
    r = table[k][1]
    r1= table[k-1][1]
    r2 = table[k-2][1]

    return f'Da {r2} = {r2//r1}*{r1} + {r}'


def pretty_print_table(a,b):
    table = egcd(a, b)
    table_with_explanation = [('k', 'r_k', 's_k', 't_k', 'Forklaring')]

    table_with_explanation.append((*table[0], 'Dette er a'))
    table_with_explanation.append((*table[1], 'Dette er b'))

    for i in range(2,len(table)):   
        table_with_explanation.append((*table[i], get_explanation(table, i)))

    return tabulate(table_with_explanation)
