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
    args = cl_parser.parse_args()
    global DEBUG
    DEBUG = args.debug
    # Get bot token from the env file
    with open(".env") as env_file:
        bot_token = env_file.readline().rstrip().split("=")[1]
    print("Token: " + bot_token)

    # Create the slack client
    global sc
    sc = SlackClient(bot_token)
    # Get bot info
    bot_id, bot_channels = util.getBotInfo(sc, bot_token)
    if not util.matchUserId(bot_id):
        print("Invalid bot id: " + bot_id)
        sys.exit(EXIT_CODES["INVALID_BOT_ID"])

    # Connect to the rtm and build bot
    if sc.rtm_connect(with_team_state=False):
    # {{{
        global duckbot
        duckbot = Duckbot(sc, bot_id)

        # Wait for the connection event
        while not event_list:
            event_list = sc.rtm_read()
        event = event_list.pop(0)
        if event["type"] == "hello":
            # Connection was good
            exit_code = run()
        else:
            # Error in connection
            error = event["error"]
            print(error["msg"] + "\nCode: " + str(error["code"]))
            sys.exit(EXIT_CODES["RTM_CONNECT_FAILED"])
    #}}}

    # Connect failed and bot was not created
    else:
        print("Failed to connect to RTM")
        sys.exit(EXIT_CODES["RTM_CONNECT_FAILED"])

    sys.exit(exit_code)
#}}}

# Running loop
# Reads for rtm events
def run():
#{{{
    if DEBUG:
        print("Duckbot running in debug mode")

    RUNNING = True
    RETURN_CODE = 0

    # Keep going until bot signals to stop
    while RUNNING:
    #{{{
        RETURN_CODE, event_list = doRead()
        if event_list and not RETURN_CODE:
            # Process all the events returned
            # EVENTUALLY: Thread each event
            for event in event_list:
                RETURN_CODE = duckbot.handleEvent(event)
        if RETURN_CODE:
            RUNNING = False

        time.sleep(1)
    #}}}
    # Bot signalled to stop, exit with code
    sys.exit(RETURN_CODE)
#}}}

# Attempt an rtm_read, catching errors on failure
# event_list populated on success, Null on failure
def doRead():
#{{{
    try:
        event_list = sc.rtm_read()
        return 0, event_list
    except TimeoutError:
        print("Error: TimeoutError")
        return EXIT_CODES["RTM_TIMEOUT_ERROR"], None
#}}}

# Call main function
if __name__ == "__main__":
    main()
