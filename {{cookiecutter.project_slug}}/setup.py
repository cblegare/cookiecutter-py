#!/usr/bin/python3.5
# coding: utf8


"""
This scripts lays building blocks for arbitrary large and complex
applications.
"""


import os
import platform
import fnmatch
import shutil

from pathlib import Path
from functools import lru_cache, reduce

from distutils.version import LooseVersion
import setuptools


PROJECT_ROOT = Path(__file__).parent

PYTHON_VERSION = platform.python_version_tuple()

DEFAULT_VERSION = '1.0'


__all__ = [
    'ProjectMetadata',
    'Clean',
    'Venv',
    'Documentation',
]


def main():
    meta = ProjectMetadata()
    meta.setup()


def cached_property(f):
    return property(lru_cache()(f))


class ProjectMetadata(object):
    """
    This hold distribution information primarily used at build time.
    """

    def __init__(self):
        self._version = None

    @cached_property
    def name(self) -> str:
        return '{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}'

    @cached_property
    def description(self):
        return '{{cookiecutter.project_short_description}}'

    @cached_property
    def version(self):
        if self._version is None:
            try:
                self._version = LooseVersion(read_file('VERSION'))
            except:
                self._version = LooseVersion(os.getenv('_VERSION',
                                                       DEFAULT_VERSION))

        return self._version

    @cached_property
    def url(self):
        return '{{cookiecutter.project_url}}'

    @cached_property
    def download_url(self):
        return '{!s}/tarball/{!s}'.format(self.url, self.version)

    @cached_property
    def license(self):
        return '{{cookiecutter.project_license}}'

    @cached_property
    def keywords(self):
        return ''

    @cached_property
    def author(self):
        return '{{cookiecutter.full_name}}'

    @cached_property
    def author_email(self):
        return '{{cookiecutter.email}}'

    @cached_property
    def classifiers(self):
        return []

    @cached_property
    def packages(self):
        if PYTHON_VERSION < ('3', '3'):
            find_packages = setuptools.find_packages
        else:
            find_packages = setuptools.PEP420PackageFinder.find
        return find_packages(str(PROJECT_ROOT), exclude=['docs',
                                                         'test*',
                                                         'requirements'])

    def setup(self):
        """Runs :func:`setuptools.setup`"""
        return setuptools.setup(**self.raw())

    @lru_cache()
    def raw(self) -> dict:
        """
        Provides a uniform access to all distribution data as python
        primitives, exactly the same one would provide to
        :func:`setuptools.setup`
        """
        return dict(name=str(self.name),
                    version=str(self.version),
                    description=str(self.description),
                    url=str(self.url),
                    license=str(self.license),
                    author=str(self.author),
                    author_email=str(self.author_email),
                    classifiers=[str(item)
                                 for item in self.classifiers],
                    packages=[str(item) for item in self.packages],
                    include_package_data=True,
                    entry_points={
                        'console_scripts': [
                            '{module!s}={module!s}.cli:main'.format(
                                module=self.name)
                        ]
                    },
                    cmdclass={'docs': Documentation,
                                'venv': Venv,
                                'clean': Clean},
                    install_requires=[],
                    tests_require=['pytest',
                                   'pytest-cookies'],
                    setup_requires=['pbr>=1.9',
                                    'setuptools>=17.1',
                                    'pytest',
                                    'pytest-runner'])

    def __str__(self):
        import pprint
        return pprint.pformat(self.raw(),)


class Clean(setuptools.Command):
    """
    Custom clean command to tidy up the project.
    """

    description = 'Custom clean command to tidy up the project.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        patterns = [
            "build",  "dist", "*.egg-info", "*.egg", "*.pyc", "*.pyo", "*~",
            "__pycache__", ".tox", ".coverage", "htmlcov"
        ]

        for pattern in patterns:
            self.remove_matching_files(pattern)

    @staticmethod
    def remove_matching_files(pattern):
        for path in find_files(pattern):
            shutil.rmtree(path, ignore_errors=True)


class Venv(setuptools.Command):
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
        venv.EnvBuilder(clear=True, with_pip=True).create(".")


class Documentation(setuptools.Command):
    """
    Make the documentation.
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
        import os
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        project_directory = Path(os.getcwd())

        self.builder = "html"
        self.paper = "letter"
        self.dist_dir = str(project_directory / "dist" / "docs")
        self.build_dir = str(project_directory / "build" / "docs")
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
            "  putting work files at '{!s}'".format(self.build_dir), 2)
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
        self.build_dir = Path(self.build_dir)
        self.src_dir = Path(self.src_dir)

        self.dist_root.mkdir(exist_ok=True, parents=True)
        self.build_dir.mkdir(exist_ok=True, parents=True)

        self.dist_root.resolve()
        self.build_dir.resolve()
        self.src_dir.resolve()

    def _build_source(self):
        import sphinx.apidoc
        build_dir = self.src_dir

        # metadata contains information supplied in setup()
        metadata = self.distribution.metadata

        # package_dir may be None, in that case use the current directory.
        src_dir = Path((self.distribution.package_dir or {'': ''})[''])

        sphinx_apidoc_opts = [
            '',
            '--module-first',   # Put module documentation before submodule
                                # documentation
            '--doc-project', metadata.name,
            '--output-dir', build_dir,
            '--maxdepth', 4,
            '--module-first',
            src_dir,
            'setup.py'
        ]

        canonical_opts = [str(arg) for arg in sphinx_apidoc_opts]

        self.announce("  Invoking sphinx : ''".format(" ".join(canonical_opts)))
        sphinx.apidoc.main([str(arg) for arg in sphinx_apidoc_opts])

        return build_dir

    def _build_doc(self, target):
        from datetime import datetime
        import shutil
        import sphinx

        rst_src = self._build_source()
        metadata = self.distribution.metadata

        build_dir = self.build_dir / target
        dist_dir = self.dist_root / target

        cached_directory = build_dir.parent / "doctrees"

        all_sphinx_opts = [
            '',
            "-b", target,            # builder to use; default is html
            "-d", cached_directory,  # path for the cached env and doctree files
            '-n',                    # warn about all missing references
            '-q',                    # no output on stdout, warnings on stderr
            '-W',                    # turn warnings into errors
            '-T',                    # show full traceback on exception
            "-D", "latex_paper_size={!s}".format(self.paper),
            '-D', 'project={!s}'.format(metadata.name),
            '-D', 'version={!s}'.format(metadata.version),
            '-D', 'copyright="{!s}, {!s}"'.format(datetime.now().year,
                                                  metadata.author),
            rst_src,
            build_dir
        ]

        sphinx.build_main([str(arg) for arg in all_sphinx_opts])

        shutil.rmtree(str(dist_dir), ignore_errors=True)
        dist_dir.parent.mkdir(exist_ok=True, parents=True)
        shutil.copytree(str(build_dir), str(dist_dir))
        return dist_dir


def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def read_file(file_path):
    return Path(PROJECT_ROOT / str(file_path)).read_text()


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


if __name__ == "__main__":
    main()
