from sys import path
from os.path import abspath, dirname, isfile, join


def path_inject(file):
    """
    append upstream folder path in env PATH while folder is module

    to resolve relative import as absolute grammar

    :param file: path of file
    :type file: str
    """
    if not file:
        return
    paths = set(path)
    folder_path = dirname(abspath(file))
    while folder_path and folder_path != '/':
        module = abspath(folder_path)
        if isfile(join(module, '__init__.py')) and module not in paths:
            path.append(module)
        folder_path = dirname(folder_path)
