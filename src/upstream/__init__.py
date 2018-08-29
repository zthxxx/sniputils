"""
inject monkey patch

    append upstream folder path in env PATH while folder is module
        to resolve relative import as absolute grammar

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
"""
import inspect

from .track_inject import path_inject

current = inspect.currentframe()
upstream = inspect.currentframe().f_back
back_import = inspect.getsourcefile(upstream)

path_inject(back_import)
