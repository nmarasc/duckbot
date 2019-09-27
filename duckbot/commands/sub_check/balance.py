# Duckbot util modules
from duckbot.util.bank import CURRENCY

# Valid command names
NAMES = [
    'BUX',
    'DUX',
    'DOLANS',
    'BALANCE',
    ':MONEYBAG:',
    ':MONEY_WITH_WINGS:'
]

# Command help variables
PURPOSE = 'Check bank balance of yourself or others'
USAGE = (
    f'Usage: {NAMES[0]} [target]\n'
    'No target defaults to yourself :duck:'
)

# Command responses
RESPONSES = {
    'SELF': f'You currently have {{}} {CURRENCY}',
    'TARGET': f'<@{{}}> currently has {{}} {CURRENCY}'
}

# Check bank balance of a user
# Params: user   - user id to get balance of
#         target - True if user was a target
# Return: String response from subcommand
def check(user, target, bank):
    balance = bank.getBalance(user)
    if target:
        response = RESPONSES['TARGET'].format(user, balance)
    else:
        response = RESPONSES['SELF'].format(balance)
    return response

# Retrieve command help message
# Params: None
# Return: String help message
def getHelp():
    return f'{PURPOSE}\n{USAGE}'
