"""
inject monkey patch

    append upstream folder path in env PATH while folder is module
        to resolve relative import as absolute grammar
        [support multiple to exec patch more times]
    Usage:
    as files like this:
    /top
        __init__.py
        /foo
            __init__.py
            foo.py
        /bar
            __init__.py
            bar.py

    in bar.py code as:
        # bar.py
        import sniputils.upstream
        import foo.foo.xxx      # <- this is relative import but use absolute grammar

    it will append ['/top'] to sys.path
    NOTE: re-import this module will also reload and append to sys.path,
    it's means
        import sniputils.upstream
        import sniputils.upstream
        import sniputils.upstream # <- will append ['/top', '/top', '/top'] to sys.path
"""
import inspect
import sys

from .track_inject import path_inject

current = inspect.currentframe()

module = inspect.getmodule(current)
# TODO: del module without load_module error (v0.0.9)
# del sys.modules[module.__name__]

upstream = current.f_back
back_import = inspect.getsourcefile(upstream)

path_inject(back_import)
