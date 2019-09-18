# -*- coding: utf-8 -*-
r"""Duckbot module loader.

Dynamically import duckbot modules, such as commands and utilities.
"""
import importlib
import os

# UTL_ROOT = os.path.dirname(os.path.realpath(__file__))
# SRC_ROOT = os.path.dirname(_UTL_ROOT)
# MOD_ROOT = os.path.join(SRC_ROOT, 'ducklings')
# CMD_ROOT = os.path.join(MOD_ROOT, 'command')
_TOP_PACKAGE = 'duckbot'
_CMD_PACKAGE = 'commands'
_UTL_PACKAGE = 'util'


def loadBotCommands():
    r"""Load bot command modules.

    Returns
    -------
    dict or None
        Command names mapped to their modules

    See Also
    --------
    `moduleLoader.loadFrom` for more details
    """
    return loadFrom(f'{_TOP_PACKAGE}.{_CMD_PACKAGE}')


def loadSubCommands(package: str):
    r"""Load subcommands from a given package name.

    Parameters
    ----------
    package
        Name of package to load subcommands for

    Returns
    -------
    dict or None
        Subcommand names mapped to their modules

    See Also
    --------
    `moduleLoader.loadFrom` for more details
    """
    return loadFrom(f'{_TOP_PACKAGE}.{_CMD_PACKAGE}.sub_{package}')


def loadFrom(package: str):
    r"""Load modules from an arbitrary package.

    Dynamically import modules located inside of package name provided. If
    package is not in `PYTHONPATH` then no modules will be loaded.

    Parameters
    ----------
    package
        Dot qualified package path, e.g. duckbot.util

    Returns
    -------
    dict or None
        Module names mapped to the modules
    """
    modules = None
    path = os.path.join(*package.split('.'))
    if os.path.isdir(path):
        names = _getModuleNames(path)
        paths = [f'{package}.{name}' for name in names]
        modules = _loadModules(paths)
    return modules


def _getModuleNames(path):
    r"""Find modules in the given package path.

    Get the names of modules at a given relative path. Modules that begin
    with '_' will not be included.

    Parameters
    ----------
    path
        Relative path to package directory

    Returns
    -------
    list[str]
        Module names
    """
    modules = []
    # This assumes the directory is not empty. There should always at least
    # be an __init__.py in the package directory if things are structured
    # properly.
    _, _, filenames = next(os.walk(path))
    for name in filenames:
        name = name.split('.')
        # This also assumes that modules will not have '.' in the name.
        # It's better to die than let that happen anyway.
        if name[1] == 'py' and not name[0].startswith('_'):
            modules.append(name[0])
    return modules

# Import modules and map them to their names in a dictionary
# Params: mod_paths - list of dot qualified module paths to be imported
# Return: Dictionary with module names mapped to the module
def _loadModules(mod_paths):
    loaded = {}
    for path in mod_paths:
        # Import the module
        module = importlib.import_module(path)
        if not hasattr(module, 'DISABLED') or not module.DISABLED:
            try:  # See if the module defined its own names
                new = {name:module for name in module.NAMES}
                loaded = {**new, **loaded}
            except AttributeError:  # Otherwise use the path basename
                loaded[path.split('.')[-1]] = module
    return loaded
