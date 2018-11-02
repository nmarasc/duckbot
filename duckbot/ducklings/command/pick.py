# Duckbot util modules
from util.common import roll

# Valid command names
NAMES = [
    'PICK',
    'PICKIT',
    'PIKMIN'
]

# Command help message
HELP = (
    'Randomly pick from a list of items\n'
    f'Usage: <@{{id}}> {NAMES[0]} <item1> <item2> ...\n'
    'Use quotes to have items with spaces in them :duck:'
)

PICK_RANGE = range(2, 21)  # Pick between 2 and 20 things

# Randomly pick from a list of specified items
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list of items to pick from
# Return: String containing response from command
def handle(user, channel, cmd_args):
    cmd_len = len(cmd_args)
    if cmd_len in PICK_RANGE:
        pick = cmd_args[roll(cmd_len)-1]
        response = f'I choose: {pick}'
    else:
        response = 'Must pick between {} and {} items'.format(
            min(PICK_RANGE),
            max(PICK_RANGE)
        )
    return response

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(arguments):
    return HELP
