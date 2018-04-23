# Python imports
import sys
import time
import argparse

# Slack import
from slackclient import SlackClient

# Project imports
import util
from duckbot import Duckbot

# Mainline code
# Handles creation and deletion of bot
# Passes slack events to bot as well
def main():
#{{{
    event_list = []

    # Construct commandline parser
    cl_parser = argparse.ArgumentParser(description='Start up Duckbot')
    cl_parser.add_argument('--debug', action='store_true')
    cl_parser.add_argument('--nolog', dest='log', action='store_false', default=True)
    args = cl_parser.parse_args()
    global DEBUG
    DEBUG = args.debug

    logger = util.Logger(log=args.log)
    # Get bot token from the env file
    with open(".env") as env_file:
        bot_token = env_file.readline().rstrip().split("=")[1]
    logger.log("Token    : " + bot_token)

    # Create the slack client
    global sc
    sc = SlackClient(bot_token)
    # Get bot info
    bot_id, bot_channels = util.getBotInfo(sc, bot_token)
    if not util.matchUserId(bot_id):
        print("Invalid bot id: " + bot_id)
        sys.exit(util.EXIT_CODES["INVALID_BOT_ID"])

    # Connect to the rtm and build bot
    if sc.rtm_connect(with_team_state=False):
    # {{{
        duckbot = Duckbot(sc, bot_id, logger)

        # Wait for the connection event
        while not event_list:
            event_list = sc.rtm_read()
        event = event_list.pop(0)
        if event["type"] == "hello":
            # Connection was good
            exit_code = run(duckbot)
        else:
            # Error in connection
            error = event["error"]
            print(error["msg"] + "\nCode: " + str(error["code"]))
            sys.exit(util.EXIT_CODES["RTM_CONNECT_FAILED"])
    #}}}

    # Connect failed and bot was not created
    else:
        print("Failed to connect to RTM")
        sys.exit(util.EXIT_CODES["RTM_CONNECT_FAILED"])

    sys.exit(exit_code)
#}}}

# Running loop
# Reads for rtm events
def run(duckbot):
#{{{
    if DEBUG:
        print("Duckbot running in debug mode")

    RUNNING = True
    RETURN_CODE = 0

    # Keep going until bot signals to stop
    while RUNNING:
    # {{{
        time.sleep(1)
        RETURN_CODE, event_list = doRead()
        if event_list and not RETURN_CODE:
            # Process all the events returned
            # EVENTUALLY: Thread each event
            for event in event_list:
                RETURN_CODE = duckbot.handleEvent(event)
        duckbot.tick()
        if RETURN_CODE:
            RUNNING = False
    #}}}
    # Bot signalled to stop, return to mainline
    return RETURN_CODE
#}}}

# Attempt an rtm_read, catching errors on failure
# event_list populated on success, None on failure
def doRead():
#{{{
    try:
        event_list = sc.rtm_read()
        return 0, event_list
    except TimeoutError:
        print("Error: TimeoutError")
        return util.EXIT_CODES["RTM_TIMEOUT_ERROR"], None
    except:
        print("Error: RTM read failed")
        return util.EXIT_CODES["RTM_GENERIC_ERROR"], None
#}}}

# Call main function
if __name__ == "__main__":
    main()
