"""Main module for the MdBOM CLI tool.

MdBOM takes a CycloneDX standard bom.json
file and extracts relevant data from it for
creating a 3rd party software markdown document.
"""

import logging

import click

from mdbom.bom.processor import ProcessingError
from mdbom.bom.pypi import PyPiProcessor
from mdbom.md.md import GeneratingError, generate_markdown

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(levelname)s [%(module)s] : %(message)s")
log_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.NOTSET, handlers=[log_handler])

logger = logging.getLogger("MdBOM")


@click.group()
def cli():
    """Run the main entry point for MdBOM."""
    pass


@click.command()
def info():
    """Print a simple info about MdBOM."""
    click.echo("Check the documentation: https://haro87.github.io/mdbom/")
    click.echo("for further information.")


@click.command()
@click.option(
    "--input",
    "input_file",
    default="bom.json",
    help="BOM file to process",
)
@click.option(
    "--output",
    "output_file",
    default="3rd-party.md",
    help="Target .md file",
)
@click.option(
    "--template",
    "template_file",
    default="template.md.jinja",
    help="The Jinja2 template file",
)
def generate(input_file, output_file, template_file):
    """Processes a given BOM file and generates the markdown file.

    Args:
        input_file: The input_file holding the BOM info.
        output_file: The output_file where the result should be stored.
        template_file: The template_file to be used for markdown generation.

    Raises:
        ClickException: In case invalid input is provided.
    """
    try:
        pypi_proc = PyPiProcessor()
    except ProcessingError as pie:
        raise click.ClickException(pie)

    try:
        packages = pypi_proc.get_packages_from_bom(filename=input_file)
    except ProcessingError as pge:
        raise click.ClickException(pge)

    try:
        packages = pypi_proc.construct_urls(packages=packages)
    except ProcessingError as pce:
        raise click.ClickException(pce)

    try:
        generate_markdown(
            template=template_file,
            file_name=output_file,
            packages=packages,
        )
    except GeneratingError as ge:
        raise click.ClickException(ge)

    click.echo("Generated markdown file:")
    click.echo(output_file)


cli.add_command(info)
cli.add_command(generate)
