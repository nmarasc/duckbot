# Duckbot util modules
from util.common import roll

# Valid command names
NAMES = [
    "COIN"
]

# Flip a coin
# Params: args - list of arguments, **unused**
# Return: String containing the response
def handle(args=None):
    response = "You got: "
    result = roll(2)
    # Save a branch half of the time by assuming one
    response += "TAILS"
    if result == 1:
        response += "HEADS"
    return response
