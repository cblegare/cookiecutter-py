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


import subprocess
import shlex
import sys

from baked import baked_project

default_context = {
    "project_slug": "projectslug"
}


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


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)