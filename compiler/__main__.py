import io

import click  # type: ignore[import]

from .compiler import StarlaCompiler

compiler = StarlaCompiler()


@click.command()
@click.argument("file", type=click.File("r"), default="main.star")
def cli(file: io.TextIOWrapper):
    file_ast = compiler.compile(file.read())
    click.echo(file_ast)


cli()  # pylint: disable=no-value-for-parameter
