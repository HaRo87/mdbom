"""Main module for the MdBOM CLI tool.

MdBOM takes a CycloneDX standard bom.json
file and extracts relevant data from it for
creating a 3rd party software markdown document.
"""

import logging

import click

from mdbom.bom.bom import ProcessingError
from mdbom.bom.npm import NpmProcessor
from mdbom.bom.pypi import PyPiProcessor
from mdbom.md.md import GeneratingError, generate_markdown

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(levelname)s [%(module)s] : %(message)s")
log_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.NOTSET, handlers=[log_handler])

logger = logging.getLogger("MdBOM")

PYPI_PROCESSOR_NAME = "pypi"
NPM_PROCESSOR_NAME = "npm"


@click.group()
def cli():
    """Run the main entry point for MdBOM."""


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
@click.option(
    "--type",
    "proc_type",
    default="pypi",
    help="The processors used for generation (pypi/npm)",
)
def generate(input_file, output_file, template_file, proc_type):
    """Processes a given BOM file and generates the markdown file.

    Args:
        input_file: The input_file holding the BOM info.
        output_file: The output_file where the result should be stored.
        template_file: The template_file to be used for markdown generation.
        proc_type: The processor type which is used to process the BOM file.

    Raises:
        ClickException: In case invalid input is provided.
    """
    processors = {}
    try:
        processors[PYPI_PROCESSOR_NAME] = PyPiProcessor()
    except ProcessingError as pie:
        raise click.ClickException(pie)

    try:
        processors[NPM_PROCESSOR_NAME] = NpmProcessor()
    except ProcessingError as npe:
        raise click.ClickException(npe)

    if proc_type not in processors:
        raise click.ClickException(
            "Invalid processor provided, check --help for available ones",
        )

    try:
        packages = processors[proc_type].get_packages_from_bom(
            filename=input_file,
        )
    except ProcessingError as pge:
        raise click.ClickException(pge)

    try:
        packages = processors[proc_type].construct_urls(packages=packages)
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
