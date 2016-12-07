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


@pytest.fixture
def client(app):
    new_client = app.test_client()
    return new_client


def test_web_get_root_is_ok(client):
    rv = client.get('/')
    assert rv.status_code == 200, 'GET root route '


def test_web_get_greetings_is_ok(client):
    rv = client.get('/greetings')
    assert rv.status_code == 404, 'GET greetings without arg does not exists'


def test_web_get_greetings_with_name(client):
    rv = client.get('/greetings/John')
    assert rv.status_code == 200, 'GET greetings with arg responds "OK"'
    assert 'Hello John!' in rv.data.decode(), 'greetings responded as expected'


def test_web_get_greetings_with_name_and_formal_style(client):
    rv = client.get('/greetings/John?style=formal')
    assert rv.status_code == 200, 'GET greetings with arg responds "OK"'
    assert 'Good evening John' in rv.data.decode(), (''
        'greetings responded as expected')


def test_web_get_greetings_with_name_and_slang_style(client):
    rv = client.get('/greetings/John?style=slang')
    assert rv.status_code == 200, 'GET greetings with arg responds "OK"'
    assert 'Yo !!1 John!' in rv.data.decode(), 'greetings responded as expected'
