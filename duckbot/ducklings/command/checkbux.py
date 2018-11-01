# Duckbot util modules
from util.common import matchUserId
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
# Params: args - Dict of arguments containing:
#   user    - user id requesting balance
#   channel - channel id command was issed from, **unused**
#   ops     - list containing target user
# Return: String response from command
def handle(**args):
    ops = args['ops']
    target = None
    if ops:  # Check text for target user
        target = matchUserId(ops[0])

    # TODO: Dodge comparisons or give up and add it
    # temporary solution below
    user = args['user'] if not target else target

    balance = _checkUser(user)
    if not balance:
        response = bank.ERROR['NOT_A_MEMBER'].format(user)
    elif target:  # Valid target id
        response = RESPONSES['TARGET'].format(target, balance)
    else:  # Invalid or missing target id
        response = RESPONSES['SELF'].format(balance)
    return response

# Retrieve command help message
# Params: ops - help options, **unused**
# Return: String help message
def getHelp(ops):
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
