# Valid command names
NAMES = [
    'FACT',
    'FACTOID'
]

# Command help variables
PURPOSE = 'Pull out a random and totally true fact'
USAGE = f'Usage: <@{{id}}> {NAMES[0]}'

# Generate a random ad lib fact
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list of command arguments, **unused**
# Return: String containing response from command
def handle(user, channel, cmd_args):
    return 'Not yet. Kweh :duck:'

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args):
    return f'{PURPOSE}\n{USAGE}'
