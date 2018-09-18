from typing import List

from pandas import DataFrame, read_csv

from ..snippets import ensure_dir_exist


def separator_filter(item):
    """
    filter whitespace which has ambiguity in data-str

    :param item: data item, if str, filter whitespace
    :return: item or filtered
    """
    if isinstance(item, str):
        return item.replace('\r', ' ').replace('\n', ' ').replace(',', '-')
    return item


def frame_csv(data_frame: DataFrame, file: str, **kwargs):
    """
    store pandas.DataFrame to csv, with default options
    """
    ensure_dir_exist(file)
    data_frame.to_csv(file, encoding='utf-8', header=True, index=False, **kwargs)


def save_list_csv(data: List[List], columns: List[str], file: str, **kwargs):
    """
    store data list to csv
    """
    for index, line in enumerate(data):
        data[index] = [separator_filter(item) for item in line]
    frame = DataFrame(data, columns=columns)
    frame_csv(frame, file, **kwargs)


def read_list_csv(columns: List[str], file: str, **kwargs) -> List[List]:
    """
    read csv with columns, return raw data list

    :return: DataFrame rows value
    """
    frame = read_csv(file, names=columns, header=0, encoding='utf-8', **kwargs)
    return frame.values
