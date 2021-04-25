======================
How to install MdBOM
======================

This page describes how to install MdBOM. 

MdBOM requires Python 3.8 or above.

To install Python 3.8, I recommend using `Anaconda <https://www.anaconda.com>`.

First, you should create a new environment:

.. code-block::
    conda create -n mdb python=3.8

Then you need to make sure to activate it:

.. code-block::
    conda activate mdb

Now you can install MdBOM via:

.. code-block::
    pip install mdbom

If you want to check your installation you can run:

.. code-block::
    mdb info

which should produce an output similar to:

.. code-block::
    Check the documentation: https://haro87.github.io/mdbom/
    for further information.

