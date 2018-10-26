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
    user = args['user']
    ops = args['ops']
    target = None
    if ops:  # Check text for target user
        target = matchUserId(ops[0])
    if target:  # Valid target id
        response = _checkUser(target, True)
    else:  # Invalid or missing target id
        response = _checkUser(user)
    return response

# Retrieve command help message
# Params: ops - help options, **unused**
# Return: String help message
def getHelp(ops):
    return HELP

# Determine eligibility of user id and get balance
# Params: uid    - user id to get balance of
#         target - True if user is a target
def _checkUser(uid, target=False):
    # Note: Channel is being omitted from this check since CHECKBUX
    #   command is valid in any channel, so the related return code
    #   does not need to be checked
    return_code = checkEligible(uid)
    if return_code == 0:  # User is a member
        balance = bank.balance(uid)
        if target:
            result = RESPONSES['TARGET'].format(uid, balance)
        else:
            result = RESPONSES['SELF'].format(balance)
    else:  # User is not a member
        result = bank.ERROR['NOT_A_MEMBER'].format(uid)
    return result
