# -*- coding: utf-8 -*-
r"""Duckbot module loader.

Dynamically import duckbot modules, such as commands and utilities.
"""
from typing import List
import logging

import os
import importlib

logger = logging.getLogger(__name__)

_TOP_PACKAGE = 'duckbot'
_CMD_PACKAGE = 'commands'
_UTL_PACKAGE = 'util'


def loadBotCommands() -> dict:
    r"""Load bot command modules.

    Returns
    -------
    dict or None
        Command names mapped to their modules

    See Also
    --------
    `moduleLoader.loadFrom` for more details
    """
    logger.info('Loading bot commands')
    return loadFrom(f'{_TOP_PACKAGE}.{_CMD_PACKAGE}')


def loadSubCommands(package: str) -> dict:
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
    logger.info(f'Loading subcommands for package: {package}')
    return loadFrom(f'{_TOP_PACKAGE}.{_CMD_PACKAGE}.sub_{package}')


def loadFrom(package: str) -> dict:
    r"""Load modules from an arbitrary package.

    Dynamically import modules located inside of package name provided. If
    package is not in `PYTHONPATH` environment variable then no modules
    will be loaded.

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
    path = os.path.realpath(os.path.join(*package.split('.')))
    if os.path.isdir(path):
        names = _getModuleNames(path)
        paths = [f'{package}.{name}' for name in names]
        logger.info(paths)
        modules = _loadModules(paths)
    else:
        logger.error(f'{package} not found. No modules loaded.')
    return modules


def _getModuleNames(path: str) -> List[str]:
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


def _loadModules(paths: List[str]) -> dict:
    r"""Import requested modules.

    Import modules from a given list of dot qualified paths and give back a
    mapping of the module names to the module itself. If a module has
    defined a `NAMES` attribute then those values will be used as names for
    the module, otherwise the file name will be used. If a module has a
    `DISABLED` attribute and it is ``True`` then that module will not be
    returned.

    Parameters
    ----------
    paths
        Dot qualified module paths

    Returns
    -------
    dict
        Module names mapped to modules
    """
    loaded = {}
    for path in paths:
        module = importlib.import_module(path)
        if not (hasattr(module, 'DISABLED') and module.DISABLED):
            try:
                new = {name: module for name in module.NAMES}
                loaded = {**new, **loaded}
            except AttributeError:
                loaded[path.split('.')[-1]] = module
    return loaded
