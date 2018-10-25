# Duckbot util modules
from util.common import matchUserId
from util.common import bank

# Valid command names
NAMES = [
    'CHECKBUX'
]

# Command responses
RESPONSES = {
    "SELF": f'You currently have {{}} {bank.CURRENCY}'
    "TARGET": f'<@{{}}> currently has {{}} {bank.CURRENCY}'
    "TARGET_BAD": '<@{}> is not currently registered for this system :duck:'
}

# Check bank balance of a user
# Params: args - Dict of arguments containing:
#   user    - user id requesting balance
#   channel - channel id command was issed from, **unused**
#   ops     - list containing target user
# Return: String response from command
def handle(**args):
    user = args["user"]
    ops = args["ops"]
    target = None
    if ops:  # Check text for target user
        target = matchUserId(ops[0])
    if target:  # Valid target id
        return_code = bank.checkEligible(target)
        if return_code == 0:  # Target is a member
            balance = bank.balance(target)
            response = RESPONSES["TARGET"].format(target, balance)
        else:  # Target is not a member
            response = bank.ERRORS["TARGET_NOT_A_MEMBER"].format(target)
    else:  # No target
        return_code = bank.checkEligible(user)
        if return_code == 0:  # User is a member
            balance = self.bank.balance(user)
            response = RESPONSES["SELF"].format(balance)
        else:  # User is not a member
            response = bank.ERRORS["NOT_A_MEMBER"]
    return response
