======================
Cookiecutter PyPackage
======================

Cookiecutter_ template for a Python package.

* GitHub repo: https://github.com/cblegare/cookiecutter-py/
* Free software: GNU General Public License v3

Features
--------

* Testing setup with ``unittest`` and ``python setup.py test`` or ``py.test``
* Tox_ testing: Setup to easily test for Python 3.5 (WIP)
* Sphinx_ docs: Documentation ready for generation with, for example,
  ReadTheDocs_
* Command line interface using Click
* Support for implicit namespaces from `PEP420`_
* Gets you started for a web application (optional)

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _PEP420: https://www.python.org/dev/peps/pep-0420/


Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/cblegare/cookiecutter-py.git

Then:

* Create a repo and put it there.
* Install the dev requirements into a virtualenv.
  (``pip install -r requirements/dev.txt``)
* Edit the `requirements.txt` file that specifies the packages you will need
  for your project and their versions. For more info see the
  `pip docs for requirements files`_.

.. _`pip docs for requirements files`: https://pip.pypa.io/en/stable/user_guide/#requirements-files


Known issues
~~~~~~~~~~~~

Be carefull with namespace packages using the `implicit namespace`_
mechanism. Most projects managed by the Python Packaging Authority are
not fully compliant yet.

- https://github.com/pypa/packaging-problems/issues/12
- https://github.com/pypa/setuptools/pull/789
- https://github.com/pypa/setuptools/issues/250
- https://github.com/pypa/setuptools/issues/513
- https://github.com/pypa/pip/issues/3

You may also have issues with imports with sphinx, pytest or pylint.

- https://github.com/sphinx-doc/sphinx/issues/1500
- https://github.com/pytest-dev/pytest/issues/1567
- https://github.com/pytest-dev/pytest/pull/1568
- https://github.com/PyCQA/pylint/issues/842

.. _`implicit namespace`: https://www.python.org/dev/peps/pep-0420/


Fork This / Create Your Own
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

* It's up to you whether or not to rename your fork/own version. Do whatever
  you think sounds good.

Or Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.


.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _Bumpversion: https://github.com/peritus/bumpversion
.. _PyPi: https://pypi.python.org/pypi

.. _`Nekroze/cookiecutter-pypackage`: https://github.com/Nekroze/cookiecutter-pypackage
.. _`tony/cookiecutter-pypackage-pythonic`: https://github.com/tony/cookiecutter-pypackage-pythonic
.. _`ardydedase/cookiecutter-pypackage`: https://github.com/ardydedase/cookiecutter-pypackage
.. _github comparison view: https://github.com/tony/cookiecutter-pypackage-pythonic/compare/audreyr:master...master
.. _`network`: https://github.com/audreyr/cookiecutter-pypackage/network
.. _`family tree`: https://github.com/audreyr/cookiecutter-pypackage/network/members