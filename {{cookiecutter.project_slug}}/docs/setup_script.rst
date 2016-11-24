.. _setup:


setup module
============


The *setup.py* file is a swiss knife for various tasks.


making a virtual python environment
-----------------------------------

Start by creating a virtual python environment::

    $ python setup.py venv

You now can use this isolated clean python environment::

    $ bin/python --version
    Python 3.5.2

You may also activate it for the current shell.  POSIX shells would use::

    $ . bin/activate

running tests
-------------

We use `py.test`_ for running tests because it is amazing.  Run it by invoking
the simple *test* alias of *setup.py*::

    $ bin/python setup.py test


.. _py.test: http://doc.pytest.org/en/latest/

building source distirbutions
-----------------------------

Standard *sdist* is supported::

    $ bin/python setup.py sdist


building binary distributions
-----------------------------

Use the `wheel distribution standard`_::

    $ bin/python setup.py bdist_wheel

.. _wheel distribution standard: http://pythonwheels.com/


building html documentation
---------------------------

First, make sure to have the technical writer's requiments::

    $ bin/python -m pip install -r requirements/_docs.txt

Then, use *setup.py* to build the documentation::

    $ bin/python setup.py docs

A `make`_ implementation is not required on any platform.

.. _make: https://www.gnu.org/software/make/
