#!/usr/bin/python3
# coding: utf8


"""
Product configuration for setup
"""


import descriptor

from _config import Struct, Version


class ProductInfo(Struct):
    """
    Contains this distribution product information
    """
    name = descriptor.String()
    version = Version.descriptor()
    release = Version.descriptor()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)