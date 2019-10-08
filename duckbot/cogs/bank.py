# -*- coding: utf-8 -*-
r"""Duckbot Cog for all banking related activities.

Classes
-------
Bank
    Manager for user accounts and gacha pools
"""
import logging

from discord.ext import commands

from duckbot.util import choiceFunctions as cFunc

logger = logging.getLogger(__name__)


class Bank(commands.Cog):
    r"""The royal bank of Duckbot.

    Manager for Duckbot related banking function and gacha pools.

    Parameters
    ----------
    client : duckbot.clients.DuckDiscordClient
        Active Discord client

    Attributes
    ----------
    client : duckbot.clients.DuckDiscordClient
        Active Discord client
    temporary : bool
        ``True`` if state is not being saved
    users : dict
        Users and their Duckbot bank account details
    pool : List[int]
        Gacha pool for users to pull from
    CURRENCY : str
        Name of Duckbot currency
    STARTING_BALANCE : int
        User starting balance
    GACHA_NAMES : List[str]
        Names of gacha pulls

    Methods
    -------
    addUser
        Add user to the bank
    isUser
        Check if user is in the bank
    getPool
        Get gacha pool of a user
    hasPull
        Check if a user has a certain pull value
    addPool
        Add a value to a user's pool
    removeBest
        Remove the best value from a user's pool
    nuke
        Wipe the gacha pool of every user
    getBalance
        Get bank balance of a user
    deposit
        Add amount to a user's balance
    withdraw
        Subtract amount from a user's balance
    regen
        Restore some balance for users that are low
    hasFreePull
        Check if user has their daily pull available
    setFreePull
        Set free pull value for users
    """
    CURRENCY = 'dux'
    STARTING_BALANCE = 100
    GACHA_NAMES = [
        'Trash',
        'Common',
        'Uncommon',
        'Rare',
        'Super Rare',
        'Ultra Rare',
        'SS Ultra Secret Rare',
        '1000-chan'
    ]

    _DEFAULT_PULL_POOL = [-1, -1, 500, 100, 50, 10, 3, 1]
    _DEFAULT_USER_POOL = [0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, client):
        r"""Bank initialization."""
        self.client = client
        self.temporary = self.client.temporary
        self.users = {}
        # TODO: Use temporary for reading state
        self.pool = list(self._DEFAULT_PULL_POOL)

    def addUser(self, user):
        r"""Add user to the bank.

        Parameters
        ----------
        user : int
            User id to add
        """
        self.users[user] = {
            'balance': self.STARTING_BALANCE,
            'pool': list(self._DEFAULT_USER_POOL),
            'free': True
        }
        logger.debug(f'Added user: {user}')

    def isMember(self, user):
        r"""Check if user is in the bank.

        Parameters
        ----------
        user
            User id to check
        """
        return user in self.users

    def getPool(self, user):
        r"""Get user pool.

        Parameters
        ----------
        user : int
            User id to get pool of

        Returns
        -------
        List[int]
            Pool of user id
        """
        return self.users[user]['pool']

    def hasPull(self, user, pull):
        r"""Check if a user has a certain pull.

        Parameters
        ----------
        user : int
            User id to check for pull value
        pull : int
            Pull index to check for

        Returns
        -------
        bool
            ``True`` if user has specified pull
        """
        return self.users[user]['pool'][pull] > 0

    def addPool(self, user, pull):
        r"""Add value to a user's pool.

        Parameters
        ----------
        pull : int
            Pull index to increase
        user : int
            User id to increase pull of

        Returns
        -------
        int
            Id of user pull was stolen from
        """
        chosen = None
        self.players[user]['pool'][pull] += 1
        if self.pool[pull] > 0:
            self.pool[pull] -= 1
            logger.debug(f'Index {pull} taken from global pool')
        elif self.pool[pull] == 0:
            chosen = self._steal(user, pull)
            self.players[chosen]['pool'][pull] -= 1
            logger.debug(f'Index {pull} taken from user {chosen}')
        return chosen

    def removeBest(self, user):
        r"""Remove a user's best pull from their pool.

        Parameters
        ----------
        user : int
            User id to remove from

        Returns
        -------
        int
            Pull id of removed value or -1
        """
        pool = self.users[user]['pool']
        try:
            pull = max([i for i, v in enumerate(pool) if v > 0])
            pool[pull] -= 1
            if self.pool[pull] >= 0:
                self.pool[pull] += 1
        except ValueError:
            pull = -1
        logger.debug(f'Removed {pull} from user {user}')
        return pull

    def nuke(self):
        r"""Wipe the gacha pool of every user."""
        for user in self.users.values():
            user['pool'] = list(self._DEFAULT_USER_POOL)

    def getBalance(self, user):
        r"""Get user balance.

        Parameters
        ----------
        user : int
            Id to get balance from

        Returns
        -------
        int
            Balance of user
        """
        return self._balance(user)

    def deposit(self, user, amount):
        r"""Add amount to a user's balance.

        Parameters
        ----------
        user : int
            User id to increase balance of
        amount : int
            Amount to increase balance by
        """
        self._balance(user, amount)

    def withdraw(self, user, amount):
        r"""Subtract amount from a user's balance.

        Parameters
        ----------
        user : int
            User id to decrease balance of
        amount : int
            Amount to decrease balance by
        """
        self._balance(user, -amount)

    def regen(self):
        r"""Restore some balance for users low on cash."""
        for user in self.users.values():
            balance = user['balance']
            if balance <= 95:
                user['balance'] += 5
            elif balance < 100:
                user['balance'] = 100

    def hasFreePull(self, user):
        r"""Check for free pull available.

        Parameters
        ----------
        user : int
            User id to check for free pull

        Returns
        -------
        bool
            User's free pull status
        """
        return self.users[user]['free']

    def setFreePull(self, value, user=None):
        r"""Set free pull value of users.

        Parameters
        ----------
        value : bool
            Value to set free pull to
        user : int, optional
            User id to set, all users set if None or omitted
        """
        if user:
            self.users[user]['free'] = value
        else:
            for user in self.users.values():
                user['free'] = value

    def _steal(self, thief, pull):
        r"""Choose user to steal pull from.

        Parameters
        ----------
        pull : int
            Pull index being stolen
        thief : int
            User that is stealing

        Returns
        -------
        int
            User id being stolen from
        """
        users = []
        for user in self.users:
            if self.hasPull(user, pull) and user != thief:
                users.append(user)
        if users:
            choice = cFunc.randomChoice(users)
        else:
            choice = thief
        return choice

    def _balance(self, user, amount=0):
        r"""Adjust a user's balance and return the result.

        Parameters
        ----------
        user : int
            User id to adjust balance of
        amount : int, optional
            Amount to adjust balance, default is 0

        Returns
        -------
        int
            User's balance after adjustment
        """
        self.users[user]['balance'] += amount
        return self.users[user]['balance']

    # Read in bank state file and initialize
    # Params: None
    # Return: None
    # Notes : Please don't write your own bank file.
    # You make mistakes, the bot doesn't
