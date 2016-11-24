#!/usr/bin/python3
# coding: utf8


"""Cookiecutter template tests."""


from pathlib import Path
import sys

if __name__ == '__main__' and not __package__:
    # This should never happen when installed from pip (setup.py).
    # This workaround is NOT bulletproof, rather brittle as many edge
    # cases are not covered
    # See http://stackoverflow.com/a/28154841/2479038
    distance = len(Path(sys.argv[0]).parts)
    top = Path(__file__).resolve().parents[distance]

    print('warning: running package directly, risking ImportError',
          file=sys.stderr)
    print('Simulating installation by adding {!s} to sys.path'.format(top),
          file=sys.stderr)

    sys.path.append(str(top))

    py = sys.executable
    print('To prevent this, run this script as a module:',
          file=sys.stderr)
    print('    {!s} -m {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}'.format(py),
          file=sys.stderr)
    print('Or install it beforehand using setuptools (or pip):',
          file=sys.stderr)
    print('    {!s} -m pip install {{ cookiecutter.project_slug }}'.format(py),
          file=sys.stderr)

from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %} import __project__  # noqa
from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}. cli import main  # noqa

if __name__ == '__main__':
    main(prog_name=__project__)
