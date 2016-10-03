#!/usr/bin/python3
# coding: utf8


"""
Helpers for YAML serialization
"""


import inspect
from typing import *
import ruamel.yaml as yaml

import wrapt

from _introspection import fqcn


def yaml_serializable_scalar(cls: Type,
                             yaml_repr: Callable[[Any], str]=str,
                             cls_ctor: Callable[[str], Any]=None,
                             tag: str=None) -> None:
    """
    Registers a multi representer and a constructor in the global YAML
    implementations.  In this case we use ruamel's YAML module.

    Value object classes are especially good candidates for being
    registered as yaml scalar this way.

    Example usage:

    .. code-block::

        >>> import ruamel.yaml as yaml
        >>> from pathlib import Path
        >>> yaml_serializable_scalar(Path)
        >>> yaml.dump(Path("../foo/bar/baz")).rstrip()
        "!pathlib.Path '../foo/bar/baz'"

    :param cls: The class we want to register
    :param yaml_repr: This callable is used to transform an instance of
                      cls into a scalar YAML value.  It defaults to
                      :func:´str´
    :param cls_ctor: This callable should return an instance of cls
                     (or a sub class) given a YAML scalar string. It
                     defaults to the class' default constructor.
    :param tag: Tags are a prefix in the scalar value used to identify
                the constructor implementation to use during
                deserialization. It defaults to the fully qualified
                class name of the class prefixed with '!'.
    """
    if tag is None:
        tag = "!{!s}".format(fqcn(cls))
    if yaml_repr is None:
        yaml_repr = str
    if cls_ctor is None:
        cls_ctor = cls

    if not tag.startswith("!"):
        tag = "!" + tag

    def representer(dumper: yaml.Dumper, data):
        return dumper.represent_scalar(str(tag), yaml_repr(data))

    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return cls_ctor(value)

    yaml.add_multi_representer(cls, representer)
    yaml.add_constructor(str(tag), constructor)


def yaml_scalar(yaml_repr: Callable[[Any], str] = None,
                cls_ctor: Callable[[str], Any] = None,
                tag: str=None):
    """
    Apply :func:´yaml_serializable_scalar´ as a class decorator

    .. todo::

        This decorator could be compatible with instance methods for
        registering properties

    :param yaml_repr:
    :param cls_ctor:
    :param tag:
    :raises TypeError: A :class:´TypeError´ is raised when not applied
                       to a class definition.
    :return: The decorated class
    """
    @wrapt.decorator()
    def decorator(wrapped, instance, args, kwargs):
        if instance is None:
            if inspect.isclass(wrapped):
                # Decorator was applied to a class.
                yaml_serializable_scalar(wrapped, yaml_repr, cls_ctor, tag)
                return wrapped(*args, **kwargs)
            else:
                # Decorator was applied to a function or staticmethod.
                raise TypeError("Cannot mark functon or staticmethod as "
                                "yaml serializable")
        else:
            if inspect.isclass(instance):
                # Decorator was applied to a classmethod.
                raise TypeError("Cannot mark class method as "
                                "yaml serializable")
            else:
                # Decorator was applied to an instancemethod.
                raise TypeError("Cannot mark instance method as "
                                "yaml serializable")
    return decorator


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)
