# Duckbot util modules
from util.common import roll

# Valid command names
NAMES = [
    'PICK',
    'PICKIT',
    'PIKMIN'
]

PICK_RANGE = range(2, 21)  # Pick between 2 and 20 things

# Randomly pick from a list of specified items
# Params: args - list containing items to pick from
# Return: String containing response from command
def handle(args):
    if len(args) in PICK_RANGE:
        response = "I choose: " + args[roll(len(args))-1]
    else:
        response = ("Must pick between " + str(min(PICK_RANGE)) +
                    " and " + str(max(PICK_RANGE)))
    return response
