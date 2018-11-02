# Duckbot util modules
from util.common import matchUserID
from util.common import bank

# Valid command names
NAMES = [
    'CHECKBUX'
]

# Command help message
HELP = (
    'Check bank balance of yourself or others\n'
    f'Usage: <@{{id}}> {NAMES[0]} [target]\n'
    'No target defaults to yourself :duck:'
)

# Command responses
RESPONSES = {
    'SELF': f'You currently have {{}} {bank.CURRENCY}'
    'TARGET': f'<@{{}}> currently has {{}} {bank.CURRENCY}'
}

# Check bank balance of a user
# Params: user     - user id requesting a balance
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing target user
# Return: String response from command
def handle(user, channel, cmd_args):
    target = None
    if cmd_args:  # Check for target user option
        target = matchUserID(cmd_args[0])
        if target:
            user = target
    balance = _checkUser(user)
    if not balance:  # User was not a member
        response = bank.ERROR['NOT_A_MEMBER'].format(user)
    elif target:  # User was a target
        response = RESPONSES['TARGET'].format(target, balance)
    else:  # User was not a target
        response = RESPONSES['SELF'].format(balance)
    return response

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args):
    return HELP

# Determine eligibility of user id and get balance
# Params: user - user id to check
# Return: integer balance of user or None
def _checkUser(user):
    # Note: Channel is being omitted from this check since CHECKBUX
    #   command is valid in any channel, so the related return code
    #   does not need to be checked
    result = None
    return_code = bank.checkEligible(user)
    if return_code == 0:  # User is a member
        result = bank.balance(user)
    return result
