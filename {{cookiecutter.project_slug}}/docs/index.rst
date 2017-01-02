.. {{ cookiecutter.project_slug }} documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
{% set is_open_source = cookiecutter.project_license != 'Not open source' -%}
{% set title = "Welcome to " + cookiecutter.project_name + "'s documentation!" %}
{{ title }}
{% for n in range(title|length) %}={% endfor %}

.. include:: ../README.rst

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


Development resources
=====================

.. toctree::
   :maxdepth: 2

   setup_script
   testing
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
