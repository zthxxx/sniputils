from collections import namedtuple
from datetime import timedelta
from functools import reduce
from os import makedirs, path
from typing import Iterable, List

import arrow


def ensure_dir_exist(file):
    dirs = path.dirname(file)
    if dirs and not path.exists(dirs):
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


def reduce_set(items: List[list]) -> set:
    return set(
        reduce(lambda a, b: set(a) | set(b), items)
    )


def period_split(start, end, delta: timedelta) -> List[namedtuple('period', ['start', 'end'])]:
    """
    :param start: period start time, string or datetime type
    :param end: period ending time, string or datetime type
    :param delta: steping length, must be a timedelta

    :return:

    ..
        input:  [start                                     end]
        output: [[start delta] [delta] ... [delta] [delta end]]
    """
    start = arrow.get(start)
    end = arrow.get(end)
    splits = []
    while start < end:
        next_step = start + delta
        splits.append((start, next_step if next_step <= end else end))
        start = next_step
    return splits
