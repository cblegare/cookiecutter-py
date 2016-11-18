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

    description = 'bake the cookiecutter'
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

    description = 'create documentation distribution'
    user_options = [
        ('builder=', None, 'documentation output format'
                                 ' [default: html]'),
        ('paper=', None, 'paper format [default: letter]'),
        ('dist-dir=', None, 'directory to put final built distributions in'
                            ' [default: dist/docs]'),
        ('build-dir=', None, 'temporary directory for creating the distribution'
                            ' [default: build/docs]'),
        ('src-dir=', None, 'documentation source directory'
                           ' [default: docs'),
    ]

    targets = {
        "html": {
            "comment": "The HTML pages are in {build_dir!s}.",
        },
        "dirhtml": {
            "comment": "The HTML pages are in {build_dir!s}.",
        },
        "singlehtml": {
            "comment": "The HTML pages are in {build_dir!s}.",
        },
        "latex": {
            "comment": "The LaTeX files are in {build_dir!s}.",
        },
    }

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        project_directory = Path(__file__).parent

        self.builder = "html"
        self.paper = "letter"
        self.dist_dir = str(project_directory / "dist")
        self.build_root = str(project_directory / "build")
        self.src_dir = str(project_directory / "docs")

    def finalize_options(self):
        if self.builder in self.targets:
            self._actual_targets = [self.builder]
        elif self.builder == "all":
            self._actual_targets = self.targets.keys()
        else:
            self._actual_targets = []
        assert self.paper in ["a4", "letter"]
        self._canonical_directories()
        self.announce(
            "Building {!s} documentation".format(self.builder), 2)
        self.announce(
            "  using source at '{!s}'".format(self.src_dir), 2)
        self.announce(
            "  putting work files at '{!s}'".format(self.build_root), 2)
        self.announce(
            "  distributing documentation at '{!s}'".format(self.dist_root), 2)

    def run(self):
        """Run command."""
        result_dirs = {}
        for target in self._actual_targets:
            result_dirs[target] = self._build_doc(target)
        for target, result_dir in result_dirs.items():
            self.announce("Documentation target '{!s}' : {!s}".format(
                target,
                self.targets[target]["comment"].format(
                    build_dir=result_dir)), 2)

    def _canonical_directories(self):
        self.dist_root = Path(self.dist_dir)
        self.dist_root.mkdir(exist_ok=True, parents=True)
        self.dist_root.resolve()
        self.build_root = Path(self.build_root)
        self.build_root.mkdir(exist_ok=True, parents=True)
        self.build_root.resolve()
        self.src_dir = Path(self.src_dir)
        self.src_dir.resolve()

    def _build_doc(self, target):
        import shutil
        import sphinx
        build_dir = self.build_root / "docs" / target
        dist_dir = self.dist_root / "docs" / target

        cached_directory = build_dir.parent / "doctrees"

        all_sphinx_opts = [
            '',
            "-b", target,
            "-d", cached_directory,
            "-D", "latex_paper_size={!s}".format(self.paper),
            self.src_dir,
            build_dir
        ]

        sphinx.build_main([str(arg) for arg in all_sphinx_opts])

        shutil.rmtree(str(dist_dir), ignore_errors=True)
        dist_dir.parent.mkdir(exist_ok=True, parents=True)
        shutil.copytree(str(build_dir), str(dist_dir))
        return dist_dir


class Venv(Command):
    """
    Setup venvs for development or production
    """

    description = 'create a virtualenv pre-installed with dependencies'
    user_options = [
        # The format is (long option, short option, description).
        ('deps=', None, 'path to requirements.txt'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.deps = './requirements.txt'

    def finalize_options(self):
        """Post-process options."""
        if self.deps:
            deps = Path(str(self.deps))
            assert deps.exists(), \
                ('Requirements file %s does not exist.'.format(deps))

    def run(self):
        """Run command."""
        import venv
        venv.EnvBuilder(clear=True, with_pip=True).create("venv")


class Clean(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import shutil
        import glob
        shutil.rmtree("./build", ignore_errors=True)
        shutil.rmtree("./__pycache__", ignore_errors=True)
        shutil.rmtree("./dist", ignore_errors=True)
        for path in glob.glob("./*.egg-info"):
            shutil.rmtree(path, ignore_errors=True)


def get_distribution_info():
    return dict(
        name='cookiecutter-py',
        packages=[],
        version='1.0',
        description='Cookiecutter template for a Python package',
        author='Charles Bouchard-Légaré',
        license='GNU General Public License v3',
        author_email='cblegare.atl@ntis.ca',
        url='https://github.com/abstrus/cookiecutter-py',
        setup_requires=['pytest-runner', 'cookiecutter'],
        tests_require=['pytest', 'pytest-cookies', 'sphinx'],
        keywords=['cookiecutter', 'template', 'package'],
        cmdclass={'docs': Documentation,
                  'venv': Venv,
                  'clean': Clean,
                  'cookiecutter': Cookiecutter},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Software Development'
        ],
    )


def main():
    setup(**get_distribution_info())


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