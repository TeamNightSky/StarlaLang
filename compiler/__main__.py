import io
import logging

import click  # type: ignore[import]

from .compiler import StarlaCompiler

compiler = StarlaCompiler()


@click.group()
def cli():
    """Welcome to the Starla compiler!"""


@cli.command(name="compile")
@click.argument("file", type=click.File("r"), default="main.star")
@click.option("-l", "--level", default="ERROR", help="Logging level, INFO, DEBUG, etc.")
def cli_compile(file: io.TextIOWrapper, level: str):
    """Compiles a source file into a binary."""
    compiler.compile(file.read(), level=getattr(logging, level.upper()))


@cli.command(name="interactive")
def cli_interactive(verbose: int):
    """Debug your code interactively by looking at ASTs of snippets!"""
    code = ""
    click.echo("------ Code Editor ------")
    while True:
        line = input(": ")
        if line.strip() == "":
            break
        code += line + "\n"
    click.echo(compiler.compile(code, level=getattr(logging, level.upper())))


cli()  # pylint: disable=no-value-for-parameter
