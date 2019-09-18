# Last Updated: 2.2
import logging

logger = logging.getLogger(__name__)

# Valid command names
NAMES = [
    'HELP',
    'HEP',
    'HALP',
    '?',
    ':QUESTION:',
    ':GREY_QUESTION:'
]

# Command help message
HELP = "Don't get smart, you know how to use this :duck:"

# General help variables
PURPOSE = 'Duckbot is a general purpose slackbot for doing various things'
USAGE = (
    'To interact with it use {{bot}} <command>\n'
    'Supported commands: {cmds}\n'
    'Use {{bot}} '
    f'{NAMES[0]} <command> for more details'
)

# Command responses
RESPONSES = {
    'BAD_CMD': '{} is not a recognized command',
    'NO_HELP': '{} has no help defined'
}

# Command modules
# Since commands are loaded at runtime, this gets set by the event manager
COMMANDS = {}

# Get bot help messages
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing command argument text
# Return: String containing command response
def handle(user, channel, args):
    logger.info(f'Processing {NAMES[0]} command')
    try:
        command = COMMANDS.get(str.upper(args[0]), None)
        response = command.getHelp(args[1:])
    except IndexError:  # No arguments, default help
        names = {cmd.NAMES[0] for cmd in COMMANDS.values()}
        response = f'{PURPOSE}\n{USAGE}'.format(cmds=', '.join(names))
    except AttributeError:  # Invalid command or no help defined
        if not command:  # Command was invalid
            logger.info(f'User entered invalid command for {NAMES[0]}')
            response = RESPONSES['BAD_CMD'].format(args[0])
        else:  # Somebody didn't define a help function :rage:
            logger.error('No help function defined for: {command.NAMES[0]}')
            response = RESPONSES['NO_HELP'].format(command.NAMES[0])
    return response

# Retrieve help command message
# Params: args - help command arguments, **unused**
# Return: String help message
def getHelp(args):
    return HELP
