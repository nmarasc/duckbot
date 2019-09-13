from util.common import roll
from util.rangeDict import rangedict
from util.common import bank

# Valid command names
NAMES = [
    'PULL'
]

# Command help variables
PURPOSE = 'Spend your bucks on gacha'
USAGE = (
    f'Usage: <@{{id}}> {NAMES[0]} [#-of-pulls]\n'
    f'Up to 10 pulls may be done at once :duck:'
)

# Module constants
GACHA_NAMES = [
        'Trash',
        'Common',
        'Uncommon',
        'Rare',
        'Super Rare',
        'Ultra Rare',
        'SS Ultra Secret Rare',
        '1000-chan'
]
GACHA_RANGES = rangedict({
    range(50, 150): 0,
    range(150, 600): 1,
    range(600, 800): 2,
    range(800, 900): 3,
    range(900, 975): 4,
    range(975, 990): 5,
    range(990, 1000): 6,
    range(1000, 1001): 7
})
PULL_MAX = max(max(GACHA_RANGES, key=lambda key: max(key)))
PULL_RANGE = range(1, 11)
PULL_COST = 10

ERROR = {
    'BAD_PULL': (
        'Invalid number of pulls: {}\n'
        f'Allowed range is {min(PULL_RANGE)} to {max(PULL_RANGE)}'
    )
}

# Spend on gacha draws
# Params: user     - user id of player
#         channel  - channel id playing from
#         cmd_args - list containing argument text
# Return: String response from command


def handle(user, channel, cmd_args):

    # Parse out bet arguments
    amount = _parsePullArgs(cmd_args)
    # Check gambling eligibility and argument validity
    status = _checkStatus(user, channel)
    if status['return_code']:  # Some error with status check
        response = status
    else:  # No status error, time to pull
        response = _pull(user, amount)
    return response

# Retrieve command help message
# Params: args - help arguments
# Return: String help message


def getHelp(args):
    return f'{PURPOSE}\n{USAGE}'

# Buy a gacha pull
# Params: user    - uid of player
#         amount  - number of pulls to do
# Return: Message containing results


def _pull(user, amount):
    message = ''

    if bank.hasFreePull(user):  # Free daily pull available
        bank.setFreePull(False, user)
        message = f'Free daily pull results: {_doPull()}\n\n'

    # Check range and total cost
    if amount in PULL_RANGE:
        if amount * PULL_COST <= balance.check(user):
            bank.deduct(user, amount * PULL_COST)
            message += f'Your pull results: {_doPull(amount)}'
        else:
            message += (
                f"{bank.ERROR['LOW_BALANCE']}\n"
                f'{balance.check(user)}'
            )
    else:
        message += ERROR['BAD_PULL'].format(amount)

    return message


def _doPull(amount=1):
    result = ''
    nuked = False
    while amount and nuked == False:
        pull = roll(PULL_MAX)
        if pull >= 50:  # Good pull
            name = GACHA_NAMES[pull]
            taken = bank.addPool(pull, user)
            if taken == user:  # Normal accquire
                result += '\nYou have received a {name}'
            elif taken:  # Stolen
                result += '\nYou have stolen a {name} from <@{taken}>'
            else:  # None available
                result += '\nThere were no more {name} available'
        elif pull > 1:  # Pull is less than 50
            removed = bank.removeBest(user)
            if removed < 0:  # Nothing to lose
                response += bank.MESSAGE['NO_LOSS']
            else:
                name = GACHA_NAMES[removed]
                if pull == GACHA_RANGES[PULL_MAX]:  # Lost big
                    result += (
                        '\nYou have disappointed {name}. '
                        'She returns back to the pool'
                    )
                else:  # Lost best
                    result += '\nYou lost a {name}'
        else:  # Rolled a 1
            bank.nuke()
            result = bank.MESSAGE['NUKE']
            nuked = True
    # Send back results
    return result

# Parse argument string for pull arguments
# Params: args - list of options to parse out
# Return: parsed argument list
def _parsePullArgs(args):
    try:
        # $$$ I can't tell whether a user typed -1 or garbage text with
        #     this function, it may need to be changed later
        result = parseNum(args[0])
        # Just ignore the problem for now
        if result == -1:
            result = 1
    except IndexError:  # Empty args
        result = 1
    return result

# Check the eligibilty of user and channel for this command
# Params: user    - user id issuing command
#         channel - channel id command issued from
# Return: dict with return code and status message
def _checkStatus(user, channel):
    message = ''
    return_code = bank.checkEligible(user, channel)
    if return_code == 1:  # Not a member
        message = bank.ERROR['NOT_A_MEMBER'].format(user)
    elif return_code == 2:  # Bad channel
        message = bank.ERROR['BAD_CHANNEL'].format(channel)
    return {'return_code': return_code, 'message': message}
