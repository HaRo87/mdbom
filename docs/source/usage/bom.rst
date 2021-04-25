======================
How to generate a BOM
======================

You can use a tool like `cyclonedx-bom <https://pypi.org/project/cyclonedx-bom/>`_.

.. important:: Do not install this tool inside the same environment.

After successfully installing it, you need to run:

.. code-block::
    pip freeze > requirements.txt

Then, you can generate a BOM via:

.. code-block::
    cyclonedx-py -o bom.json -j

MdBOM can work with the generated BOM.