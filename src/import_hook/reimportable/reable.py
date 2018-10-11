from collections import namedtuple
import sys

try:
    import __builtin__ as builtins
except ImportError:
    import builtins

reables = set()
ImportArgs = namedtuple('ImportArgs', ['globals', 'locals', 'fromlist', 'level'])
# defaults compatible with py2 import args
ImportArgs.__new__.__defaults__ = ({}, {}, tuple(), 0)


def reimport_hook():
    """
    add a import hook to re-import some module
    """
    if not hasattr(builtins, '__native_import__'):
        builtins.__native_import__ = builtins.__import__

        native_import = builtins.__native_import__

        def hook_import(name, *args, **kwargs):
            import_args = ImportArgs(*args)
            if import_args.fromlist:
                package_full = '.'.join([name] + list(import_args.fromlist))
                if package_full in reables:
                    del sys.modules[name]
                    del sys.modules[package_full]
            elif name in reables:
                del sys.modules[name]
            return native_import(name, *args, **kwargs)

        builtins.__import__ = hook_import


def set_reimport(module):
    """
    set a module to re-importable

    :param module: module name which want to reimportable
    :type module: str

    Usage:

    .. code:: python

        from sniputils.import_hook import set_reimport
        set_reimport(__name__)
    """
    reimport_hook()
    reables.add(module)


def disreimport(module):
    """
    disable a re-importable module

    usage like set_reimport

    :param module: module name which want to disable reimport
    :type module: str
    """
    if module in reables:
        reables.remove(module)
