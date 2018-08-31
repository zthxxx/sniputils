import sys
try:
    import __builtin__ as builtins
except ImportError:
    import builtins

reables = set()


def reimport_hook():
    """
    add a import hook to re-import some touchmodule
    :return:
    """
    if not hasattr(builtins, '__native_import__'):
        builtins.__native_import__ = builtins.__import__

        native_import = builtins.__native_import__

        def hook_import(name, *args, **kwargs):
            if name in reables:
                del sys.modules[name]
            return native_import(name, *args, **kwargs)

        builtins.__import__ = hook_import


def set_reimport(module):
    """
    :param module: str - module name which want to reimportable
    Usage:
        from reimportable import set_reimport
        set_reimport(__name__)
    """
    reimport_hook()
    reables.add(module)


def disreimport(module):
    """
    :param module: str - module name which want to disable reimport
    usage like set_reimport
    """
    if module in reables:
        reables.remove(module)
