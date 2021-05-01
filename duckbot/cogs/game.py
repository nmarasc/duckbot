# -*- coding: utf-8 -*-
r"""Duckbot Cog for games and gambling activities.

Classes
-------
Game
    Container Cog for gaming and banking commands.
"""
import logging

from discord.ext import commands

from .util.bank import Bank

from duckbot.util import choiceFunctions as cFunc
from .data import gacha_names

logger = logging.getLogger(__name__)


class Game(commands.Cog):
    r"""Container Cog for gaming and banking commands.

    Methods
    -------
    join
        Join command handler
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

    def __init__(self):
        r"""Game initialization."""
        self.bank = Bank()

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

    @commands.command(
        help='Create an account at the bank of Duckbot.',
        ignore_extra=True
    )
    async def join(self, ctx):
        r"""Register user with the bank system if not already.

        Parameters
        ----------
        ctx
            Context information for the command
        """
        logger.debug('Processing JOIN command')
        user = ctx.author.id
        if self.bank.isMember(user):
            balance = self.bank.getBalance(user)
            response = (
                'You already have a Duckbank account!\n'
                f'You have {balance} {self.bank.CURRENCY}'
            )
            logger.info(f'{ctx.author} not added, already a member')
        else:
            self.bank.addUser(user)
            response = (
                'You have successfully created a Duckbank account!\n'
                f'You have {self.bank.STARTING_BALANCE} {self.bank.CURRENCY}'
            )
            logger.info(f'{ctx.author} added')
        await ctx.send(response)
