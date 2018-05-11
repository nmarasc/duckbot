# Python imports
import sys
import os
import time
import argparse

# Slack import
from slackclient import SlackClient

# Project imports
import util
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
    logger.log("FLUSH    : Clearing buffer before exit", flush=True)
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
    args = cl_parser.parse_args()
    global debug_g, log_g
    debug_g = args.debug
    log_g = args.log
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

    # Start the logger with logging mode
    global logger
    logger = util.Logger(log=log_g)
    logger.log("BOT TOKEN: " + bot_token)

    # Create the slack client
    global sc
    sc = SlackClient(bot_token)
    # Get bot info
    bot_id, bot_channels = util.getBotInfo(sc, bot_token)
    if not util.matchUserId(bot_id):
        logger.log("BAD ID   : " + bot_id)
        return util.EXIT_CODES["INVALID_bot_id"], None

    # Connect to rtm and create bot if successful
    return_code = connect()
    if return_code:
        return return_code, None
    else:
        return return_code, Duckbot(sc, bot_id, bot_channels, logger, debug_g)
#}}}

# Connect to the rtm and test connection
# Params: None
# Return: 0 if connection went okay
#         Non zero if there was an error
def connect():
#{{{
    # Connect to the rtm
    if sc.rtm_connect(with_team_state=False):
    # {{{
        event_list = []
        # Wait for the connection event
        while not event_list:
            event_list = sc.rtm_read()
        event = event_list.pop(0)
        if event["type"] == "hello":
            # Connection was good
            return 0
        else:
            # Error in connection
            error = event["error"]
            logger.log("CON ERROR: " + error["msg"])
            logger.log(" --  CODE: " + str(error["code"]))
            return util.EXIT_CODES["RTM_CONNECT_FAILED"]
    #}}}
    # RTM connect failed
    else:
        logger.log("CON ERROR: Failed to connect to RTM")
        return util.EXIT_CODES["RTM_CONNECT_FAILED"]
#}}}

# Running loop, polls for events and hands them to the bot, then ticks the bot
# Params: duckbot - Duckbot instance
# Return: Bot exit code (documented in util.py)
def run(duckbot):
#{{{
    if debug_g:
        logger.log("DEBUG    : Duckbot running in debug mode")

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
        event_list = sc.rtm_read()
        return 0, event_list
    except TimeoutError:
        logger.log("RTM ERROR: TimeoutError")
        return util.EXIT_CODES["RTM_TIMEOUT_ERROR"], None
    except:
        logger.log("RTM ERROR: RTM read failed")
        return util.EXIT_CODES["RTM_GENERIC_ERROR"], None
#}}}

# Call main function
if __name__ == "__main__":
    sys.exit(main())
