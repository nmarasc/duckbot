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



# This is set by the client when the bank is initialized
bank = None


def handle(user: int, channel: int, args: List[str]):
    pass


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
