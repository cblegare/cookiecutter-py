#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_{{cookiecutter.project_slug}}
----------------------------------

Tests for `{{cookiecutter.project_slug}}` module.
"""


import pytest

from click.testing import CliRunner

from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %} import cli


@pytest.fixture
def some_string():
    """
    Sample pytest fixture.

    See more at: `http://doc.pytest.org/en/latest/fixture.html`
    """
    return "some_string"


def test_content(some_string: str):
    """
    Sample pytest test function with the pytest fixture as an argument.
    """
    assert some_string.upper() == "SOME_STRING"


def test_command_line_help():
    """
    Make sure the command line help message works and contains the project's
    name
    """
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--help'])
    assert result.exit_code == 0
    expected = (
        '{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}',
        '--help',
        'Show this message and exit.'
    )
    assert all(x in result.output for x in expected)

def test_command_line_version():
    """
    The command line should provide the version number
    """
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--version'])
    assert result.exit_code == 0
    expected = (
        ', version'
    )
    assert expected in result.output

def test_command_line_greet():
    """
    The sub-command 'greet' works and outputs its message
    """
    runner = CliRunner()
    result = runner.invoke(cli.main, ['greet'])
    assert result.exit_code == 0
    expected = (
        'Hello World!',
    )
    assert all(x in result.output for x in expected)
