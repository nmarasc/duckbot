# -*- coding: utf-8 -*-
r"""Core Cog and command utility functions and variables."""

__all__ = ['roll']

import random


def roll(sides, amount=1):
    r"""Random number generation within the specified parameters

    Parameters
    ----------
    sides
        number of sides for the die
    amount : optional
        number of dice to roll
    """
    rolls = []
    for i in range(amount):
        rolls.append(random.randint(1, sides))
    if len(rolls) == 1:
        return rolls[0]
    return rolls
