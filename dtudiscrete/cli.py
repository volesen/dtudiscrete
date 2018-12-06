#!/usr/bin/env python3
import click
from pretty_print import pretty_print_table
from dtudiscrete.least_multiple import lcm


@click.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
@click.option('--use-latex', is_flag = True)
def egcd(a, b, use_latex):
    click.echo(pretty_print_table(a, b, "latex" if use_latex else "plain"))
    click.echo('\n' + lcm(a, b))


# Execute CLI
if __name__ == "__main__" :
	egcd()
