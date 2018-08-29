from sys import path
from os.path import abspath, dirname, isfile, join


def path_inject(file):
    folder_path = dirname(file)
    while folder_path and folder_path != '/':
        module = abspath(folder_path)
        if isfile(join(module, '__init__.py')):
            path.append(module)
        folder_path = dirname(folder_path)
