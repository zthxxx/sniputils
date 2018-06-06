from functools import reduce
from os import makedirs, path
from typing import Iterable


def ensure_dir_exist(file):
    dirs = path.dirname(file)
    if not path.exists(dirs):
        makedirs(dirs)


def ensure_set(data):
    if not isinstance(data, Iterable):
        return {data}
    if not isinstance(data, set):
        return set(data)
    return data


def args2set(func):
    def args_set_func(*args):
        sets = [ensure_set(arg) for arg in args]
        return func(*sets)

    return args_set_func


def reduce_set(items):
    return set(
        reduce(lambda a, b: set(a) | set(b), items)
    )
