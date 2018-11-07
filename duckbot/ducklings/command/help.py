# Last Updated: 2.2

# Valid command names
NAMES = [
    'HELP',
    'HEP',
    '?',
    ':QUESTION:',
    ':GREY_QUESTION:'
]

# Command help message
HELP = (
    "Don't get smart, you know how to use this :duck:"
)

# General help message
DEFAULT_HELP = (
    'Duckbot is a general purpose slackbot for doing various things\n'
    'To interact with it use <@{{id}}> <command>\n'
    'Supported commands: {}\n'
    f'Use <@{{{id}}}> {NAMES[0]} <command> for more details'
)

# Command modules
# Since commands are loaded at runtime, this gets set by the event manager
COMMANDS = {}

# Get bot help messages
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing command argument text
# Return: String containing command response
def handle(user, channel, cmd_args):
    if cmd_args:  # Check for command
        command = COMMANDS.get(str.upper(cmd_args[0]), 0)
        if command:  # Was a command
            try:
                response = command.getHelp(cmd_args[1:])
            except AttributeError:
                # Somebody didn't define a help function :rage:
                response = f'No help defined for command: {command.NAMES[0]}'
        else:  # Invalid command
            response = f'{cmd_args[0]} is not a recognized command'
    else:  # Default help message
        command_names = [cmd.NAMES[0] for cmd in COMMANDS]
        response = DEFAULT_HELP.format(", ".join(command_names))
    return response

# Retrieve help command message
# Params: args - help command arguments, **unused**
# Return: String help message
def getHelp(args):
    return HELP

#            ,util.COMMANDS["BET"] :\
#                ("Bet on a game with bank balance to win big\n"
#                "Usage: <@" + bot_id + "> BET <amount> <game> <game-options>\n"
#                "List of currently supported games: " + ", ".join(util.GAMES) + "\n"
#                "Use HELP BET <game> for details on options")
#        self.game_help_messages = {
#             util.GAMES["COIN"] :\
#                ("Flip a coin and call it\n"
#                "Usage options: COIN ( H[EADS] | T[AILS] )")
#            ,util.GAMES["DICE"] :\
#                ("Roll the dice and guess even or odd\n"
#                "Usage options: DICE ( E[VENS] | O[DDS] )")
