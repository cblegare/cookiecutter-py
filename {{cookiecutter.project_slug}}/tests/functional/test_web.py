#!/usr/bin/env python
# coding: utf8


"""Tests for `{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}.cli` module."""


import flask
import pytest

from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %} import web


@pytest.fixture
def app():
    app = web.create_app()
    return app


def test_app(app):
    assert isinstance(app, flask.Flask)
