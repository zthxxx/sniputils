import logging
from collections import namedtuple
from contextlib import contextmanager
from datetime import timedelta
from functools import reduce
from os import makedirs, path
from typing import Iterable, List

import arrow


class classproperty(property):  # noqa: N801
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


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


def reduce_set(items_list: List[list] = None) -> set:
    """
    flatten list of values list to set

    Usage:

    .. code:: python

        reduce_set([[1, 2, 3], [2, 3, 4], [5]])
        # {1, 2, 3, 4, 5}

        reduce_set([])
        # set()

        reduce_set()
        # set()

    :param items_list: list of values list
    :type items_list: list

    :return: flatten set
    """
    return set(
        reduce(lambda a, b: set(a) | set(b), items_list or [], set())
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


@contextmanager
def except_all(item=None):
    """
    context to except all Exception

    :param item: any thing as return

    :return: item

    .. code:: python

        print('start')
        with except_all():
            print(1 / 0)
            print('result')
        print('end')

    ..
        output ->

            start
            ERROR:root:division by zero
            end
    """
    try:
        yield item
    except Exception as e:
        logging.error(e)
        errors = globals().get('errors')
        if errors is not None:
            errors.append(e)
