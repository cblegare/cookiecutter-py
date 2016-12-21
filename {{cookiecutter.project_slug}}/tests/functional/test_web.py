#!/usr/bin/env python
# coding: utf8


"""Tests for `{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}.cli` module."""


import pytest

from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %} import web


@pytest.fixture
def web_app():
    app = web.create_app()
    return app


@pytest.fixture
def client(web_app):
    new_client = web_app.test_client()
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


{% if cookiecutter.make_rest_api == 'y' -%}
def test_api_get(client):
    rv = client.get('/api/myresource/')
    assert rv.status_code == 200, 'GET api with arg responds "OK"'
    assert 'hello world' in rv.data.decode(), 'api responded as expected'


def test_api_post(client):
    rv = client.post('/api/myresource/')
    assert rv.status_code == 202, 'GET api with arg responds "Accepted"'
    assert 'hello world' in rv.data.decode(), 'api responded as expected'
{% endif -%}
