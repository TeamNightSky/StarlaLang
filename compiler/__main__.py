import io
import click

from .compiler import StarlaCompiler

compiler = StarlaCompiler()


@click.command()
@click.argument("file", type=click.File("r"), default="main.star")
def cli(file: io.TextIOWrapper):
    tree = compiler.compile(file.read())
    click.echo(tree)


cli()