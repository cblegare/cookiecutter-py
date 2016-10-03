#!/usr/bin/python3
# coding: utf8


"""
Descriptor API.

For several good examples of this, read the python cookbook :cite:´BeJo13´.

.. rubric:: References

.. [BeJo13] Python Cookbook, 3rd edition, by David Beazley and Brian K. Jones (O’Reilly). Copyright 2013 David Beazley and Brian Jones, 978-1-449-34037-7.
"""


class Descriptor(object):
    """
    Base class for a descriptor.  We do not use :class:´abc.ABCMeta´
    to minimize metaclass conflicts in subclass implementation.

    Example usage:

    .. code-block::

        >>> class HitPoints(Descriptor):
        ...     def __init__(self, name=None, **opts):
        ...         if 'on_below_zero' not in opts:
        ...             raise TypeError('missing death callback')
        ...
        ...         self.on_below_zero = opts.pop('on_below_zero')
        ...         super().__init__(name, **opts)
        ...
        ...     def __set__(self, instance, value):
        ...         super().__set__(instance, value)
        ...         if getattr(instance, self.name) < 0:
        ...             on_below_zero = getattr(instance, self.on_below_zero)
        ...             on_below_zero()
        ...
        >>> class PlayerCharacter(object):
        ...     hit_points = HitPoints("hit_points", on_below_zero="die")
        ...
        ...     def __init__(self, starting_hit_points):
        ...         self.hit_points = starting_hit_points
        ...
        ...     def die(self):
        ...         print("Arrrgs!!!")
        ...
        >>> elf_mage = PlayerCharacter(7)
        >>> elf_mage.hit_points = 3        # Rolled 4 on 1d4 but has -1 CON
        >>> monster_damage = 10            # Orc with a battleaxe rolled 1d12+3
        >>> elf_mage.hit_points -= monster_damage
        Arrrgs!!!

    """

    def __init__(self, name=None, **kwargs):
        """
        :param name: The property name of this descriptor.  The metaclass
                     :class:´DescriptorRegister´ can do it for you.
        :param kwargs: All kwargs are added as attributes. This may be
                       useful for subclasses relying on a configuration
        """
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        """
        :param instance: Since a decorator is used as an other object's
                         attribute, this contains that object's instance
        :param value: The raw value to set, before descriptor-fu
        """
        instance.__dict__[self.name] = value


class DescriptorRegister(type):
    """
    This metaclass let a class set automatically the name of its
    descriptors (sub-classes of :class:´Descritor´ above).

    For instance, our :class:´PlayerCharacter´'s definition can now be
    simpler:

    .. code-block::

        >>> class HitPoints(Descriptor):
        ...     pass # see above
        ...
        >>> class PlayerCharacter(metaclass=DescriptorRegister):
        ...     hit_points = HitPoints(on_below_zero="die") #

    """

    def __new__(cls, clsname, bases, methods):
        """
        :param clsname: Class name of the class we are creating
        :param bases: The class we are creating inherits from all of
                      these
        :param methods: A list of all method names, which include
                        attributes
        :return: A class we just created.
        """
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)


class HasDescriptorMixin(object):
    """
    Descriptors are useful for keeping a certain property as a specific
    class while exposing primitive type as it's interface. This class
    provides a class method for constructing a descriptor of this class.

    This class is also useful for monkey-patching third party objects to
    use them in descriptors.
    """

    @staticmethod
    def descriptor(*args, **kwargs):
        args_l = list(args)
        try:
            descriptor_class = args_l.pop(0)
        except IndexError:
            descriptor_class = Descriptor
        return descriptor_class(*tuple(args_l), **kwargs)


class TransformOnSet(Descriptor):
    """
    Transforms a value before assignment

    Example usage:

    .. code-block::

        >>> class Person(metaclass=DescriptorRegister):
        ...     age = TransformOnSet(set_callable=str)
        ...
        >>> john = Person()
        >>> john.age = 42
        >>> john.age
        '42'
        >>> john.age.__class__
        <class 'str'>

    """
    set_callable = lambda x: x

    def __set__(self, instance, value):
        super().__set__(instance, self.set_callable(value))


class String(TransformOnSet):
    set_callable = str


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, report=False)
