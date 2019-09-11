#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Main driver script for Duckbot.

This script handles program setup (commmand line parsing, logging
config, etc) and then starts Duckbot.
"""
# Last Updated: 1.0
# Python imports
import sys, os
import time, re, ast
import logging, logging.config
import argparse
from configparser import ConfigParser, ExtendedInterpolation

# Duckbot imports
from duckbot import Duckbot
from duckbot import EXIT_CODES
##FIXME don't reach into the bowels of the package
from duckbot.util.config import _valueize

# Configuration file paths
CONFPATH_LOG = '.config/logging.conf'
CONFPATH_BOT = '.config/bot.conf'


def main() -> int:
    r"""Mainline entry point.

    Create and run a Duckbot instance with supplied command line
    arguments and config file options.

    Returns
    -------
    int
        Exit code from the bot (documented in ##TODO)
    """
    # The logger is allowed to be global to the module, since
    # everything uses it.
    global logger

    args = parseCommandLine()

    log_conf = parseLogConfig(args)
    logging.config.dictConfig(log_conf)
    logger = logging.getLogger(__name__)
    logger.info('Logging configured and initialized')

    duckbot = duckboot()

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


def duckboot() -> Duckbot:
    r"""Create a Duckbot instance.

    Search for client tokens and instantiate a bot instance. If no
    tokens are found, the bot is not created.

    Returns
    -------
    Duckbot
        Duckbot instance or None on failure
    """
    config = {
        'slack' = CONNECT_SLACK,
        'discord' = CONNECT_DISCORD
    }

    if CONNECT_SLACK:
        config['slack_token'] = _findToken('SLACK_TOKEN')
    if CONNECT_DISCORD:
        config['discord_token'] = _findToken('DISCORD_TOKEN')

    duckbot = Duckbot(config)

    return duckbot


def parseLogConfig(args: dict) -> dict:
    r"""Parse config file for logging.

    Gather logging configuration data and then massage the data into a
    valid format. Any command line flags that affect logging
    configuration are read and handlers are adjusted. The log
    directory specified is created if it does not already exist.

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

    logConfig = _valueize(parser['general'])
    logConfig['root'] = {**parser['root']}
    logConfig['root']['handlers'] = re.split(
        ',\s*',
        logConfig['root']['handlers']
    )
    logConfig['formatters'] = _parseSubsection('formatters', parser)
    logConfig['handlers'] = _parseSubsection('handlers', parser)
    logConfig['loggers'] = _parseSubsection('loggers', parser)

    if args.debug:
        logConfig['handlers']['default']['level'] = 'DEBUG'
        logConfig['handlers']['console']['level'] = 'DEBUG'
    if args.verbose:
        logConfig['root']['handlers'].append('console')
    if args.temporary:
        logConfig['root']['handlers'].remove('default')

    # The log file is created at config time, so the path has to exist
    # before configuration happens
    os.makedirs(parser['paths']['log_dir'], exist_ok=True)
    return logConfig


def parseCommandLine() -> dict:
    r"""Parsing function for command line arguments.

    Utilize the ``argparse`` package to handle gathering and parsing
    of command line arguments.

    Returns
    -------
    dict
        Command line arguments with their values
    """
    # Use the script docstring as part of the usage message
    cl_parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
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
        '-t', '--temporary', action='store_true',
        help='\tdo not write values out to disk')
    return cl_parser.parse_args()


def _parseSubsection(section: str, parser: ConfigParser) -> dict:
    r"""Aggragate subsection data from the parser.

    Use the ``keys`` field of a section to determine subsections and
    gather all subsections into a single dictionary.

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
        section_keys = re.split(',\s*', parser[section]['keys'])
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


def _findToken(name: str, config: dict) -> str:
    r"""Search sources for client token.

    Check provided config, environment and .env file for token.

    Parameters
    ----------
    name
        Token name to search for
    config
        Bot config options

    Returns
    -------
    str
        Client token or None if no token was found
    """
    token = None
    if name in config:
        logger.info(f'{name} found in config options')
        token = config[name]
    elif name in os.environ:
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
            logger.warning(f'{name} was not found!')
    return token


# Connect to the rtm and test connection
# Params: None
# Return: 0 if connection went okay
#         Non zero if there was an error
def connect():
#{{{
    # Connect to the rtm
    if util.sc.rtm_connect(with_team_state=False):
    #{{{
        event_list = []
        # Wait for the connection event
        while not event_list:
            event_list = util.sc.rtm_read()
        event = event_list.pop(0)
        if event["type"] == "hello":
            # Connection was good
            util.logger.log(DiagMessage("INI0040I"))
            return 0
        else:
            # Error in connection
            error = event["error"]
            util.logger.log(DiagMessage("INI0040E",error["msg"]))
            util.logger.log(DiagMessage("INI0041E",str(error["code"])))
            return util.EXIT_CODES["RTM_BAD_CONNECTION"]
    #}}}
    # RTM connect failed
    else:
        util.logger.log(DiagMessage("INI0042E"))
        return util.EXIT_CODES["RTM_CONNECT_FAILED"]
#}}}

# Running loop, polls for events and hands them to the bot, ticks
# Params: duckbot - Duckbot instance
# Return: Bot exit code (documented in util.py)
def run(duckbot):
    if util.debug:
        util.logger.log(DiagMessage("INI0050D"))
    else:
        util.logger.log(DiagMessage("INI0050I"))

    running = True
    return_code = 0
    # Keep going until bot signals to stop
    while running:
        # Pause between reads to reduce the cycles spent spinning
        # Delay may need to be adjusted if bot feels sluggish
        time.sleep(util.RTM_READ_DELAY)

        return_code, event_list = doRead()
        if event_list and not return_code:
            # Process all the events returned
            for event in event_list:
                return_code, message = duckbot.handleEvent(event)
                if return_code == 0:
                    messenger.send(message)
                elif return_code == 1:
                    print(message)
                else:
                    # Ignore unknown event type
                    return_code = 0
        # Tick bot internal counter
        duckbot.tick()
        if return_code:
            running = False
    # Bot signalled to stop, return to mainline
    return return_code

# Attempt an rtm_read, catching errors on failure
# Params: None
# Return: 0 return code and populated event list on success
#         Non 0 return code and None on failure
def doRead():
#{{{
    # Attempt to do rtm read, except errors
    # When new errors are experienced, they will be added specifically
    try:
        event_list = util.sc.rtm_read()
        return 0, event_list
    except TimeoutError:
        util.logger.log(DiagMessage("BOT0031E"))
        return util.EXIT_CODES["RTM_TIMEOUT_ERROR"], None
    except Exception as err:
        print("Error: RTM read failed")
        print(err,file=sys.stderr)
        util.logger.log(DiagMessage("BOT0030E"))
        return util.EXIT_CODES["RTM_GENERIC_ERROR"], None
#}}}

# Call main function
if __name__ == "__main__":
    sys.exit(main())
