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
