import io
import logging

import click  # type: ignore[import]

from .compiler import StarlaCompiler

compiler = StarlaCompiler()


@click.group()
def cli():
    """Generic help message"""


@cli.command()
@click.argument("file", type=click.File("r"), default="main.star")
@click.option("-v", "--verbose", count=True, help="generic help message")
@click.option("-q", "--quiet", count=True, help="generic help message")
def compile(file: io.TextIOWrapper, verbose: int, quiet: int):
    """lol3"""
    file_ast = compiler.compile(file.read(), verbosity=4 + quiet - verbose)


cli()  # pylint: disable=no-value-for-parameter
