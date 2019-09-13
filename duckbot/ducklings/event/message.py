# Last Updated: 2.2
# Python imports
import re
# Duckbot util modules
import util.common as util
from util.diagMessage import DiagMessage

# Command processor modules, loaded and set by the event manager
COMMANDS = {}

# Get command from event and call command handler
# Params: event - standardized event instance
# Return: dict with return code and message from command handler
def process(event):
    response = {'return_code': 0}
    # Extract command from event text
    cmd, cmd_args = _getCommand(event.text)
    try: # Attempt to call command handler
        response = COMMANDS[cmd].handle(event.user, event.channel, cmd_args)
        #TODO: check rc maybe
    except KeyError: # No command or unrecognized, ignore
        response['return_code'] = -1
        response['message'] = None
    return response
###
#     # HELP command
#     if command == util.COMMANDS["HELP"]:
#         return self.help_handler.act(u_parms)
#     # PULL command
#     elif command == util.COMMANDS["PULL"]:
#         amount = u_parms[0] if u_parms else None
#         return self.gamble_handler.pull(event.user, event.channel, amount)
###

# Parse message for mention, command, and parms
# Params: text - message text to parse
# Return: command word and params or None,None if no command
def _getCommand(text):
#{{{
    # Message event with no text? Don't even know if it's possible
    # But I'll stop it if it is
    if not text:
        return None, None

    # Break up the text and try to match the trigger with the bot_id
    text_arr = re.split(r'\s+',text.strip())
    trigger = text_arr.pop(0).upper()
    id_str = util.matchUserID(trigger)

    # FIXME: Where is the bot_id, how does this know who the bot is

    # Check for mention from id or trigger, then get command
    if ((id_str == self.bot_id) or
       (trigger   == ":DUCKBOT:")) and text_arr:
        c_word = text_arr.pop(0).upper()
        command = util.COMMANDS.get(c_word,0)
        command = util.COMMANDS_ALT.get(c_word,0) if not command else command
        return command, text_arr

    # No mention or no command word, ignore
    else:
        return None, None
#}}}
