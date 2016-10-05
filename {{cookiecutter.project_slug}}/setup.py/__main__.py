#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


"""
Setup script
"""


from pathlib import Path
from functools import lru_cache as cached
import distutils.cmd
import distutils.log
import setuptools
from typing import *
import venv


PROJECT_ROOT = Path(__file__).parent.parent


_cmdclasses = {}


def cmdclass(cls: type) -> type:
    global _cmdclasses

    _cmdclasses[str(cls.__name__).lower()] = cls

    return cls


def cmdclasses():
    return _cmdclasses


def setup():
    profile = {
        "name": "{{cookiecutter.project_slug}}",
        "description": "{{cookiecutter.project_short_description}}",
        "long_description": str(long_description()),
        "url": "{{cookiecutter.project_url}}",
        "license": "{{cookiecutter.project_license}}",
        "classifiers": [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
        ],
        "keywords": '',
        "packages": setuptools.find_packages(exclude=['doc', 'test*']),
        "include_package_data": True,
        "entry_points": {
            'console_scripts': [
                '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.__main__:main'
            ]
        },
        "author": 'Charles Bouchard-Légaré',
        "install_requires": list(install_requires()),
        "setup_requires": ['pytest', 'pytest-runner'],
        "tests_require": ['pytest', 'pytest-cookies'],
        "dependency_links": list(dependency_links()),
        "author_email": 'cblegare.atl@ntis.ca',
        "version": str(version()),
        "cmdclass": dict(cmdclasses())
    }

    url_pass = {
        "download_url": "{!s}/tarball/{!s}".format(profile["url"],
                                                   profile["version"])
    }

    from collections import ChainMap

    config = ChainMap({}, profile, url_pass)

    setuptools.setup(
        **config
    )


def version():
    return "1.0"


@cached()
def long_description():
    return ""


@cached()
def install_requires():
    return []


@cached()
def dependency_links():
    return []


@cmdclass
class Venv(distutils.cmd.Command):
    """
    Setup venvs for development or production
    """

    description = 'bake some venv'
    user_options = [
        # The format is (long option, short option, description).
        ('deps=', None, 'path to requirements.txt'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.deps = ''

    def finalize_options(self):
        """Post-process options."""
        if self.deps:
            deps = Path(str(self.deps))
            assert deps.exists(), ('Pylint config file %s does not exist.'.format(deps))

    def run(self):
        """Run command."""
        self.announce(
            'Running command: venv',
            level=distutils.log.INFO)
        venv.EnvBuilder(clear=True, with_pip=True).create("venv")


def main():
    setup()


if __name__ == "__main__":
    main()
