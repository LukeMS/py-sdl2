"""..."""

import os
from configparser import ConfigParser as _ConfigParser


def sdl2_path(*args):
    """Get the dnf_game base path."""
    return os.path.join(os.path.dirname(__file__), '..', *args)


class Singleton(object):
    """Restrict the instantiation of each class to one object.

    Must be declared as a metaclass of the singleton classes.

    Example:
        class SingletonJR(metaclass=Singleton)
            pass
    """

    _instances = {}

    def __new__(cls, *args, **kwargs):
        ""
        if cls._instances.get(cls, None) is None:
            print("new")
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]


class ConfigParser(_ConfigParser, Singleton):
    """..."""

    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)
        self.read(sdl2_path('sdl2.cfg'))


def get_cfg(option, key):
    """Interface for ConfigParser.

    Args:
        option (str): group in the ini/cfg file
        key (str): key inside the group

    Usage:
        get_cfg('DLL', 'PYSDL2_DLL_PATH')"""
    try:
        return ConfigParser()[option][key]
    except KeyError:
        return None
