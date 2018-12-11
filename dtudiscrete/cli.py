#!/usr/bin/env python3
import click
from .pretty_print import pretty_print_table
from .least_multiple import lcm
from dtudiscrete.congruence_eqn import congruence_eqn

@click.group()
def cli():
    pass


@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
@click.argument('n', type=int)
def ceqn(a, b, n):
    click.echo(congruence_eqn(a, b, n, steps = True).encode('utf-8'))


@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
@click.option('--use-latex', is_flag = True)
def egcd(a, b, use_latex):
    click.echo(pretty_print_table(a, b, "latex" if use_latex else "plain"))
    click.echo('\n' + lcm(a, b))


if __name__ == '__main__':
    ceqn()