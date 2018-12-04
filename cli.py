import click
from pretty_print import pretty_print_table


@click.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
def egcd(a, b):
    click.echo(pretty_print_table(a, b))



# Execute CLI
if __name__ == "__main__" :
	egcd()
