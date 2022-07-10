# How to generate a markdown file

## Using a template for your markdown report

You need a template file for generating a markdown file. 
You can have a look at the [examples](https://github.com/HaRo87/mdbom/tree/develop/examples)
provided by the MdBOM project. 

The template can be specified via the `--template` option.

## Generating a markdown file based on a single BOM

Once you have a template and a BOM you should be able to generate
a markdown file via

```bash
mdb generate --input bom.json --output 3rd-party.md --template template.md.jinja
```

This will take the "bom.json" file as input, collect all relevant information and 
use the "template.md.jinja" template to generate the "3rd-party.md" file.

## Generating a markdown file based on multiple BOMs

It is also possible to take multiple BOM files as input by simply providing
a directory path via the `--input` option. If a directory is provided
MdBOM tries to process all `.json` files in that directory. Make sure that
only valid BOMs are present as JSON files in that directory.

The complete command could look like:

```bash
mdb generate --input ./my-boms --output 3rd-party.md --template template.md.jinja
```

## Filtering specific types

In case you are using multiple BOM files, coming from different ecosystems, you can 
apply a filter, via the `--type` option, which will only return information which matches the specified type.

The complete command could look like:

```bash
mdb generate --input ./my-boms --output 3rd-party.md --template template.md.jinja --type pypi
```

## Supported package managers 

Currently, MdBOM supports the following package manager types:

- pypi
- npm 
- golang