#     def readState(self):
#         reading_users = True
#         try:
#             with open('bank.dat','r') as data:
#                 for line in data:
#                     line = line.strip()
#                     # Skip comments
#                     if line.startswith('#'):
#                         pass
#                     # Signal switch to pool
#                     elif line.startswith(';'):
#                         reading_users = False
#                         # Parse line for user data
#                     elif reading_users and line:
#                         user_data = self._parseuserData(line.split(':'))
#                             if user_data:
#                                 self.users[user_data[0]] = {
#                                     'balance' : user_data[1],
#                                     'pool'    : user_data[2],
#                                     'free'    : user_data[3]
#                                 }
#                     # Parse line for gacha data
#                     elif line:
#                         self.pool = [int(val) for val in line.split(',')]
#         # File doesn't exist, can't be read or gacha pool format error
#         except (OSError, ValueError):
#             self.pool = list(self._DEFAULT_PULL_POOL)

    # Save bank state into file
    # Params: None
    # Return: None
#     def saveState(self):
#         try:
#             with open('bank.dat','w') as data:
#                 # Write out user data
#                 data.write('# users\n')
#                 for key in self.users:
#                     data.write(key + ':' + str(self.users[key]['balance']))
#                     data.write(':' + ','.join(map(str,self.users[key]['pool'])))
#                     data.write(':' + str(self.users[key]['free']))
#                     data.write('\n')
#                 data.write(';\n')
#                 # Write pool data
#                 data.write('# Gacha Pool\n')
#                 data.write(','.join(map(str,self.pool)))
#         # File couldn't be written
#         except OSError:
#             pass

    # Parse user data of line
    # Params: data - line data
    # Return: user data list or None
#     def _parseuserData(self, data):
#         try:
#             if len(data) == 4:
#                 user_data = [util.matchUserId(data[0])]
#                 user_data.append(int(data[1]))
#                 user_data.append([int(val) for val in data[2].split(',')])
#                 user_data.append(data[3] == 'True')
#                 if user_data[0]:
#                     return user_data
#         except ValueError:
#             pass
#         return None
