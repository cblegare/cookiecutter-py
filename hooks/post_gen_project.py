#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


"""
cookiecutter hook after generation
"""


import fnmatch
import os


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def find_files(directory, pattern):
    """Generate file names matching pattern recursively found in directory."""
    for root, dirs, files in os.walk(str(directory)):
        for basename in files:
            if fnmatch.fnmatch(basename, str(pattern)):
                filename = os.path.join(root, basename)
                yield filename


def find_files_in_patterns(directory, patterns):
    for pattern in patterns:
        yield from find_files(directory, pattern)


if __name__ == '__main__':
    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if '{{ cookiecutter.use_flask }}' != 'y':
        flask_patterns = ['*web.py']
        flask_files = find_files_in_patterns(PROJECT_DIRECTORY, flask_patterns)
        for flask_file in flask_files:
            remove_file(flask_file)

    if 'Not open source' == '{{ cookiecutter.project_license }}':
        remove_file('LICENSE')

    namespace = '{{ cookiecutter.namespace }}'
    source_dir = '{{ cookiecutter.project_slug }}'
    if namespace:
        parts = namespace.split(".")
        os.makedirs(os.path.join(*parts), exist_ok=True)
        os.rename(source_dir, os.path.join(*parts, source_dir))
