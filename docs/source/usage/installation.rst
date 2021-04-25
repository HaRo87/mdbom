======================
How to install MdBOM
======================

This page describes how to install MdBOM. 

MdBOM requires Python 3.8 or above.

To install Python 3.8, I recommend using `Anaconda <https://www.anaconda.com>`_.

First, you should create a new environment::

    conda create -n mdb python=3.8

Then you need to make sure to activate it::

    conda activate mdb

Now you can install MdBOM via::

    pip install mdbom

If you want to check your installation you can run::

    mdb info

which should produce an output similar to::

    Check the documentation: https://haro87.github.io/mdbom/
    for further information.

