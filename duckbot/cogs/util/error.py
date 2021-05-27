# -*- coding: utf-8 -*-
r"""Cog and command specific exceptions.

Classes
-------
GachaRangeError
    Exception when attempting to pull outside of the allowed range
GachaCostError
    Exception when attempting to pull more than a user can afford
"""

_all__ = ['GachaRangeError', 'GachaCostError']


class GachaRangeError(Exception):
    r"""Exception when attempting to pull outside of the allowed range.

    Attributes
    ----------
    rmin
        Minimum value allowed in range
    rmax
        Maximum value allowed in range
    attempt
        Value that failed the caused the error
    message
        Explanation of the error
    """

    def __init__(self, prange, attempt):
        self.rmin = min(prange)
        self.rmax = max(prange)
        self.attempt = attempt
        self.message = f'Attempt ({attempt}) is not in [{self.rmin}, {self.rmax}] range'
        super().__init__(self.message)


class GachaCostError(Exception):
    r"""Exception when attempting to pull more than a user can afford.

    Attributes
    ----------
    balance
        Current balance of user requesting pull
    cost
        Cost of the failed pull
    message
        Explanation of the error
    """

    def __init__(self, balance, cost):
        self.balance = balance
        self.cost = cost
        self.message = f'Cost ({cost}) is greater than balance ({balance})'
        super().__init__(self.message)
