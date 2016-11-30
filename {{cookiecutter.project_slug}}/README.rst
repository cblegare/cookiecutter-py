{% set is_open_source = cookiecutter.project_license != 'Not open source' -%}

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
{% endif %}


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `abstrus/cookiecutter-py`_
project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`abstrus/cookiecutter-py`: https://github.com/abstrus/cookiecutter-py
