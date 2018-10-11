from inspect import currentframe, getmodule
from ..reimportable import reable


exclude = {reable}


def which_import_me():
    """
    get which import the caller who used this track func

    Usage:

    .. code:: python

        # foo.py
        from .bar import *

        # bar.py
        from import_hook import which_import_me
        back_imported = which_import_me()
        print(back_imported)

    .. code:: bash

        $ python bar  --> output: <module foo.py>

    :return: module - which import the caller
    """
    this_track = currentframe()
    current_called = this_track.f_back
    upstream = current_called.f_back

    while upstream:
        trace_module = getmodule(upstream)
        upstream = upstream.f_back
        # back imported caller need to be a three party libraries,
        # impossible to be a builtin func or code
        # TODO: exclude is ugly, need to remove from stack frame
        if trace_module and trace_module not in exclude:
            return trace_module
