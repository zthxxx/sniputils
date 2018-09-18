import locale
from os import path

from setuptools import find_packages

__version__ = '0.1.0'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())

__all__ = find_packages(path.dirname(__file__))
# but only import_hook designed to compatible with python2.7


# recommend to set 'LC_ALL=en_US.UTF-8'
# it's must if use click
# also set 'LC_ALL=en_US.UTF-8' in pycharm environment or system env
# PyCharm -> Run -> Edit Configurations -> Defaults -> Python -> Environment variables
# $ export LC_ALL=en_US.UTF-8
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def get_version():
    return __version__
