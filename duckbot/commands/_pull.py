# -*- coding: utf-8 -*-
from typing import Union, List
import logging

from duckbot.util.common import roll
from duckbot.util.common import parseNum
from duckbot.util.rangeDict import rangedict
from duckbot.util.common import bank
from duckbot.util.bank import GACHA_NAMES

logger = logging.getLogger(__name__)

DISABLED = False

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
    ),
    'LOW_BALANCE' : (
        "Your balance is too low to make this transaction"
    )
}
RESPONSES = {
    'NO_LOSS' : (
        "\nThat was a disappointing pull, but you had nothing to lose"
    ),
    'NUKE' : (
        "You have set off the nuke! Everyone has returned to the pool\n"
        "Let the shaming begin! :duck:"
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
        message = f'Free daily pull results: {_doPull(user)}\n\n'

    if type(amount) is int and amount in _PULL_RANGE:
        if amount * _PULL_COST <= bank.getBalance(user):
            bank.deduct(user, amount * _PULL_COST)
            message += f'Your pull results: {_doPull(user,amount)}'
        else:
            message += (
                f"{_ERROR['LOW_BALANCE']}: {bank.getBalance(user)}\n"
            )
    else:
        message += _ERROR['BAD_PULL'].format(amount)

    return message


def _doPull(user, amount=1):
    result = ''
    nuked = False
    while amount and nuked == False:
        pull = roll(_PULL_MAX)
        if pull >= 50:  # Good pull
            name = GACHA_NAMES[_GACHA_RANGES[pull]]
            taken = bank.addPool(_GACHA_RANGES[pull], user)
            if taken == user:  # Normal accquire
                result += f'\nYou have received a {name}'
            elif taken:  # Stolen
                result += f'\nYou have stolen a {name} from <@{taken}>'
            else:  # None available
                result += f'\nThere were no more {name} available'
        elif pull > 1:  # Pull is less than 50
            removed = bank.removeBest(user)
            if removed < 0:  # Nothing to lose
                response += RESPONSES['NO_LOSS']
            else:
                name = GACHA_NAMES[removed]
                if pull == _GACHA_RANGES[_PULL_MAX]:  # Lost big
                    result += (
                        f'\nYou have disappointed {name}. '
                        'She returns back to the pool'
                    )
                else:  # Lost best
                    result += f'\nYou lost a {name}'
        else:  # Rolled a 1
            bank.nuke()
            result = RESPONSES['NUKE']
            nuked = True
        amount -= 1
    # Send back results
    return result
