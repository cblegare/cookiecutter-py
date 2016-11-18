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


from contextlib import contextmanager
import importlib.util
import os
import subprocess
import shlex
import sys

from cookiecutter.utils import rmtree

import importlib


default_context = {
    "project_slug": "projectslug"
}


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
        with inside_dir(project.project_path):
            yield project
    finally:
        rmtree(str(result.project))


def test_project_metadata_has_a_name(cookies):
    """A default ProjectMetadata instance has a name -> str"""
    with baked_project(cookies, {"project_slug": "slug",
                                 "namespace": "ns"}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert isinstance(project_metadata.name, str)


def test_project_name_prefixed_by_namespace(cookies):
    """A ProjectMetadata include namespace in name"""
    with baked_project(cookies, {"project_slug": "slug",
                                 "namespace": "ns"}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert project_metadata.name == "ns.slug"


def test_project_name_supports_long_namespace(cookies):
    """A ProjectMetadata supports long namespaces in name"""
    with baked_project(cookies, {"project_slug": "slug",
                                 "namespace": "ns.long"}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert project_metadata.name == "ns.long.slug"


def test_project_metadata_has_a_short_description(cookies):
    """A ProjectMetadata description comes from context"""
    with baked_project(cookies,
                       {"project_short_description": "Descr"}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert project_metadata.description == "Descr"


def test_project_metadata_has_a_version(cookies):
    """A default ProjectMetadata instance has a version"""
    with baked_project(cookies, {}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert project_metadata.version is not None


def test_project_metadata_has_packages(cookies):
    """A default ProjectMetadata instance has packages"""
    with baked_project(cookies, {}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert project_metadata.packages


def test_project_metadata_with_namespace_has_packages(cookies):
    """A default ProjectMetadata instance has sub-packages under namespace"""
    with baked_project(cookies, {"project_slug": "slug",
                                 "namespace": "ns"}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert "ns" in project_metadata.packages
        assert "ns.slug" in project_metadata.packages


def test_project_metadata_supports_deep_packages(cookies):
    """
    A default ProjectMetadata instance for multiple namespace layers has
    nested packages
    """
    with baked_project(cookies, {"project_slug": "slug",
                                 "namespace": "alpha.beta.gamma"}) as project:
        project_metadata = project.setup_module.ProjectMetadata()
        assert "alpha" in project_metadata.packages
        assert "alpha.beta" in project_metadata.packages
        assert "alpha.beta.gamma" in project_metadata.packages
        assert "alpha.beta.gamma.slug" in project_metadata.packages


def test_docs_command(cookies):
    """
    Documentation should build without error
    """
    with baked_project(cookies, {}) as project:
        docs_command = "{!s} setup.py docs".format(sys.executable)
        subprocess.check_call(shlex.split(docs_command))
        print("test_docs_command path",
              str(project.project_path))


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory.

    Example usage:

    .. code-block::

        >>> with inside_dir("tests"):
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
