# Python imports
import sys
import os
import time
import argparse

# Slack import
from slackclient import SlackClient

# Project imports
import util
from util import DiagMessage
from duckbot import Duckbot

# Mainline code
# Create a Duckbot and start running it
# Params: None
# Return: Bot exit code (documented in util.py)
def main():
#{{{
    initProgram()
    return_code, duckbot = duckboot()
    if not return_code:
        return_code = run(duckbot)
    util.logger.log(DiagMessage("LOG0011I"), flush=True)
    return return_code
#}}}

# Initial program set up
#   - Command line parsing and directory changing
# Params: None
# Return: None
def initProgram():
#{{{
    # Change context directory to the running one
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Construct command line parser and get arguements
    cl_parser = argparse.ArgumentParser(description='Start up Duckbot')
    cl_parser.add_argument('--debug', action='store_true')
    cl_parser.add_argument('--nolog', dest='log', action='store_false', default=True)
    cl_parser.add_argument('--nobnk', dest='bnk', action='store_false', default=True)
    args = cl_parser.parse_args()
    util.debug = args.debug
    util.bank_file = args.bnk

    # Start the logger with logging mode
    util.logger = util.Logger(log=args.log)
    util.logger.log(DiagMessage("INI0000I"))
#}}}

# Set up and start the bot
# Params: None
# Return: 0 return code and Duckbot instance on success
#         Non 0 return code and None on failure
# Credit: Name courtesy of Katie. What a thinker, what a genius, wow
def duckboot():
#{{{
    # Get bot token from the env file
    with open("../.env") as env_file:
        bot_token = env_file.readline().rstrip().split("=")[1]
    util.logger.log(DiagMessage("INI0010I", bot_token))

    # Create the slack client
    util.sc = SlackClient(bot_token)
    util.logger.log(DiagMessage("INI0020I"))

    # Get bot info
    bot_str, bot_channels = util.getBotInfo(bot_token)
    bot_id = util.matchUserId(bot_str)
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
#}}}

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
#{{{
    if util.debug:
        util.logger.log(DiagMessage("INI0050D"))
    else:
        util.logger.log(DiagMessage("INI0050I"))

    running = True
    return_code = 0
    # Keep going until bot signals to stop
    while running:
    # {{{
        # Pause between reads to reduce the cycles spent spinning
        # Delay may need to be adjusted if bot feels sluggish to respond
        time.sleep(util.RTM_READ_DELAY)

        return_code, event_list = doRead()
        if event_list and not return_code:
            # Process all the events returned
            for event in event_list:
                return_code = duckbot.handleEvent(event)
        # Tick bot internal counter
        duckbot.tick()
        if return_code:
            running = False
    # }}}
    # Bot signalled to stop, return to mainline
    return return_code
#}}}

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

    except _ as err:
        print("Error: RTM read failed")
        print(err,file=sys.stderr)
        util.logger.log(DiagMessage("BOT0030E"))
        return util.EXIT_CODES["RTM_GENERIC_ERROR"], None
#}}}

# Call main function
if __name__ == "__main__":
    sys.exit(main())
