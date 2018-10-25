# Duckbot util modules
from util.common import roll

# Valid command names
NAMES = [
    "COIN"
]

# Command help messsage
HELP = (
    "Flip a coin\n"
    "Usage: <@{id:s}> " + NAMES[0]
)

# Flip a coin
# Params: args - dict of arguments, **unused**
# Return: String containing the response
def handle(**args):
    response = "You got: "
    result = roll(2)
    # Save a branch half of the time by assuming one
    response += "TAILS"
    if result == 1:
        response += "HEADS"
    return response

# Retrieve command help message
# Params: ops - help options, **unused**
# Return: String help message
def getHelp(ops):
    return HELP
