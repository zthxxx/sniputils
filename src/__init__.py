from os import path

from setuptools import find_packages

__version__ = '0.0.9'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())

__all__ = find_packages(path.dirname(__file__))


def get_version():
    return __version__
