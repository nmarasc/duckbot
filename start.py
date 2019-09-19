#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Main driver script for Duckbot.

This script handles program setup (commmand line parsing, logging config,
etc) and then starts Duckbot.
"""
import logging
import logging.config

import sys
import os
import re
import argparse
from configparser import ConfigParser, ExtendedInterpolation

from duckbot import Duckbot
from duckbot import EXIT_CODES
# ##FIXME don't reach into the bowels of the package
from duckbot.util.config import _valueize

# Configuration file paths
CONFPATH_LOG = '.config/logging.conf'
CONFPATH_BOT = '.config/bot.conf'

# Which clients to connect to
CONNECT_DISCORD = True
CONNECT_SLACK = False


def main() -> int:
    r"""Mainline entry point.

    Create and run a Duckbot instance with supplied command line arguments
    and config file options.

    Returns
    -------
    int
        Exit code from the bot (documented in duckbot.core)
    """
    # The logger is allowed to be global to the module, since everything
    # uses it.
    global logger

    args = parseCommandLine()

    log_conf = parseLogConfig(args)
    logging.config.dictConfig(log_conf)
    logging.getLogger('duckbot.clients').setLevel('DEBUG')
    logger = logging.getLogger(__name__)
    logger.info('Logging configured and initialized')

    duckbot = duckboot(args)

    if duckbot is None:
        exit_code = EXIT_CODES['BAD_INIT']
    else:
        logger.info('Duckbot created and configured')
        exit_code = duckbot.run()

    if exit_code != 0:
        logger.critical('Duckbot failed with exit code: {exit_code}')
    else:
        logger.info('Duckbot shut down successfully')
    return exit_code


def duckboot(args: dict) -> Duckbot:
    r"""Create a Duckbot instance.

    Search for client tokens and instantiate a bot instance. The bot will
    fail to be created if connections are requested, but no tokens are
    found.

    Parameters
    ----------
    args
        Command line arguments

    Returns
    -------
    Duckbot
        Duckbot instance or None on failure
    """
    config = {
        'slack_token': None,
        'discord_token': None,
        'temporary': False,
        'muted': args.muted
    }

    if CONNECT_SLACK:
        config['slack_token'] = _findToken('SLACK_TOKEN')
    if CONNECT_DISCORD:
        config['discord_token'] = _findToken('DISCORD_TOKEN')
    if args.temporary in ['all', 'bot']:
        config['temporary'] = True

    duckbot = Duckbot(config)
    return duckbot


def parseCommandLine() -> dict:
    r"""Parsing function for command line arguments.

    Utilize the ``argparse`` package to handle gathering and parsing of
    command line arguments.

    Returns
    -------
    dict
        Command line arguments with their values
    """
    # Use the script docstring as part of the usage message
    cl_parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=('options:\n'
            '  log\tlogging messages are temporary\n'
            '  bot\tbot state is temporary\n'
            '  all\tall of the above are temporary, default for no option'
        )
    )
    # Possibly change verbosity to a count and make the default level
    # WARNING if the INFO messages get too chatty
    cl_parser.add_argument(
        '-d', '--debug', action='store_true',
        help='\tadd debug messages to the log')
    cl_parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='\tprint log messages to the console')
    cl_parser.add_argument(
        '-m', '--muted', action='store_true', default=False,
        help='\ttell bot not to respond to messages')
    cl_parser.add_argument(
        '-t', '--temporary', action='store', const='all',
        nargs='?', metavar='option',
        help='\tdo not write values out to disk')
    args = cl_parser.parse_args()
    if args.temporary not in [None, 'all', 'bot', 'log']:
        raise ValueError(f'option not recognized: {args.temporary}')
    return args


def parseLogConfig(args: dict) -> dict:
    r"""Parse config file for logging.

    Gather logging configuration data and then massage the data into a
    valid format. Any command line flags that affect logging configuration
    are read and handlers are adjusted. The log directory specified is
    created if it does not already exist.

    Parameters
    ----------
    args
        Command line arguments

    Returns
    -------
    dict
        Logging configuration data
    """
    parser = ConfigParser(
        interpolation=ExtendedInterpolation(),
        allow_no_value=True
    )
    parser.optionxform = str
    parser.read(CONFPATH_LOG)

    config = _valueize(parser['general'])
    config['root'] = {**parser['root']}
    config['root']['handlers'] = re.split(
        r',\s*',
        config['root']['handlers']
    )
    config['formatters'] = _parseSubsection('formatters', parser)
    config['handlers'] = _parseSubsection('handlers', parser)
    config['loggers'] = _parseSubsection('loggers', parser)

    if args.debug:
        config['root']['level'] = 'DEBUG'
        config['handlers']['default']['level'] = 'DEBUG'
        config['handlers']['console']['level'] = 'DEBUG'
    if args.verbose:
        config['root']['handlers'].append('console')
    if args.temporary in ['all', 'log']:
        config['root']['handlers'].remove('default')

    # The log file is created at config time, so the path has to exist
    # before configuration happens
    os.makedirs(parser['paths']['log_dir'], exist_ok=True)
    return config


def _parseSubsection(section: str, parser: ConfigParser) -> dict:
    r"""Aggregate subsection data from the parser.

    Use the keys field of a section to determine subsections and gather all
    subsections into a single dictionary.

    Parameters
    ----------
    section
        Name of section to find subsections for
    parser
        ``ConfigParser`` instance that has read config data

    Returns
    -------
    dict
        Dictionary of all subsections and their data
    """
    parsed = {}
    if parser[section]['keys'] is not None:
        section_keys = re.split(r',\s*', parser[section]['keys'])
    else:
        section_keys = []
    for item in parser.sections():
        splist = item.split('.')
        try:
            if splist[0] == section and splist[1] in section_keys:
                parsed[splist[1]] = _valueize(parser[item])
        except IndexError:
            pass
    return parsed


def _findToken(name: str) -> str:
    r"""Search sources for client token.

    Check environment and .env file for token.

    Parameters
    ----------
    name
        Token name to search for

    Returns
    -------
    str
        Client token or None if no token was found
    """
    token = None
    if name in os.environ:
        logger.info(f'{name} found in environment')
        token = os.environ[name]
    else:
        try:
            with open('.env') as envfile:
                for line in envfile:
                    line = line.strip().split('=')
                    if line[0] == name:
                        token = line[1]
                        logger.info(f'{name} found in .env file')
        except (OSError, IndexError):
            pass
    if token is None:
        logger.warning(f'{name} was not found!')
    return token


if __name__ == "__main__":
    sys.exit(main())
