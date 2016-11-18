.. {{ cookiecutter.project_slug }} documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
{% set is_open_source = cookiecutter.project_license != 'Not open source' -%}
{% set title = "Welcome to " + cookiecutter.project_name + "'s documentation!" %}
{{ title }}
{% for n in range(title|length) %}={% endfor %}

{% if is_open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

.. image:: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg
     :target: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/
     :alt: Updates


{{ cookiecutter.project_short_description }}


{% if is_open_source %}
{{ cookiecutter.project_name }} is free software and licensed under the
{{ cookiecutter.project_license}}.  See :ref:`license` for details.

* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{% endif %}


Contents:

.. toctree::
   :maxdepth: 2

   installation
   usage


Project Information
===================

.. toctree::
   :maxdepth: 2

   contributing
   history
   license
   {% if cookiecutter.create_author_file == 'y' %}authors{% endif %}


API Documentation
=================

.. toctree::
   :maxdepth: 2

   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
