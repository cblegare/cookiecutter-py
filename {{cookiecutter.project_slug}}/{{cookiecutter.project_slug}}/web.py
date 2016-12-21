#!/usr/bin/python3
# coding: utf8


"""Cookiecutter template tests."""

from flask import Blueprint, Flask, request
{% if cookiecutter.make_rest_api == 'y' -%}
from flask_ripozo import FlaskDispatcher
from ripozo.decorators import apimethod
from ripozo.adapters import SirenAdapter, HalAdapter
from ripozo.resources import ResourceBase
{% endif -%}

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


{% if cookiecutter.make_rest_api == 'y' -%}
class HelloWorldViewset(ResourceBase):
    resource_name = 'myresource'  # The name of the resource.  This will be
                                  # appended to the _namespace to complete
                                  # the url.

    # The decorator indicates that the base url will be used
    # and that it will be registered for GET requests
    # a GET request to /api/myresource would be dispatched to this
    # method and handled here
    @apimethod(methods=['GET'])
    def hello(cls, request, *args, **kwargs):
        faked_response_properties = {'content': 'hello world'}
        return cls(properties=faked_response_properties)

    @apimethod(methods=['POST'])
    def post_hello(cls, request, *args, **kwargs):
        faked_response_properties = {'content': 'hello world'}
        return cls(properties=faked_response_properties, status_code=202)


def create_app():
    # Create the flask application
    app = Flask(__name__)
    api_blueprint = Blueprint('hello_api', __name__)

    # Create the dispatcher
    dispatcher = FlaskDispatcher(api_blueprint, url_prefix='/api')

    # Specify the valid response types
    dispatcher.register_adapters(SirenAdapter, HalAdapter)

    # This will register all of the apimethod decorated methods in
    # this class specified.  In this case it adds the /api/myresource GET
    # route to the application
    dispatcher.register_resources(HelloWorldViewset)
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    app.register_blueprint(api_blueprint)

    return app
{% else -%}
def create_app():
    """Create a new Flask web application and returns it."""
    app = Flask(__name__)
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
    return app
{% endif -%}
