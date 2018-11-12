# Duckbot util modules
from util.common import bank

# Valid command names
NAMES = [
    'POOL',
    'COLLECTION',
]

# Command help variables
PURPOSE = 'Check the gacha pool of yourself or a user\n'
USAGE = (
    f'Usage <{{id}}> {NAMES[0]} [target]\n'
    'No target defaults to yourself :duck:'
)
HELP = f'{PURPOSE}{USAGE}'

# Command responses
RESPONSES = {
    'SELF': 'You currently have:\n{}',
    'TARGET': '<@{}> currently has:\n{}'
}

# Check gacha collection of a user
# Params: user   - user id to get collection of
#         target - True if user was a target
# Return: String message from subcommand
def check(user, target):
    pool = bank.getPool(user)
    for poolID in range(0, len(pool)):
        pool[poolID] = f'{pool[poolID]} {bank.GACHA_NAMES[poolID]}'
    result = "\n".join(pool)
    if target:
        response = RESPONSES['TARGET'].format(user, result)
    else:
        response = RESPONSES['SELF'].format(result)

# Retrieve command help message
# Params: None
# Return: String help message
def getHelp():
    return HELP
