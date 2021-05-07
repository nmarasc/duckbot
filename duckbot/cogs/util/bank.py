# -*- coding: utf-8 -*-
r"""Duckbot bank account management.

Classes
-------
Bank
    Duckbot upper management for all accounts at the bank of ducks
"""
import logging

from .data import Gacha

__all__ = ['Bank']

logger = logging.getLogger(__name__)


class Bank():
    r"""Duckbot upper management for all accounts at the bank of ducks.

    Attributes
    ----------
    CURRENCY
        Name of the Duckbot currency
    STARTING_BALANCE
        Starting value of Duckbank account
    users
        Collection of registered users
    pool
        Current gacha pool
    gacha
        Enum containing gacha names

    Methods
    -------
    isMember
        Check if user has a Duckback account
    getBalance
        Get Duckbank user's account balance
    getCollection
        Get Duckbank user's gacha collection
    addUser
        Add new user account to the Duckbank
    """

    _DEFAULT_PULL_POOL = [-1, -1, 500, 100, 50, 10, 3, 1]
    _DEFAULT_USER_COLLECTION = [0, 0, 0, 0, 0, 0, 0, 0]

    CURRENCY = 'dux'
    STARTING_BALANCE = 100

    def __init__(self):
        r"""Bank initialization."""
        self.users = {}
        self.pool = list(self._DEFAULT_PULL_POOL)
        self.Gacha = Gacha

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

    def addUser(self, user):
        r"""Add user to the bank.

        Parameters
        ----------
        user
            User id to add
        """
        self.users[user] = {
            'balance': self.STARTING_BALANCE,
            'collection': list(self._DEFAULT_USER_COLLECTION),
            'free': True
        }

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
