#!/usr/bin/python3
# coding: utf8


"""Unit tests for the `{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}.greetings` module."""


from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %} import greetings


def test_formal():
    assert 'Good evening John' == str(greetings.Formal('John'))


def test_slang():
    assert 'Yo !!1 John!' == str(greetings.Slang('John'))
