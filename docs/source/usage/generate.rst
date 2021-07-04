===============================
How to generate a markdown file
===============================

You need a template file for generating a markdown file. 
You can have a look at the `examples <https://github.com/HaRo87/mdbom/tree/develop/examples>`_
provided by the MdBOM project. 

Once you have a template and a BOM you should be able to generate
a markdown file via::

    mdb generate --input bom.json --output 3rd-party.md --template template.md.jinja

This will take the "bom.json" file as input, collect all relevant information and 
use the "template.md.jinja" template to generate the "3rd-party.md" file.

The default "processor" used for processing BOM information can deal with
Python, or to be more specific PyPi packages. But you can also specify a
different processor by using the "--type" option::

    mdb generate --input bom.json --output 3rd-party.md --template template.md.jinja --type npm
