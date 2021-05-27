# -*- coding: utf-8 -*-
r"""Duckbot bank account management.

Classes
-------
Bank
    Duckbot upper management for all accounts at the bank of ducks
"""
import logging

from .gacha import Gacha
from .error import GachaRangeError
from .error import GachaCostError

__all__ = ['Bank']

logger = logging.getLogger(__name__)


class Bank():
    r"""Duckbot upper management for all accounts at the bank of ducks.

    Attributes
    ----------
    PULL_RANGE
        Range for valid number of pulls at a time
    PULL_COST
        Cost of a single pull
    CURRENCY
        Name of the Duckbot currency
    STARTING_BALANCE
        Starting value of Duckbank account
    users
        Collection of registered users
    Gacha
        Gacha manager

    Methods
    -------
    isMember
        Check if user has a Duckback account
    getBalance
        Get Duckbank user's account balance
    getCollection
        Get Duckbank user's gacha collection
    hasFreebie
        Get user's free pull status
    addUser
        Add new user account to the Duckbank
    deduct
        Subtract an amount from a user's balance
    deposit
        Add an amount to a user's balance
    addPull
        Add a pull to a user's collection
    removeBest
        Remove the best pull from a user's collection
    nuke
        Wipe every user's collection
    setFreebie
        Set user(s) free pull status
    regen
        Restore some balance for users that are low
    """

    _DEFAULT_COLLECTION = [0, 0, 0, 0, 0, 0, 0, 0]

    PULL_RANGE = range(1, 11)
    PULL_COST = 10

    CURRENCY = 'dux'
    STARTING_BALANCE = 100

    def __init__(self):
        r"""Bank initialization."""
        self.users = {}
        self.Gacha = Gacha()

    def isMember(self, user):
        r"""Check if user is in the bank.

        Parameters
        ----------
        user
            User id to check
        """
        return user in self.users

    def getBalance(self, user):
        r"""Get user balance.

        Parameters
        ----------
        user
            Id of user to fetch balance of

        Returns
        -------
        int
            Balance of user
        """
        return self._balance(user)

    def getCollection(self, user):
        r"""Get user collection.

        Parameters
        ----------
        user
            User id to get collection of

        Returns
        -------
        List
            User's gacha collection
        """
        return self.users[user]['collection']

    def hasFreebie(self, user):
        r"""Check for free pull available.

        Parameters
        ----------
        user
            User id to check for free pull

        Returns
        -------
        bool
            User's free pull status
        """
        return self.users[user]['free']

    def addUser(self, user):
        r"""Add user to the bank.

        Parameters
        ----------
        user
            User id to add
        """
        self.users[user] = {
            'balance': self.STARTING_BALANCE,
            'collection': list(self._DEFAULT_COLLECTION),
            'free': True
        }

    def deduct(self, user, amount):
        r"""Subtract amount from a user's balance.

        Parameters
        ----------
        user
            User id to decrease balance of
        amount
            Amount to decrease balance by
        """
        self._balance(user, -amount)

    def deposit(self, user, amount):
        r"""Add amount to a user's balance.

        Parameters
        ----------
        user
            User id to increase balance of
        amount
            Amount to increase balance by
        """
        self._balance(user, amount)

    def addPull(self, user, pull):
        r"""Add value to a user's collection.

        Parameters
        ----------
        user
            User whose collection to add to
        pull
            Pull index to add

        Returns
        -------
        int
            Pull index added
        """
        self.users[user]['collection'][pull] += 1
        return pull

    def removeBest(self, user):
        r"""Remove the best pull from a user's collection.

        Parameters
        ----------
        user
            User to remove from

        Returns
        -------
        int
            Negative pull index removed or None
        """
        coll = self.users[user]['collection']
        try:
            pull = max([idx for idx, val in enumerate(coll) if val > 0])
            coll[pull] -= 1
            pull *= -1
        except ValueError:
            pull = None
        return pull

    def nuke(self):
        r"""Wipe the gacha pool of every user."""
        for user in self.users.values():
            user['collection'] = list(self._DEFAULT_COLLECTION)

    def setFreebie(self, value, user=None):
        r"""Set free pull value of user(s).

        Parameters
        ----------
        value
            Value to set free pull to
        user : optional
            User id to set, all users set if None or omitted
        """
        if user:
            self.users[user]['free'] = value
        else:
            for user in self.users.values():
                user['free'] = value

    def pull(self, user, amount):
        r"""Pull from the pool and add to the user's collection.

        Parameters
        ----------
        user
            User id doing the pull
        amount
            Number of pulls to attempt

        Returns
        -------
        List
            Results of the pull

        Raises
        ------
        GachaRangeError
            Raised if number of pulls is outside the valid range
        GachaCostError
            Raised if the cost of the pulls exceeds the user's balance
        """
        if amount not in self.PULL_RANGE:
            raise GachaRangeError(self.PULL_RANGE, amount)

        balance = self.getBalance(user)
        cost = self.PULL_COST * amount
        if balance < cost:
            raise GachaCostError(balance, cost)

        self.deduct(user, cost)
        return self._pull(user, amount)

    def freePull(self, user):
        r"""Pull one from the pool without checking cost.

        This also enables the ability to rig the daily if so desired.

        Parameters
        ----------
        user
            User id to do a free pull for

        Returns
        -------
        List
            Results of the pull helper
        """
        return self._pull(user, 1)

    def regen(self):
        r"""Restore some balance for users low on cash."""
        for user in self.users.values():
            balance = user['balance']
            if balance <= 95:
                user['balance'] += 5
            elif balance < 100:
                user['balance'] = 100

    def _pull(self, user, amount):
        r"""Helper function to do pulls from the gacha manager.

        Parameters
        ----------
        user
            User id to do pull(s) for
        amount
            Number of pulls to do

        Returns
        -------
        List
            Results of the pull
        """
        result = []
        nuked = False

        while amount > 0 and not nuked:
            pull = self.Gacha.pull()
            if pull > 50:
                result.append(self.addPull(user, self.Gacha.RANGES[pull]))
            elif pull > 1:
                result.append(self.removeBest(user))
            else:
                self.nuke()
                result = []
                nuked = True
            amount -= 1
        return result

    def _balance(self, user, amount=0):
        r"""Adjust a user's balance and return the result.

        Parameters
        ----------
        user
            User id to adjust balance of
        amount
            Amount to adjust balance, default is 0

        Returns
        -------
        int
            User's balance after adjustment
        """
        self.users[user]['balance'] += amount
        return self.users[user]['balance']
