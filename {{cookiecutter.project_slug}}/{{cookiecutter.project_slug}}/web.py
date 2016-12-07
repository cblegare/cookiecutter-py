#!/usr/bin/python3
# coding: utf8


"""Cookiecutter template tests."""

from flask import Blueprint, Flask, request

from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %} import greetings

{{ cookiecutter.project_slug }} = Blueprint('greeting_page', __name__)

all_blueprints = [{{ cookiecutter.project_slug }}]


@{{ cookiecutter.project_slug }}.route('/')
def root_view():
    """Trivial root resource."""
    return ''


@{{ cookiecutter.project_slug }}.route('/greetings/<person>')
def greetings_view(person='World!'):
    """Provide the greeting resource."""
    style = request.args.get('style', None)

    if style == 'slang':
        message = str(greetings.Slang(person))
    elif style == 'formal':
        message = str(greetings.Formal(person))
    else:
        message = str(greetings.Greetings(person))

    return message


def create_app():
    """Create a new Flask web application and returns it."""
    app = Flask(__name__)
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
    return app
