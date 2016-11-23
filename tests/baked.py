#!/usr/bin/python3.5
# coding: utf8


"""
Tests for the generated setup.py script


The generated setup script was once generated as a package.  That is a
directory named ``setup.py`` with a ``__main__.py`` and a ``__init__.py``
files in it.


It is now known that the python packaging infrastructure will not support
this invocation scheme. See the
`pull request https://github.com/pypa/python-packaging-user-guide/pull/270`_
on the subject.
"""


import os
import importlib.util
from contextlib import contextmanager

from cookiecutter.utils import rmtree


class BakedProject(object):
    def __init__(self, context: dict, baked_cookies, setup_module):
        self.context = context
        self.project_path = baked_cookies.project
        self.setup_module = setup_module


@contextmanager
def baked_project(cookies, ctx):
    """
    Delete the temporal directory that is created when executing the
    tests

    :param cookies: pytest_cookies.Cookies, cookie to be baked and its
                    temporal files will be removed
    :param ctx:
    :return:
    """
    result = cookies.bake(extra_context=ctx)
    module_path = os.path.join(str(result.project), 'setup.py')
    module_name = 'setup'

    spec = importlib.util.spec_from_file_location(module_name,
                                                  module_path)
    setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup)

    try:
        project = BakedProject(ctx, result, setup)
        with _inside_dir(project.project_path):
            yield project
    finally:
        rmtree(str(result.project))


@contextmanager
def _inside_dir(dirpath):
    """
    Execute code from inside the given directory.

    Example usage:

    .. code-block::

        >>> with _inside_dir("tests"):
        ...    for filename in os.listdir(os.getcwd()):
        ...        print(filename)
        test_bake.py

    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(str(dirpath))
        yield
    finally:
        os.chdir(old_path)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)
