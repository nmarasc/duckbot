# -*- coding: utf-8 -*-
from .bidict import Bidict

__all__ = ['etoi']

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
    pass
