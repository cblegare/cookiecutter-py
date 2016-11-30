#!/usr/bin/python3
# coding: utf8


"""
Descriptor API.

For several good examples of this, read the python cookbook [BeJo13]_.

.. rubric:: References

.. [BeJo13] Python Cookbook, 3rd edition,
            by David Beazley and Brian K. Jones (O’Reilly).
            Copyright 2013 David Beazley and Brian Jones, 978-1-449-34037-7.
"""


class Descriptor(object):
    """
    Base class for a descriptor.

    We do not use :class:´abc.ABCMeta´ to minimize metaclass conflicts in
    subclass implementation.

    Example usage::

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
        Construct a descriptor.

        A descriptor's constructor is usually called from a class definition
        body.

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
        Set self.  This gets called with the assignement operator (*=*).

        :param instance: Since a decorator is used as an other object's
                         attribute, this contains that object's instance
        :param value: The raw value to set, before descriptor-fu
        """
        instance.__dict__[self.name] = value


class DescriptorRegister(type):
    """
    Automatically set the name of descriptors of generated classes.

    This metaclass let a class set automatically the name of its
    descriptors (sub-classes of :class:´Descriptor´).

    For instance, our :class:´PlayerCharacter´'s definition can now be
    simpler::

        >>> class HitPoints(Descriptor):
        ...     pass # see above
        ...
        >>> class PlayerCharacter(metaclass=DescriptorRegister):
        ...     hit_points = HitPoints(on_below_zero="die") #

    """

    def __new__(cls, clsname, bases, methods):
        """
        When the class is instanciated, set all names of :class:~`Descriptor`s.

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


class TransformOnSet(Descriptor):
    """
    Transform a value before assignment.

    Example usage::

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

    def __set__(self, instance, value):
        """Store the result of ``self.set_callable(value)``."""
        super().__set__(instance, self.set_callable(value))

    @classmethod
    def set_callable(cls, x):
        """Default to doing nothing (neutral)."""
        return x


class String(TransformOnSet):
    """Cast to string on every assignment."""

    set_callable = str


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, report=False)
