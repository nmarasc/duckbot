# -*- coding: utf-8 -*-
r"""Duckbot bank account management.

Classes
-------
Bank
    Duckbot upper management for all accounts at the bank of ducks
"""
import logging

from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands.errors import MemberNotFound

from .util.gacha import Gacha
from .util.error import GachaRangeError
from .util.error import GachaCostError

__all__ = ['Bank']

logger = logging.getLogger(__name__)


class Bank(commands.Cog):
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
    join
        Join command handler
    check
        Check command handler
    balance
        Check balance subcommand handler
    collection
        Check collection subcommand handler

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

    @property
    def description(self):
        r"""Return cog description"""
        desc = ('A collection of commands related to Duckbank management.\n'
                'Your funds are safe with the duck.')
        return desc

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

    @commands.command(
        help='Create a Duckbank account.',
        ignore_extra=True
    )
    async def join(self, ctx):
        r"""Register user with the bank system if not already.

        Parameters
        ----------
        ctx
            Context information for the command
        """
        user = ctx.author.id
        if self.isMember(user):
            balance = self.getBalance(user)
            response = (
                'You already have a Duckbank account!\n'
                f'You have {balance} {self.CURRENCY}'
            )
            logger.info(f'{ctx.author} not added, already a member')
        else:
            self.addUser(user)
            response = (
                'You have successfully created a Duckbank account!\n'
                f'You have {self.STARTING_BALANCE} {self.CURRENCY}'
            )
            logger.info(f'{ctx.author} added')
        await ctx.send(f'{ctx.message.author.mention} {response}')

    @commands.group(
        help=('Retrieve information about the Duckbank.\n'
              '\tReturns all own info if subcommand omitted.'),
        ignore_extra=True,
        aliases=[':heavy_check_mark:', ':white_check_mark:', ':ballot_box_with_check:']
    )
    async def check(self, ctx):
        r"""Check command main handler.

        Parameters
        ----------
        ctx
            Context information for the command
        """
        if ctx.invoked_subcommand is None:
            result = []
            user = ctx.message.author
            if self.isMember(user.id):
                balance = self.getBalance(user.id)
                collection = self.getCollection(user.id)
                for i in range(0, len(collection)):
                    result.append(f'{collection[i]} {self.Gacha.NAMES(i).name}')
                result = '\n'.join(result)
                response = f'You have {balance} {self.CURRENCY} and:\n{result}'
            else:
                response = 'You are not a member of the Duckbank!'
            await ctx.send(f'{ctx.message.author.mention} {response}')

    @check.command(
        help=('Check a user\'s Duckbank balance.\n'
              '`[user]` - mention of the user you want to check\n'
              '\toptional, default checks own balance'),
        ignore_extra=True,
        aliases=[':moneybag:', ':money_with_wings:', 'bux', 'dux', 'dolans']
    )
    async def balance(self, ctx, target=None):
        r"""Check balance subcommand handler.

        Parameters
        ----------
        ctx
            Context information for the command
        target : optional
            User to check the balance of
        """
        user = await self._checkTarget(target, ctx)
        if user:
            balance = self.getBalance(user.id)
            if user == ctx.message.author:
                response = f'You have {balance} {self.CURRENCY}!'
            else:
                response = f'{user.name} has {balance} {self.CURRENCY}!'
            await ctx.send(f'{ctx.message.author.mention} {response}')

    @check.command(
        help=('Check a user\'s Duckbank gacha collection.\n'
              '`[user]` - mention of the user you want to check\n'
              '\toptional, default checks own collection'),
        ignore_extra=True,
        aliases=['gacha', 'pool']
    )
    async def collection(self, ctx, target=None):
        r"""Check collection subcommand handler.

        Parameters
        ----------
        ctx
            Context information for the command
        target : optional
            User to check the collection of
        """
        user = await self._checkTarget(target, ctx)
        if user:
            collection = self.getCollection(user.id)
            result = []
            for i in range(0, len(collection)):
                result.append(f'{collection[i]} {self.Gacha.NAMES(i).name}')
            result = '\n'.join(result)
            if user == ctx.message.author:
                response = f'You currently have:\n{result}'
            else:
                response = f'{user.name} currently has:\n{result}'
            await ctx.send(f'{ctx.message.author.mention} {response}')

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

    async def _checkTarget(self, target, ctx):
        r"""Check for a valid mentioned user.

        Parameters
        ----------
        target
            User provided target to check
        ctx
            Context for member check

        Returns
        -------
        Member
            matching member of the target or None
        """
        if target is None:
            user = ctx.message.author
        else:
            try:
                user = await MemberConverter().convert(ctx, target)
                if not user.mentioned_in(ctx.message):
                    raise MemberNotFound('user not mentioned')
            except MemberNotFound:
                # To stop any possible @everyone shenanigans
                cleaned = await commands.clean_content().convert(ctx, target)
                await ctx.send(f'{ctx.message.author.mention} User {cleaned} not recognized!')
                return None
        if not self.isMember(user.id):
            if user == ctx.message.author:
                response = 'You are not a member of the Duckbank!'
            else:
                response = f'{user.name} is not a member of the Duckbank!'
            await ctx.send(f'{ctx.message.author.mention} {response}')
            user = None
        return user
