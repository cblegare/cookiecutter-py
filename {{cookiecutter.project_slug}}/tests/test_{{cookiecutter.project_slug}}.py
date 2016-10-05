#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_{{cookiecutter.project_slug}}
----------------------------------

Tests for `{{cookiecutter.project_slug}}` module.
"""


import pytest

from click.testing import CliRunner

from {{cookiecutter.project_slug}} import __main__


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


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
    assert '{{cookiecutter.project_slug}}.__main__.main' in result.output
    help_result = runner.invoke(__main__.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
