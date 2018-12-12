#!/usr/bin/env python3

'''
    The CLI interface for the package.
    
    The avabilable commands are as such (see --help for more information):
        - *egcd*: Calculate the GCD of the two integer inputs.
        - *ceqn*: Solve the given congruence equation.
        - *crt*: Solve for the chinese remainder.
'''

import click

from .pretty_print import pretty_print_table
from .least_multiple import lcm
from .congruence_eqn import congruence_eqn
from .congruence_eqn_sys import chinese_remainder


@click.group()
def cli():
    pass



@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
@click.option('--use-latex', is_flag = True)
def egcd(a, b, use_latex):
    click.echo(pretty_print_table(a, b, "latex" if use_latex else "plain"))
    click.echo('\n' + lcm(a, b))



@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
@click.argument('n', type=int)
def ceqn(a, b, n):
    click.echo(congruence_eqn(a, b, n, steps = True).encode('utf-8'))



@cli.command()
@click.argument('a1', type=int)
@click.argument('a2', type=int)
@click.argument('n1', type=int)
@click.argument('n2', type=int)
def crt(a1, a2, n1, n2):
    click.echo(chinese_remainder(a1, a2, n1, n2).encode('utf-8'))



if __name__ == '__main__':
    # If no command is given, assume congruence equation.
    ceqn()
