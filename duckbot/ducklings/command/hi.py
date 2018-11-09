# Valid command names
NAMES = [
    'HI',
    'HELLO'
]

# Command help message
PURPOSE = 'Legacy HI command\n'
USAGE = f'Usage: <@{{id}}> {NAMES[0]}'
HELP = f'{PURPOSE}{USAGE}'

# Say hello
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list of command arguments, **unused**
# Return: String containing command response
def handle(user, channel, cmd_args):
    return 'Kweh! :DUCK:'

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args):
    return HELP
