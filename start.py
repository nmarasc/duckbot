#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main driver script for Duckbot.

This script handles program setup (commmand line parsing, config file
reading, etc) and then starts Duckbot.
"""
# Last Updated: 1.0
# Python imports
import sys
import os
import time
import argparse
import logging

# Slack import
from slackclient import SlackClient

# Project imports
from config.logger import loggerConfigDict

import duckbot.util.common as util
# from duckbot.util.diagMessage import DiagMessage
# from duckbot.util.logger import Logger

from duckbot.core import Duckbot

# The logger is allowed to be global to the module, everything uses it
global logger



def main():
    """Mainline entry point.

    Create and run a Duckbot instance with supplied command line
    arguments and config file options.

    Returns
    -------
    int
        Exit code from the bot (documented in ##FIXME)
    """
#     bot_args = parseCommandLine()
#     bot_conf = parseConfig()
    initProgram()
    return_code, duckbot = duckboot()
    if not return_code:
        return_code = run(duckbot)
    util.logger.log(DiagMessage("LOG0011I"), flush=True)
    return return_code


def parseCommandLine():
    """Parsing function for command line arguments.

    Utilize the ``argparse`` package to handle gathering and parsing
    of command line arguments.

    Returns
    -------
    dict
        Command line arguments with their values
    """
    # Use the script's docstring as part of the usage message
    cl_parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    cl_parser.add_argument(
        '-d', '--debug', action='store_true',
        help='\tadd debug messages to the log')
    cl_parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='\tprint log messages to the console')
    cl_parser.add_argument(
        '-t', '--temporary', action='store_true',
        help='\tdo not write values out to disk')
#     cl_parser.add_argument('--debug', action='store_true')
#     cl_parser.add_argument('--nolog', dest='log', action='store_false', default=True)
#     cl_parser.add_argument('--nobnk', dest='bnk', action='store_false', default=True)
    return cl_parser.parse_args()


# Initial program set up
#   - Command line parsing and directory changing
# Params: None
# Return: None
def initProgram():
#{{{
    util.debug = args.debug
    util.bank_file = args.bnk

    # Start the logger with logging mode
    util.logger = Logger(log=args.log)
    util.logger.log(DiagMessage("INI0000I"))
#}}}

# Set up and start the bot
# Params: None
# Return: 0 return code and Duckbot instance on success
#         Non 0 return code and None on failure
# Credit: Name courtesy of Katie. What a thinker, what a genius, wow
def duckboot():
    # Check for environment variable
    try:
        bot_token = os.environ["BOT_TOKEN"]
        print("Got token from env")
    except KeyError:
        # TODO: Log env variable not found
        try:
            # Get bot token from the env file
            with open("../.env") as env_file:
                bot_token = env_file.readline().rstrip().split("=")[1]
            print("Got token from file")
        # Can't open file or doesn't exist
        except OSError:
            # Exit because there is no token to connect with
            # TODO: Make no token error code
            print("No token found")
            return -1, None

    util.logger.log(DiagMessage("INI0010I", bot_token))

    # Create the slack client
    util.sc = SlackClient(bot_token)
    util.logger.log(DiagMessage("INI0020I"))

    # Get bot info
    bot_str, bot_channels = util.getBotInfo(bot_token)
    bot_id = util.matchUserID(bot_str)
    if not bot_id:
        util.logger.log(DiagMessage("INI0030E",bot_str))
        return util.EXIT_CODES["INVALID_BOT_ID"], None
    util.logger.log(DiagMessage("INI0030I",bot_id))

    # Connect to rtm and create bot if successful
    return_code = connect()
    if return_code:
        return return_code, None
    else:
        return return_code, Duckbot(bot_id, bot_channels)

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

# Running loop, polls for events and hands them to the bot, then ticks the bot
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
        # Delay may need to be adjusted if bot feels sluggish to respond
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
