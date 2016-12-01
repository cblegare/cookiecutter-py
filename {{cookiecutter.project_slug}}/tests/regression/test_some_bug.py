#!/usr/bin/python3
# coding: utf8


"""Non-regression tests for the `{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}.greetings` module."""


import {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}


def test_example():
    pass
