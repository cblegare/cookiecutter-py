#!/usr/bin/python3
# coding: utf8


"""Cookiecutter template tests."""


class Greetings(object):
    """
    Wraps a name into a greeting.

    Here is an example usage::

        >>> str(Greetings('Charles'))
        'Hello Charles!'

    """

    def __init__(self, name: str):
        """
        Trivial constructor.

        :param name: The name of whom to be greeted
        """
        self._name = name

    def __str__(self):
        """Provide a string representation of a normal greeting."""
        return 'Hello {!s}!'.format(self._name)


class Formal(Greetings):
    """A more formal greeter."""

    def __str__(self):
        """Provide a string representation of a formal greeting."""
        return 'Good evening {!s}'.format(self._name)


class Slang(Greetings):
    """A rude greeter."""

    def __str__(self):
        """Provide a string representation of a slang greeting."""
        return 'Yo !!1 {!s}!'.format(self._name)
