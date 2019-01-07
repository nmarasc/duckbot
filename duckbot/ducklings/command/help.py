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
HELP = "Don't get smart, you know how to use this :duck:"

# General help variables
PURPOSE = 'Duckbot is a general purpose slackbot for doing various things'
USAGE = (
    'To interact with it use <@{{id}}> <command>\n'
    'Supported commands: {}\n'
    f'Use <@{{{id}}}> {NAMES[0]} <command> for more details'
)

# Command responses
RESPONSES = {
    'BAD_CMD': '{} is not a recognized command',
    'NO_HELP': 'No help defined for command: {}'
}

# Command modules
# Since commands are loaded at runtime, this gets set by the event manager
COMMANDS = {}

# Get bot help messages
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing command argument text
# Return: String containing command response
def handle(user, channel, cmd_args):
    try:
        command = COMMANDS.get(str.upper(cmd_args[0]), None)
        response = command.getHelp(cmd_args[1:])
    except IndexError:  # No arguments, default help
        command_names = [cmd.NAMES[0] for cmd in COMMANDS]
        response = f'{PURPOSE}\n{USAGE}'.format(', '.join(command_names))
    except AttributeError:  # Invalid command or no help defined
        if not command:  # Command was invalid
            response = RESPONSES['BAD_CMD'].format(cmd_args[0])
        else:  # Somebody didn't define a help function :rage:
            response = RESPONSES['NO_HELP'].format(command.NAMES[0])
    return response

# Retrieve help command message
# Params: args - help command arguments, **unused**
# Return: String help message
def getHelp(args):
    return HELP
