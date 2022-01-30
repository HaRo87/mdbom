# Markdown SBOM

[![ci](https://github.com/HaRo87/mdbom/workflows/ci/badge.svg)](https://github.com/HaRo87/mdbom/actions?query=workflow%3Aci)
[![cd](https://github.com/HaRo87/mdbom/workflows/deploy/badge.svg)](https://github.com/HaRo87/mdbom/actions?query=workflow%3Adeploy)
[![codecov](https://codecov.io/gh/HaRo87/mdbom/branch/main/graph/badge.svg?token=TGS5QA1M48)](https://codecov.io/gh/HaRo87/mdbom)
[![documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg?style=flat)](https://HaRo87.github.io/mdbom/)
[![pypi version](https://img.shields.io/pypi/v/mdbom.svg)](https://pypi.org/project/mdbom/)

Transform Software Bill Of Materials (SBOM) to Markdown.

## Requirements

MdBOM requires Python 3.8 or above.

## Documentation

The [documentation](https://haro87.github.io/mdbom/) is hosted on GitHub Pages.

## Installation

With `pip`:
```bash
pip install mdbom
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python -m pip install --user pipx

pipx install --python python3.8 mdbom
```

## Development

You need [Task](https://taskfile.dev/#/installation).

Setup your development environment:

```bash
task setup
```

