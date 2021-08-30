# How to generate a markdown file

You need a template file for generating a markdown file. 
You can have a look at the [examples](https://github.com/HaRo87/mdbom/tree/develop/examples)
provided by the MdBOM project. 

Once you have a template and a BOM you should be able to generate
a markdown file via

```bash
mdb generate --input bom.json --output 3rd-party.md --template template.md.jinja --type pypi
```

This will take the "bom.json" file as input, collect all relevant information and 
use the "template.md.jinja" template to generate the "3rd-party.md" file.

Currently, MdBOM does support the following two BOM types via the "--type" option:

- pypi
- npm 