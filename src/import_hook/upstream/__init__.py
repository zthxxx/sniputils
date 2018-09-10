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
        # in /test/foo/foo.py
        import sniputils.upstream
        # in /retest/bar/bar.py
        import sniputils.upstream
        # in /top.py
        import test.foo.foo
        import retest.bar.bar <- will append ['/test', '/retest'] to sys.path
"""

from inspect import getsourcefile

from .track_inject import path_inject
from ..import_track import which_import_me
from ..reimportable import set_reimport

set_reimport(__name__)

back_import = which_import_me()
back_module = getsourcefile(back_import)

path_inject(back_module)
