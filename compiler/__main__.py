import io

import click  # type: ignore[import]

from .compiler import StarlaCompiler

compiler = StarlaCompiler()


@click.group()
def cli():
    """Generic help message"""


@cli.command(name="compile")
@click.argument("file", type=click.File("r"), default="main.star")
@click.option("-v", "--verbose", count=True, help="generic help message")
@click.option("-q", "--quiet", count=True, help="generic help message")
def cli_compile(file: io.TextIOWrapper, verbose: int, quiet: int):
    """lol3"""
    compiler.compile(file.read(), verbosity=4 + quiet - verbose)


cli()  # pylint: disable=no-value-for-parameter
