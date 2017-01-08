"""..."""

import os
import configparser
from ast import literal_eval

__all__ = ("sdl2_path", "Singleton", "get_cfg")


def sdl2_path(*args):
    """Get the dnf_game base path."""
    return os.path.join(os.path.dirname(__file__), '..', *args)


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
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]


class _ConfigParser(configparser.ConfigParser, Singleton):
    """..."""

    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)
        self.read(sdl2_path('sdl2.cfg'))


def get_cfg(section, option, convert=False):
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
        v = _ConfigParser().get(section, option)
        if convert:
            return literal_eval(v)
        else:
            return v
    except KeyError:
        return None
    except configparser.NoOptionError:
        return None
