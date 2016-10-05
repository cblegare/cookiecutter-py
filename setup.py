#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


"""
Setup script
"""


import contextlib
import os
from pathlib import Path
from setuptools import setup
from setuptools import Command


PROJECT_DIRECTORY = Path(__file__).parent


class Cookiecutter(Command):
    """
    Bake the cookies
    """

    description = 'bake my cookies'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        from cookiecutter.main import cookiecutter
        cookiecutter(".", overwrite_if_exists=True, output_dir="build")


class Documentation(Command):
    """
    Bake the cookies
    """

    description = 'bake my docs'
    user_options = [
        ('sphinx-target=', None, 'documentation output format'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.sphinx_target = "html"

    def finalize_options(self):
        possible_target = [
            "html", "dirhtml", "singlehtml", "pickle", "json", "htmlhelp",
            "qthelp", "applehelp", "devhelp", "epub", "latex", "latexpdf",
            "latexpdfja", "text", "man", "texinfo", "info", "gettext",
            "changes", "xml", "pseudoxml", "linkcheck", "doctest", "coverage",
        ]
        assert self.sphinx_target in possible_target

    def run(self):
        """Run command."""
        import subprocess
        import shlex
        project_directory = Path(__file__).parent
        build_directory = project_directory / "build" / "docs"
        dist_directory = project_directory / "dist" / "docs"
        build_directory.mkdir(exist_ok=True, parents=True)
        dist_directory.mkdir(exist_ok=True, parents=True)
        build_directory = build_directory.resolve()
        dist_directory = dist_directory.resolve()
        print(build_directory.resolve(), dist_directory)
        command = "make BUILDDIR={!s} clean {!s}".format(build_directory,
                                                         self.sphinx_target)
        with working_directory(PROJECT_DIRECTORY / "docs"):
            print(command)
            subprocess.Popen(shlex.split(command)).wait()
        expected_output = build_directory / self.sphinx_target
        expected_output.replace(dist_directory / self.sphinx_target)


def main():
    setup(
        name='cookiecutter-py',
        packages=[],
        version='0.1.0',
        description='Cookiecutter template for a Python package',
        author='Charles Bouchard-Légaré',
        license='GNU General Public License v3',
        author_email='cblegare.atl@ntis.ca',
        url='https://github.com/abstrus/cookiecutter-py',
        setup_requires=['pytest-runner'],
        tests_require=['pytest', 'pytest-cookies', 'sphinx'],
        cmdclass={
            "cookiecutter": Cookiecutter,
            "docs": Documentation
        },
        keywords=['cookiecutter', 'template', 'package', ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Software Development',
        ],
    )


@contextlib.contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(str(prev_cwd))


if __name__ == "__main__":
    main()