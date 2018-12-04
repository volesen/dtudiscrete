import click
from pretty_print import pretty_print_table


@click.command()
@click.argument('a')
@click.argument('b')
def egcd(a, b):
    click.echo(pretty_print_table(a, b))
