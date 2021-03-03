# -*- coding: utf-8 -*-
from .bidict import Bidict

__all__ = ['etoi','itoe']

_EMOJINUMS = Bidict({
    ':one:': 1,
    ':two:': 2,
    ':three:': 3,
    ':four:': 4,
    ':five:': 5,
    ':six:': 6,
    ':seven:': 7,
    ':eight:': 8,
    ':nine:': 9,
    ':keycap_ten:': 10,
    ':eggplant:': 69,
    ':100:': 100,
    ':herb:': 420,
    ':1234:': 1234
})


def etoi(emoji):
    r"""Convert emoji string to a number.

    Parameters
    ----------
    emoji
        String value to convert to a number

    Return
    ------
    int value of emoji or original string if invalid
    """
    return _EMOJINUMS.get(emoji, emoji)

def itoe(number):
    r"""Covert number into emoji string.

    Parameters
    ----------
    number
        int value to covert to an emoji

    Return
    ------
    String representation of the number as an emoji or the original int value
    """
    # This is the same function as above due to the bidirectional dictionary
    # Both names are provided for readability in different contexts
    return _EMOJINUMS.get(number, number)
