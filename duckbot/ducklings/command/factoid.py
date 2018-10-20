
# Valid command names
NAMES = [
    'FACT',
    'FACTOID'
]

HELP = (
    "Pull out a random and totally true fact\n"
    "Usage: <@{id:s}> " + NAMES[0]
)

# Generate a random ad lib fact
# Params: args - list of arguments, **unused**
# Return: String containing response from command
def handle(args=None):
    return "Not yet. Kweh :duck:"
