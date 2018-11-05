# Duckbot util modules
from util.common import bank

# Valid command names
NAMES = [
    'CHECKPOOL'
]

# Command help message
HELP = (
    'Check the gacha pool of yourself or a user\n'
    f'Usage <{{id}}> {NAMES[0]} [target]\n'
    'No target defaults to yourself :duck:'
)

# Command responses
RESPONSES = {
    'SELF': 'You currently have:\n{}'
    'TARGET': '<@{}> currently has:\n{}'
}

# Check gacha collection of a user
# Params: user     - user id requesting collection
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing command argument text
# Return: Message containing collection
def handle(user, channel, cmd_args):
    target = None
    if cmd_args:  # Check for target user option
        target = matchUserID(cmd_args[0])
        if target:
            user = target
    collection = _checkUser(user)
    if not collection:
        response = bank.ERROR['NOT_A_MEMBER'].format(user)
    elif target:
        response = RESPONSES['TARGET'].format(target, collection)
    else:
        response = RESPONSES['SELF'].format(collection)
    return response

# Determine eligibility of user id and get collection
# Params: user - user id to check
# Return: String gacha collection of user or None
def _checkUser(user):
    # Note: Channel is being omitted from this check since CHECKPOOL
    #   command is valid in any channel, so the related return code
    #   does not need to be checked
    result = None
    return_code = bank.checkEligible(user)
    if return_code == 0:  # User is a member
        pool = bank.getPool(user)
        for poolID in range(0, len(pool)):
            pool[poolID] = f'{pool[poolID]} {bank.GACHA_NAMES[poolID]}'
        result = "\n".join(pool)
    return result
