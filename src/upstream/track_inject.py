from sys import path
from os.path import abspath, dirname, isfile, join


def path_inject(file):
    """
    append upstream folder path in env PATH while folder is module
    to resolve relative import as absolute grammar
    :param file: path of file
    """
    if not file:
        return
    folder_path = dirname(abspath(file))
    while folder_path and folder_path != '/':
        module = abspath(folder_path)
        if isfile(join(module, '__init__.py')):
            path.append(module)
        folder_path = dirname(folder_path)
