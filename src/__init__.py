import locale
from os import path

from setuptools import find_packages

__version__ = '0.1.1'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())

__all__ = find_packages(path.dirname(__file__))
# but only import_hook designed to compatible with python2.7


def try_locale_chain(locales):
    for item in locales:
        try:
            return locale.setlocale(locale.LC_ALL, item)
        except locale.Error:
            pass


# recommend to set 'LC_ALL=en_US.UTF-8'
# it's must if use click
# also set 'LC_ALL=en_US.UTF-8' in pycharm environment or system env
# PyCharm -> Run -> Edit Configurations -> Defaults -> Python -> Environment variables
# $ export LC_ALL=en_US.UTF-8

try_locale_chain(('en_US.UTF-8', 'en_US', 'C'))


def get_version():
    return __version__
