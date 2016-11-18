#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


"""
cookiecutter hook after generation
"""


import os


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':
    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if 'Not open source' == '{{ cookiecutter.project_license }}':
        remove_file('LICENSE')

    namespace = '{{ cookiecutter.namespace }}'
    source_dir = '{{ cookiecutter.project_slug }}'
    if namespace:
        parts = namespace.split(".")
        os.makedirs(os.path.join(*parts), exist_ok=True)
        os.rename(source_dir, os.path.join(*parts, source_dir))
