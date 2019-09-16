# Duckbot util modules
from duckbot.util.common import bank

# Valid command names
NAMES = [
    'JOIN'
]

# Command help variables
PURPOSE = 'Add yourself to the gambling system'
USAGE = (
    f'Usage: <@{{id}}> {NAMES[0]}\n'
    'Can only be used in gambling approved channels :duck:'
)

# Command responses
RESPONSES = {
    'ADDED': (
        'You have been added to the gambling system :duck:\n'
        f'You have {bank.STARTING_BUX} {bank.CURRENCY}'
    ),
    'EXISTS': (
        'You are already a member of this system :duck:\n'
        f'You have {{}} {bank.CURRENCY}'
    )
}

# Add user to gamling system if not already
# Params: user     - user id issuing command
#         channel  - channel id command was issued from
#         cmd_args - list of command arguments, **unused**
# Return: String response from the command
def handle(user, channel, cmd_args):
    return_code = bank.checkEligible(user, channel)
    if return_code == 0:  # User already a member
        response = RESPONSES['EXISTS'].format(bank.balance(user))
    elif return_code == 1:  # User not a member
        bank.addUser(user)
        response = RESPONSES['ADDED']
    else:  # Invalid channel
        response = bank.ERROR['BAD_CHANNEL']
    return response

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args):
    return f'{PURPOSE}\n{USAGE}'
