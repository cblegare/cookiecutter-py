

.. image:: https://travis-ci.org/cblegare/pythontemplate.svg?branch=master
   :target: https://travis-ci.org/cblegare/pythontemplate
   :alt: Build Status
.. image:: https://readthedocs.org/projects/cblegarepythontemplate/badge/?version=latest
   :target: http://cblegarepythontemplate.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Cookiecutter_ template for a Python package.

GitHub repo:
   https://github.com/cblegare/cookiecutter-py/
Documentation:
   https://cblegarepythontemplate.readthedocs.io
Free software:
   GNU General Public License v3

Features
--------

* Testing setup with ``unittest`` and ``python setup.py test`` or ``py.test``
* Tox_ testing: Setup to easily test for Python 3.5 (WIP)
* Sphinx_ docs: Documentation ready for generation with, for example,
  ReadTheDocs_
* Command line interface using Click_
* Support for implicit namespaces from `PEP420`_
* Gets you started for a web application (optional)

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _PEP420: https://www.python.org/dev/peps/pep-0420/
.. _Click: http://click.pocoo.org/


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

.. warning:: Be carefull with namespace packages using the
   `implicit namespace`_ mechanism. Some tools are not fully compliant yet.

Namespace package and editable installations should be fixed with
`setuptools 31`_ and Python 3.5:

- https://github.com/pypa/packaging-problems/issues/12
- https://github.com/pypa/setuptools/pull/789
- https://github.com/pypa/setuptools/issues/250
- https://github.com/pypa/setuptools/issues/513
- https://github.com/pypa/pip/issues/3

You may also have issues with imports from external tools.   Most of them are
or will be fixed in with `sphinx 1.5`_, `pytest 2.5`_ and `pylint 2.0`_ (not
released yet).

- https://github.com/sphinx-doc/sphinx/issues/1500
- https://github.com/pytest-dev/pytest/issues/1567
- https://github.com/pytest-dev/pytest/pull/1568
- https://github.com/PyCQA/pylint/issues/842

Using latest versions, only pylint_ still has issues with implicit namespaces
at the time of this writing.

.. _`implicit namespace`: https://www.python.org/dev/peps/pep-0420/
.. _`setuptools 31`: http://setuptools.readthedocs.io/en/latest/history.html#v31-0-0
.. _`sphinx 1.5`: http://www.sphinx-doc.org/en/1.5.1/changes.html#release-1-5-released-dec-5-2016
.. _`pytest 2.5`: http://doc.pytest.org/en/latest/changelog.html#id149
.. _`pylint 2.0`: https://github.com/PyCQA/pylint/milestone/2
.. _pylint: https://www.pylint.org/


Fork This / Create Your Own
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

.. note:: It's up to you whether or not to rename your fork/own version. Do
   whatever you think sounds good.

Or Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.  Read on in the :ref:`contributing`
section.


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