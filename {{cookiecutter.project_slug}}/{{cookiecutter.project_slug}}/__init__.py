#!/usr/bin/python3.5
# coding: utf8


"""
Package main definition
"""


from pkg_resources import get_distribution, DistributionNotFound


__project__ = '{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}'
__version__ = None  # required for initial installation

try:
    distribution = get_distribution(__project__)
    __version__ = distribution.version

except DistributionNotFound:
    # This will happen if the package is not installed.
    # For more informations about development installation, read about
    # the 'develop' setup.py command or the '--editable' pip option.
    # Note that development installations may break other packages from
    # the same implicit namespace
    # (see https://github.com/pypa/packaging-problems/issues/12)
    __version__ = "(local)"
else:
    pass
    # make shortcut import here

