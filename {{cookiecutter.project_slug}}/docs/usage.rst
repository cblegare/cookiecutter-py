=====
Usage
=====

As a python library
-------------------

To use {{ cookiecutter.project_name }} in a project::

    import {{ cookiecutter.project_slug }}

{% if cookiecutter.use_flask == 'y' -%}
As a flask application
----------------------

You can create a flask application with the
`{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}.web.create_app()`
function.

{% endif -%}
