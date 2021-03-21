"""Handling markdown conversion."""

from typing import List

from jinja2 import Environment

from mdbom.bom.bom import Package


class GeneratingError(RuntimeError):
    """Generating error for raising generation specific error."""

    pass


def generate_markdown(template, file_name: str, packages: List[Package]):
    """Generate markdown file from provided template.

    Args:
        template: The template which should be used.
        file_name: The file in which the result should be stored.
        packages: The package list.

    Raises:
        GeneratingError: If not all requirements are satisfied.
    """
    if template:
        if file_name:
            with open(template, "r") as template_file:
                md_template = template_file.read()

            md_env = Environment(autoescape=True).from_string(md_template)
            content = md_env.render(packages=packages)

            with open(file_name, "w") as result_file:
                result_file.write(content)
        else:
            raise GeneratingError("No valid output file name provided.")
    else:
        raise GeneratingError("No valid template provided.")
