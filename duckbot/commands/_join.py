# -*- coding: utf-8 -*-
r"""JOIN command module"""
from typing import List
import logging

from duckbot.util.bank import CURRENCY
from duckbot.util.bank import STARTING_BUX

logger = logging.getLogger(__name__)

DISABLED = False

NAMES = [
    'JOIN'
]


_RESPONSES = {
    'ADDED': (
        'You have successfully created an account :duck:\n'
        f'You have {STARTING_BUX} {CURRENCY}'
    ),
    'EXISTS': (
        'You are already a member of this system :duck:\n'
        f'You have {{}} {CURRENCY}'
    )
}

# This is set by the client when the bank is initialized
bank = None


def handle(user: int, channel: int, args: List[str]):
    r"""Register user with the bank system if not already.

    Parameters
    ----------
    user
        User id to register
    channel
        Channel id command was issued from
    args
        Command arguments, unused

    Returns
    -------
    str
        Command response text
    """
    logger.info(f'Processing {NAMES[0]} command')
    if bank.isMember(user):
        logger.info('User not added, already a member')
        response = _RESPONSES['EXISTS'].format(bank.getBalance(user))
    else:
        bank.addUser(user)
        response = _RESPONSES['ADDED']
    return response


def getHelp(args: List[str]):
    r"""Retrieve help message.

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
