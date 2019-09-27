# -*- coding: utf-8 -*-
from typing import Union, List
import logging

from duckbot.util.common import roll
from duckbot.util.common import parseNum
from duckbot.util.rangeDict import rangedict
from duckbot.util.common import bank
from duckbot.util.bank import GACHA_NAMES

logger = logging.getLogger(__name__)

DISABLED = True

# Valid command names
NAMES = [
    'PULL'
]

# Command help variables
_PURPOSE = 'Spend your bucks on gacha'
_USAGE = (
    f'Usage: {{bot}} {NAMES[0]} [#-of-pulls]\n'
    f'Up to 10 pulls may be done at once :duck:'
)

# Module constants
_GACHA_RANGES = rangedict({
    range(50, 150): 0,
    range(150, 600): 1,
    range(600, 800): 2,
    range(800, 900): 3,
    range(900, 975): 4,
    range(975, 990): 5,
    range(990, 1000): 6,
    range(1000, 1001): 7
})
_PULL_MAX = max(max(_GACHA_RANGES, key=lambda key: max(key)))
_PULL_RANGE = range(1, 11)
_PULL_COST = 10

_ERROR = {
    'BAD_PULL': (
        'Invalid number of pulls: {}\n'
        f'Allowed range is {min(_PULL_RANGE)} to {max(_PULL_RANGE)}'
    ),
    'NOT_A_MEMBER': (
        'You are not a member of the bank. Please join to do pulls :duck:'
    )
}

# This is set during initialization
bank = None


def handle(user: int, channel: int, args: List[str]):
    r"""Spend bucks on gacha draws.

    Parameters
    ----------
    user
        Player id that issued the command
    channel
        Channel id the command was issued from
    args
        Command arguments

    Returns
    -------
    str
        Command response text
    """
    try:
        amount = parseNum(args[0])
    except IndexError:
        amount = 1
    # Check gambling eligibility and argument validity
    if bank.isMember(user):
        response = _pull(user, amount)
    else:
        response = _ERROR['NOT_A_MEMBER']
    return response


def getHelp(args):
    r"""Retrieve command help message.

    Parameters
    ----------
    args
        Help arguments, unused

    Returns
    -------
    str
        Help message
    """
    return f'{_PURPOSE}\n{_USAGE}'

# Buy a gacha pull
# Params: user    - uid of player
#         amount  - number of pulls to do
# Return: Message containing results


def _pull(user: int, amount: Union[int, str]):
    r"""Buy gacha pulls

    Parameters
    ----------
    user
        Player id pulling
    amount
        Number of pulls being done

    Returns
    -------
    str
        Result message
    """
    message = ''

    if bank.hasFreePull(user):
        bank.setFreePull(False, user)
        message = f'Free daily pull results: {_doPull()}\n\n'

    if type(amount) is int and amount in _PULL_RANGE:
        if amount * _PULL_COST <= balance.check(user):
            bank.deduct(user, amount * _PULL_COST)
            message += f'Your pull results: {_doPull(amount)}'
        else:
            message += (
                f"{bank.ERROR['LOW_BALANCE']}\n"
                f'{balance.check(user)}'
            )
    else:
        message += _ERROR['BAD_PULL'].format(amount)

    return message


def _doPull(amount=1):
    result = ''
    nuked = False
    while amount and nuked == False:
        pull = roll(_PULL_MAX)
        if pull >= 50:  # Good pull
            name = _GACHA_NAMES[pull]
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
                name = _GACHA_NAMES[removed]
                if pull == _GACHA_RANGES[_PULL_MAX]:  # Lost big
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
def _parsePullArgs(args: List[str]):
    r"""Parse argument string for pull command.

    Parameters
    ----------
    args
        Command arguments

    Returns
    -------
    int
    """

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
