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
    "Pick from a number of things\n"
    "Usage: <@{id:s}> " + NAMES[0] + " <item1> <item2> ...\n"
    "Use quotes to have items with spaces in them :duck:"
)

PICK_RANGE = range(2, 21)  # Pick between 2 and 20 things

# Randomly pick from a list of specified items
# Params: args - dict of arguments containing:
#   user    - user id of command issuer
#   channel - channel id command was issued from
#   ops     - list containing items to pick from
# Return: String containing response from command
def handle(**args):
    ops = args["ops"]
    if len(ops) in PICK_RANGE:
        response = "I choose: " + ops[roll(len(args))-1]
    else:
        response = ("Must pick between " + str(min(PICK_RANGE)) +
                    " and " + str(max(PICK_RANGE)))
    return response

# Retrieve command help message
# Params: ops - help options, **unused**
# Return: String help message
def getHelp(ops):
    return HELP
