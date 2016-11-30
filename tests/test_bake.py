#!/usr/bin/python3.5
# coding: utf8


from collections import OrderedDict
from contextlib import contextmanager
import copy
import datetime
import os
import pip
import pytest
import subprocess
import sys
import shlex

from cookiecutter.utils import rmtree
from click.testing import CliRunner

if sys.version_info > (3, 0):
    import importlib
else:
    import imp


CONTEXTS = OrderedDict(
    trivial={'namespace': ''},
    namespace={'namespace': 'namespace'},
    special_chars={'namespace': '',
                   'full_name': 'name "quote" name'}
)


@pytest.fixture(scope="function",
                params=CONTEXTS.values(),
                ids=list(CONTEXTS.keys()))
def context(request):
    yield copy.copy(request.param)


def test_bake_with_defaults(cookies, context):
    """
    Project is a directory and contains some specific top level files.

    :param cookies:
    :param context:
    :return:
    """

    with bake_in_temp_dir(cookies, extra_context=context) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'setup.py' in found_toplevel_files
        assert 'tests' in found_toplevel_files


def test_bake_and_run_tests(cookies, context):
    """
    Generated setup.py tests run just fine

    :param cookies:
    :param context:
    :return:
    """
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        assert result.project.isdir()
        run_inside_dir('python setup.py test', str(result.project)) == 0


def test_bake_and_check_style(cookies, context):
    """
    Generated setup.py flake8 runs just fine

    :param cookies:
    :param context:
    :return:
    """
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        assert result.project.isdir()
        run_inside_dir('python setup.py lint', str(result.project)) == 0


def test_bake_without_author_file(cookies, context):
    """
    Make sure no author file exists if specified in context

    :param cookies:
    :param context:
    :return:
    """
    context.update({'create_author_file': 'n'})
    with bake_in_temp_dir(cookies, extra_context=context) as result:

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'AUTHORS.rst' not in found_toplevel_files
        doc_files = [f.basename for f in result.project.join('docs').listdir()]
        assert 'authors.rst' not in doc_files

        # Assert there are no spaces in the toc tree
        docs_index_path = result.project.join('docs/index.rst')
        with open(str(docs_index_path)) as index_file:
            assert 'contributing\n   history' in index_file.read()

        # Check that
        manifest_path = result.project.join('MANIFEST.in')
        with open(str(manifest_path)) as manifest_file:
            assert 'AUTHORS.rst' not in manifest_file.read()


def test_bake_selecting_license(cookies, context):
    license_strings = {
        'MIT license': 'MIT ',
        'BSD license': 'Redistributions of source code must retain the above copyright notice, this',
        'ISC license': 'ISC License',
        'Apache Software License 2.0': 'Licensed under the Apache License, Version 2.0',
        'GNU General Public License v3': 'GNU GENERAL PUBLIC LICENSE',
    }
    for name, target_string in license_strings.items():
        context['project_license'] = name
        with bake_in_temp_dir(cookies, extra_context=context) as result:
            assert target_string in result.project.join('LICENSE').read()
            assert name in result.project.join('setup.py').read()


def test_bake_not_open_source(cookies, context):
    context.update({'project_license': 'Not open source'})
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'setup.py' in found_toplevel_files
        assert 'LICENSE' not in found_toplevel_files
        assert 'License' not in result.project.join('README.rst').read()


def test_bake_with_console_script_files(cookies, context):
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        project_path, project_slug, project_dir = project_info(result, context)
        print(project_path, project_slug, project_dir)
        found_project_files = os.listdir(project_dir)
        assert "__main__.py" in found_project_files
        assert "cli.py" in found_project_files
        assert "greetings.py" in found_project_files

        setup_path = os.path.join(project_path, 'setup.py')
        with open(setup_path, 'r') as setup_file:
            assert 'entry_points' in setup_file.read()


@pytest.mark.skip(reason="could not import entry point that makes absolute "
                         "imports with importlib")
def test_bake_with_console_script_cli(cookies, context):
    with bake_and_install(cookies) as result:
        project_path, project_slug, project_dir = project_info(result, context)
        module_path = os.path.join(project_dir, 'cli.py')
        module_name = '.'.join([project_slug, 'cli'])
        if sys.version_info >= (3, 5):
            spec = importlib.util.spec_from_file_location(module_name,
                                                          module_path)
            cli = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cli)
        elif sys.version_info >= (3, 3):
            file_loader = importlib.machinery.SourceFileLoader
            cli = file_loader(module_name, module_path).load_module()
        else:
            cli = imp.load_source(module_name, module_path)
        runner = CliRunner()
        noarg_result = runner.invoke(cli.main)
        assert noarg_result.exit_code == 0
        noarg_output = ' '.join(['Replace this message by putting your code into',
                                 project_slug])
        assert noarg_output in noarg_result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message' in help_result.output


def test_year_compute_in_license_file(cookies, context):
    """
    The LICENSE file at the root for generated project contains the
    current date

    :param cookies:
    :return:
    """
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        license_file_path = result.project.join('LICENSE')
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result, actual_context=None):
    """
    Get toplevel dir, project_slug, and project dir from baked cookies

    :param result:
    :return:
    """
    if actual_context is None:
        actual_context = {}

    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    namespace = actual_context.get("namespace", None)

    if namespace:
        project_dir = os.path.join(project_path, namespace, project_slug)
    else:
        project_dir = os.path.join(project_path, project_slug)

    return project_path, project_slug, project_dir


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
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the
    tests

    :param cookies: pytest_cookies.Cookies, cookie to be baked and its
                    temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


@contextmanager
def bake_and_install(cookie, *args, **kwargs):
    actual_context = kwargs.get("extra_context", {})
    with bake_in_temp_dir(cookie, *args, **kwargs) as result:
        project_path, project_slug, project_dir = project_info(result, actual_context)
        pip.main(['install', '--upgrade', '--editable', str(project_path)])
        yield result
        pip.main(['uninstall', project_slug])


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit
    status

    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being
                    run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the command
    output

    :param command:
    :param dirpath:
    :return:
    """
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)
