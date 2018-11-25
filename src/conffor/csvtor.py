from typing import List

from pandas import DataFrame, read_csv

from ..snippets import ensure_dir_exist


def frame_csv(data_frame: DataFrame, file: str, **kwargs):
    """
    store pandas.DataFrame to csv, with default options
    """
    ensure_dir_exist(file)
    data_frame.to_csv(file, encoding='utf-8', **{**dict(header=True, index=False), **kwargs})


def save_list_csv(data: List[List], columns: List[str], file: str, **kwargs):
    """
    store data list to csv
    """
    frame = DataFrame(data, columns=columns)
    frame_csv(frame, file, **kwargs)


def read_list_csv(columns: List[str], file: str, **kwargs) -> List[List]:
    """
    read csv with columns, return raw data list

    :return: DataFrame rows value
    """
    frame = read_csv(file, names=columns, **{**dict(header=0, encoding='utf-8'), **kwargs})
    return frame.values
