"""
Output the log to both log-file and console.
"""
import logging
import sys

from ..snippets import ensure_dir_exist

MSG_FORMAT = '%(asctime)s <%(name)s: %(threadName)s> %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def format_stream(stream=sys.stdout,
                  level=logging.INFO, msg_format=MSG_FORMAT, date_format=TIME_FORMAT):
    """
    create a formatted stream handler
    """
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
    handler.setFormatter(formatter)
    return handler


def clear_logsetting():
    """
    clear all root logger handlers, reset level debug
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers = []
    return root


def reset_logbase(
    filename=None, stream=sys.stdout,
    filemode='a',
    level=logging.INFO, msg_format=MSG_FORMAT, date_format=TIME_FORMAT,
):
    """
    :param filename: which file will logging to
    :param stream: stream type, default is ``stdout``
    :param filemode: [w]overwrite or [a]append mode, default is append
    :param level: logging level, default is ``INFO``
    :param msg_format: message format pattern str, default is ``logsetting.MSG_FORMAT``
    :param date_format: time format pattern str, default is ``logsetting.TIME_FORMAT``
    """
    format_config = {
        'level': level,
        'format': msg_format,
        'datefmt': date_format,
        'filemode': filemode
    }
    root = clear_logsetting()
    if filename:
        ensure_dir_exist(filename)
        logging.basicConfig(filename=filename, **format_config)
    if stream:
        root.addHandler(format_stream(stream, level, msg_format, date_format))
