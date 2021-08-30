# How to install MdBOM

This page describes how to install MdBOM. 

MdBOM requires Python 3.8 or above.

To install Python 3.8, I recommend using [Anaconda](https://www.anaconda.com).

First, you should create a new environment

```bash
conda create -n mdb python=3.8
```

Then you need to make sure to activate it

```bash
conda activate mdb
```

Now you can install MdBOM via

```bash
pip install mdbom
```

If you want to check your installation you can run

```bash
mdb info
```

which should produce an output similar to

```bash
Check the documentation: https://haro87.github.io/mdbom/
for further information.
```