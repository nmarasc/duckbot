
# Valid command names
NAMES = [
    'FACT',
    'FACTOID'
]

HELP = (
    'Pull out a random and totally true fact\n'
    f'Usage: <@{{id}}> {NAMES[0]}'
)

# Generate a random ad lib fact
# Params: args - dict of arguments, **unused**
# Return: String containing response from command
def handle(**args):
    return 'Not yet. Kweh :duck:'

# Retrieve command help message
# Params: ops - help options, **unused**
# Return: String help message
def getHelp(ops):
    return HELP
