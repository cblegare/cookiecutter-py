#!/usr/bin/python3
# coding: utf8


"""
Some introspection helpers
"""


def fqcn(cls: type):
    """
    Provides a fully qualified class name for a given class.

    Note that fully qualified class names are not properly defined in
    python.  This is a simple shorthand made for plain convenience.

    Example usage:

    .. code-block::

        >>> class Foo(object):
        ...     class Bar(object):
        ...         pass
        ...
        >>> fqcn(Foo)
        '__main__.Foo'
        >>> fqcn(Foo.Bar)
        '__main__.Foo.Bar'

    :param cls:
    :return: The fully qualified class name as a string
    """
    mod = cls.__module__
    try:
        class_name = cls.__qualname__
    except AttributeError:
        class_name = cls.__class__
    return "{!s}.{!s}".format(mod, class_name)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)
