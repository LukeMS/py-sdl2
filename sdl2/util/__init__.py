"""..."""

# support for Python 2.6, 2.7
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

# regular imports
import os
import configparser
from ast import literal_eval

__all__ = ("sdl2_path", "Singleton", "get_cfg", "iter_nested")


def sdl2_path(*args):
    """Get the dnf_game base path."""
    return os.path.join(os.path.dirname(__file__), '..', *args)


def iter_nested(iterables):
    """Iterate over a iterable of depth one or two.

    In both cases yield one item at a time.

    Args:
        iterables (iterable): a iterable or a iterable of iterables.

    Examples:
        >>> list(nested_or_not(((0, 0, 10, 10), (20, 20, 10, 10))))
        [(0, 0, 10, 10), (20, 20, 10, 10)]

        >>> list(nested_or_not((30, 30, 10, 10)))
        [(30, 30, 10, 10)]

        # in both cases this would work:
        # for tup in nested_or_not():
        #   do something
    """
    for nested in iterables:
        if hasattr(nested, "__iter__"):
            yield nested
        else:
            yield iterables
            break


class Singleton(object):
    """Restrict the instantiation of each class to one object.

    Should be used as a metaclass of the singleton classes.

    Example:
        class SingletonJR(metaclass=Singleton)
            pass
    """

    _instances = {}

    def __new__(cls, *args, **kwargs):
        """..."""
        if cls._instances.get(cls, None) is None:
            cls._instances[cls] = object.__new__(cls)
        return cls._instances[cls]


class _ConfigParser(configparser.ConfigParser):
    """..."""

    _instances = {}

    def __new__(cls, path=None, *args, **kwargs):
        """..."""
        fname = os.path.basename(path) if path else path
        if cls._instances.get(cls, None) is None:
            cls._instances[(cls, fname)] = object.__new__(cls)
        return cls._instances[(cls, fname)]

    def __init__(self, path=None, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)
        path = path or sdl2_path('sdl2.cfg')
        self.read(path)


def get_cfg(section, option, convert=False, path=None):
    """Interface for ConfigParser.

    Args:
        section (str): section in the cfg file (e.g. "MANAGER" == [MANAGER])
        option (str): key inside the group (e.g. "SCREEN_WIDTH")
        convert (bool): if True the value obtained will be converted using
            :py:meth: `ast.literal_eval` before its returned.

    Example:
        >>> get_cfg(section='MANAGER', option='SCREEN_WIDTH', convert=True)
        1024

    Returns:
        str (value of the cfg entry, if a match is found)
        None (if the option/key is not found)
    """
    try:
        v = _ConfigParser(path=path).get(section, option)
        if convert:
            return literal_eval(v)
        else:
            return v
    except KeyError:
        return None
    except configparser.NoOptionError:
        return None
