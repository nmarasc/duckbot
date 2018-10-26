# Duckbot util modules
from util.common import ERROR_CODES
from util.common import bank

# Valid command names
NAMES = [
    'JOIN'
]

# Command help message
HELP = (
    'Add yourself to the gambling system\n'
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
# Params: args - dict containing:
#   user    - user id of the command issuer
#   channel - channel id command was issued from
#   ops     - list of command options, **unused**
# Return: Message to send to channel
def handle(**args):
    user = args['user']
    channel = args['channel']

    return_code = bank.checkEligible(user, channel)
    if return_code == 0:  # User already a member
        response = RESPONSES['EXISTS'].format(bank.balance(user))
    elif return_code == 1:  # User not a member
        self.bank.addUser(user)
        response = RESPONSES['ADDED']
    else:  # Invalid channel
        response = bank.ERRORS['BAD_CHANNEL']
    return response
