"""
Some function for read and write json config file.
"""

import json

from ..snippets import ensure_dir_exist


def load(file: str):
    """
    load json file with default options

    :param file: file path to load
    :return: json data as python object
    """
    with open(file, 'r', encoding='utf-8') as jsonfile:
        config = json.load(jsonfile, encoding='utf-8')
        return config


def dump(file: str, config: dict, indent=2):
    """
    export dict as json file, with default options

    :param file: file path to export
    :param config: dict data object
    :param indent: json indent num
    """
    ensure_dir_exist(file)
    with open(file, 'w+', encoding='utf-8') as jsonfile:
        json.dump(
            config, jsonfile,
            indent=indent,
            ensure_ascii=False,
            sort_keys=True
        )
