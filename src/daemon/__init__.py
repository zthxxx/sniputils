"""
make current process run as daemon

.. note::
    need install ``python-daemon``

https://www.python.org/dev/peps/pep-3143

https://pypi.org/project/python-daemon/

Usage:

.. code:: python

    # deamon.py
    from sniputils.logsetting import reset_logbase
    reset_logbase('xxx.log')

    from sniputils.deamon import daemon
    with daemon:
        main()

.. code:: bash

    # use reset_logbase to set logging file
    $ export DAEMON_ERR_LOG='error.log'
    $ python deamon.py

    # its like the command via nohup
    $ nohup python -m main > xxx.log 2> error.log &
"""

from logging import FileHandler, Logger
import os
import signal
import sys

from daemon import DaemonContext
import lockfile

from ..snippets import ensure_dir_exist

DEFALUT_ERROR_LOG_FILE = 'error.log'
signal.signal(signal.SIGHUP, signal.SIG_IGN)


def freeze_logger_file_handlers():
    handlers = []
    handlers.extend(Logger.root.handlers)
    for logger in Logger.manager.loggerDict.values():
        if hasattr(logger, 'handlers'):
            handlers.extend(logger.handlers)
    return handlers


def preserve_logger(handler):
    if isinstance(handler, FileHandler):
        return handler.stream


def stderr_log(err=os.environ.get('DAEMON_ERR_LOG') or DEFALUT_ERROR_LOG_FILE):
    if err:
        ensure_dir_exist(err)
        stderr = open(err, 'a', encoding='utf-8')
        return stderr


class Daemon(DaemonContext):
    def terminate(self, signal_number, stack_frame):
        self.__exit__(None, None, None)
        sys.exit(0)


# ref: https://www.python.org/dev/peps/pep-3143
daemon = Daemon(
    working_directory=os.getcwd(),
    pidfile=lockfile.FileLock('.daemon.pid'),
    stderr=stderr_log(),
    files_preserve=freeze_logger_file_handlers(),
    signal_map={
        signal.SIGHUP: None,
        signal.SIGTERM: 'terminate'
    }
)
