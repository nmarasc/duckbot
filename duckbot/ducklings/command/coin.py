# Duckbot util modules
from duckbot.util.common import roll

# Valid command names
NAMES = [
    'COIN'
]

# Command help variables
PURPOSE = 'Flip a coin'
USAGE = f'Usage: {{bot}} {NAMES[0]}'

# Flip a coin
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list of command arguments, **unused**
# Return: String containing the response
def handle(user, channel, cmd_args):
    result = roll(2)
    # Save a branch half of the time by assuming one
    face = 'TAILS'
    if result == 1:
        face = 'HEADS'
    return f'You got: {face}'

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args):
    return f'{PURPOSE}\n{USAGE}'
