#!/usr/bin/python3
# coding: utf8


"""
Configuration API
"""


import functools
from distutils.version import LooseVersion

import descriptor

from _introspection import fqcn
import _yaml


def compose(*functions):
    def compose_two_functions(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose_two_functions,
                            functions,
                            lambda x: x)


@_yaml.yaml_scalar()
class Version(LooseVersion, descriptor.HasDescriptorMixin):
    """
    A fixed version class also providing descriptor

    Example usage:

    .. code-block::

        >>> v1 = Version("1.0")
        >>> v2 = Version("2.0")
        >>> v1 > v2
        False

    Since this class is marked as a YAML scalar, it is easy to
    serialize  and deserialize it
    """

    def _cmp(self, other):
        """
        This fixes bad comparison such as

        .. code-block::

            >>> v1 = Version("1.0")
            >>> v1 == ()
            False

        :param other:
        :return:
        """
        try:
            return super()._cmp(other)
        except AttributeError:
            return -1

    @staticmethod
    def descriptor(*args, **kwargs):
        """
        See also :class:´HasDescriptorMixin´

        :param args:
        :param kwargs:
        :return: A :class:´Descriptor´ instance
        """
        return descriptor.TransformOnSet(compose(Version, str), *args, **kwargs)

    def __repr__(self):
        return "<{!s} '{!s}'>".format(fqcn(self.__class__), self)


class Struct(metaclass=descriptor.DescriptorRegister):
    """
    Configuration object
    Example usage:

    .. code-block::

        >>> persona = Struct()
        >>> persona.full_name = "Jane Doe"
        >>> persona.full_name
        'Jane Doe'
        >>> print(persona.dict())
        {'full_name': 'Jane Doe'}

    """
    def dict(self):
        return self.__dict__


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)
