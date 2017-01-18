#!/usr/bin/python3.5
# coding: utf8


"""This scripts lays building blocks for development tooling."""


from distutils.version import LooseVersion, Version
from functools import lru_cache, reduce
from pathlib import Path
from typing import List
import email.utils
import fnmatch
import os
import platform
import setuptools
import shutil
import urllib.parse

__all__ = (
    'ProjectMetadata',
    'Clean',

    'Documentation',
)


PROJECT_ROOT = Path(__file__).parent

PYTHON_VERSION = platform.python_version_tuple()

DEFAULT_VERSION = '1.0'


def cached_property(f):
    """
    Annotate a class member to make it a cached property.

    This is simply a combination of :func:`property` and :func:`lru_cache`
    annotations merged together.
    """
    return property(lru_cache()(f))


class ProjectMetadata(object):
    """
    This hold distribution information primarily used at build time.

    Properties of this class are intended to roughly fit the
    `metadata
    <https://docs.python.org/2/distutils/setupscript.html#additional-meta-data>`_
    expected by keyword arguments by the :func:`setuptools.setup` function.

    Since we use *setuptools*, you may wish to read about
    `new and changed setup keywords
    <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#new-and-changed-setup-keywords>`.
    """

    def __init__(self):
        """Initialize some cached or internal storage of data."""
        self._version = None

    @cached_property
    def name(self) -> str:
        """
        Name of the package.

        .. note:
            This field is required by :func:`setuptools.setup`

        :return: A short string
        """
        value = '{% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}'
        return self._ensure_short_string(value)

    @cached_property
    def description(self) -> str:
        """
        Short, summary description of the package.

        :return: A short string
        """
        value = '{{cookiecutter.project_short_description}}'
        return self._ensure_short_string(value)

    @cached_property
    def version(self) -> Version:
        """
        Version of this release.

        .. note:
            This field is required by :func:`setuptools.setup`

        :return: A short string
        """
        if self._version is None:
            try:
                self._version = LooseVersion(read_file('VERSION'))
            except OSError:
                self._version = LooseVersion(os.getenv('_VERSION',
                                                       DEFAULT_VERSION))

        return self._ensure_short_string(self._version)

    @cached_property
    def url(self) -> str:
        """
        Home page for the package.

        .. note:
            This field is required by :func:`setuptools.setup`

        :return: A URL
        """
        value = '{{cookiecutter.project_url}}'
        return self._ensure_url(value)

    @cached_property
    def download_url(self) -> str:
        """
        Location where the package may be downloaded.

        :return: A URL
        """
        value = '{!s}/tarball/{!s}'.format(self.url, self.version)
        return self._ensure_url(value)

    @cached_property
    def license(self) -> str:
        """
        License for the package.

        .. note:
            The "license" field is a text indicating the license
            covering the package where the license is not a selection
            from the "License" Trove classifiers. See the :attr:`~classifiers`
            field. Notice that there's a "licence" distribution option
            which is deprecated but still acts as an alias for license.

        :return: A short string
        """
        value = '{{cookiecutter.project_license}}'
        return self._ensure_short_string(value)

    @cached_property
    def keywords(self) -> str:
        """
        A whitespace-separated list of keywords about this project.

        I have been able to find documentation about this parameter but it
        is clearly used in the setuptools documentation in the example
        provided for `basic usage
        <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#basic-use>`
        """
        return ''

    @cached_property
    def author(self) -> str:
        """
        Package author’s name.

        Either the author or the maintainer must be identified. If
        maintainer is provided, distutils lists it as the author in
        PKG-INFO.

        :return: A short string
        """
        value = '{{cookiecutter.full_name}}'
        return self._ensure_short_string(value)

    @cached_property
    def author_email(self) -> str:
        """
        Email address of the package author.

        See also :attr:`~author`

        :return: An email address
        """
        value = '{{cookiecutter.email}}'
        return self._ensure_email_address(value)

    @cached_property
    def classifiers(self) -> List[str]:
        """
        A list of classifiers.

        Feel free to consult
        `all possibles classifiers
        <https://pypi.python.org/pypi?%3Aaction=list_classifiers>`.

        :return: A list of strings
        """
        value = []
        return [self._ensure_short_string(string) for string in value]

    @cached_property
    def packages(self) -> List[str]:
        """
        A list of packages to distribute (and all their submodules).

        It's usage is explained in
        `distutils documentation
        <https://docs.python.org/2/distutils/setupscript.html#listing-whole-packages>`

        You may also read about :func:`setuptools.find_packages` function and
        `it's usage
        <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#using-find-packages>`.

        :return: A list of strings
        """
        if PYTHON_VERSION < ('3', '3'):
            find_packages = setuptools.find_packages
        else:
            find_packages = setuptools.PEP420PackageFinder.find
        value = find_packages(str(PROJECT_ROOT), exclude=['docs*',
                                                          'test*',
                                                          'requirements'])
        return [self._ensure_short_string(package) for package in value]

    @cached_property
    def install_requires(self) -> List[str]:
        """
        Production dependancies.

        A string or list of strings specifying what other distributions need
        to be installed when this one is.

        It's usage is explained in `setuptools documentation
        <http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies>`

        :return: a list of strings
        """
        return list_from_file('requirements/_install.txt')

    @cached_property
    def tests_require(self) -> List[str]:
        """
        Automated tests dependancies.

        If your project’s tests need one or more additional packages besides
        those needed to install it, you can use this option to specify them.

        It's usage is explained in `setuptools documentation
        <http://setuptools.readthedocs.io/en/latest/setuptools.html#new-and-changed-setup-keywords>`

        :return: a list of strings
        """
        return list_from_file('requirements/_tests.txt')

    def setup(self):
        """Run :func:`setuptools.setup` using :func:~`raw`."""
        return setuptools.setup(**self.raw())

    @lru_cache()
    def raw(self) -> dict:
        """
        Create a generic dict representation.

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
                              'clean': Clean},
                    install_requires=self.install_requires,
                    tests_require=self.tests_require,
                    setup_requires=['pbr>=1.9',
                                    'setuptools>=17.1',
                                    'flake8',
                                    'pytest-runner',
                                    'pytest'])

    def __str__(self):
        """Provide a human-readable representation."""
        import pprint
        return pprint.pformat(self.raw(),)

    @staticmethod
    def _ensure_short_string(string):
        assert len(str(string)) <= 200
        return string

    @staticmethod
    def _ensure_long_string(string):
        return string

    @staticmethod
    def _ensure_email_address(string):
        _, email_str = email.utils.parseaddr(str(string))
        assert email_str == str(string)
        return string

    @staticmethod
    def _ensure_url(string, qualifying=None):
        min_attributes = ('scheme', 'netloc')

        qualifying = min_attributes if qualifying is None else qualifying
        token = urllib.parse.urlparse(str(string))
        valid = all([getattr(token, qualifying_attr)
                     for qualifying_attr in qualifying])
        assert valid
        return string


class Clean(setuptools.Command):
    """Custom clean command to tidy up the project."""

    description = 'Custom clean command to tidy up the project.'
    user_options = []
    default_patterns = ['build',  'dist', '*.egg-info', '*.egg', '*.pyc',
                        '*.pyo', '*~', '__pycache__', '.tox', '.coverage',
                        'htmlcov']

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        for pattern in self.default_patterns:
            self._remove_matching_files(pattern)

    def _remove_matching_files(self, pattern):
        for path in find_files(pattern):
            self.announce('Cleaning path {!s}'.format(path), 2)
            shutil.rmtree(path, ignore_errors=True)


class Documentation(setuptools.Command):
    """
    Make the documentation (without the *Make* program).

    .. note::

        This command will not allow any warning from `Sphinx`_, treating
        them as errors.

    .. _Sphinx: http://www.sphinx-doc.org/
    """

    description = 'create documentation distribution'
    user_options = [
        ('builder=', None, 'documentation output format'
                           ' [default: html]'),
        ('paper=', None, 'paper format [default: letter]'),
        ('dist-dir=', None, 'directory to put final built distributions in'
                            ' [default: dist/docs]'),
        ('build-dir=', None, 'temporary directory for creating the '
                             'distribution'
                             ' [default: build/docs]'),
        ('src-dir=', None, 'documentation source directory'
                           ' [default: docs]'),
    ]

    targets = {
        'html': {
            'comment': 'The HTML pages are in {build_dir!s}.',
        },
        'dirhtml': {
            'comment': 'The HTML pages are in {build_dir!s}.',
        },
        'singlehtml': {
            'comment': 'The HTML pages are in {build_dir!s}.',
        },
        'latex': {
            'comment': 'The LaTeX files are in {build_dir!s}.',
        },
    }

    def initialize_options(self):
        """Set default values for options."""
        import os
        # Each user option must be listed here with their default value.
        project_directory = Path(os.getcwd())

        self.builder = 'html'
        self.paper = 'letter'
        self.dist_dir = str(project_directory / 'dist' / 'docs')
        self.build_dir = str(project_directory / 'build' / 'docs')
        self.src_dir = str(project_directory / 'docs')

    def finalize_options(self):
        """Post-process options."""
        if self.builder in self.targets:
            self._actual_targets = [self.builder]
        elif self.builder == 'all':
            self._actual_targets = self.targets.keys()
        else:
            self._actual_targets = []
        assert self.paper in ['a4', 'letter']
        self._canonical_directories()
        self.announce(
            'Building {!s} documentation'.format(self.builder), 2)
        self.announce(
            '  using source at "{!s}"'.format(self.src_dir), 2)
        self.announce(
            '  putting work files at "{!s}"'.format(self.build_dir), 2)
        self.announce(
            '  distributing documentation at "{!s}"'.format(self.dist_root), 2)

    def run(self):
        """Run command."""
        result_dirs = {}
        for target in self._actual_targets:
            result_dirs[target] = self._build_doc(target)
        for target, result_dir in result_dirs.items():
            self.announce('Documentation target "{!s}" : {!s}'.format(
                target,
                self.targets[target]['comment'].format(
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

        self.announce('  Invoking sphinx : '
                      '"{!s}"'.format(' '.join(canonical_opts)))
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

        cached_directory = build_dir.parent / 'doctrees'

        all_sphinx_opts = [
            '',
            '-b', target,            # builder to use; default is html
            '-d', cached_directory,  # path for the cached doctree files
            '-n',                    # warn about all missing references
            '-q',                    # no output on stdout, warnings on stderr
            '-W',                    # turn warnings into errors
            '-T',                    # show full traceback on exception
            '-D', 'latex_paper_size={!s}'.format(self.paper),
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
    """
    Compose provided functions.

    Here is an example usage::

        >>>def f(x):
        ...    return x+1
        ...
        >>> def g(y):
        ...    return y**2
        ...
        >>> f_o_g = compose(f, g)
        >>> f_o_g(1) == f(g(1))
        True
        >>> f_o_g(1)
        2
        >>> g_o_f =  compose(g, f)
        >>> g_o_f(1) == g(f(1))
        True
        >>> g_o_f(1)
        4
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def read_file(file_path: str) -> str:
    """Read text from file relative to the project root."""
    return Path(PROJECT_ROOT / str(file_path)).read_text()


def list_from_file(file_path: str) -> List[str]:
    content = read_file(file_path)
    return [line.strip() for line in content.splitlines() if line]


def find_files(directory, pattern):
    """Generate file names matching pattern recursively found in directory."""
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def main():
    """Main entry point."""
    meta = ProjectMetadata()
    meta.setup()


if __name__ == '__main__':
    main()
