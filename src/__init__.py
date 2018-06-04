__version__ = '0.0.2'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())


def get_version():
    return __version__
