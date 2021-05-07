# -*- coding: utf-8 -*-
r"""Duckbot Cog for games and gambling activities.

Classes
-------
Game
    Container Cog for gaming and banking commands.
"""
import logging

from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands.errors import MemberNotFound

from .util.bank import Bank

from duckbot.util import choiceFunctions as cFunc

logger = logging.getLogger(__name__)


class Game(commands.Cog):
    r"""Container Cog for gaming and banking commands.

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

    @property
    def description(self):
        r"""Return cog description"""
        desc = ('A collection of commands related to the Duckbank and games.\n'
                'Invest, gamble, panic.')
        return desc

    @commands.command(
        help='Spend your hard earned currency on gacha',
        ignore_extra=True
    )
    async def pull(self, ctx, amount=1):
        r"""Spend a user's currency to pull rewards from the gacha pool.

        Parameters
        ----------
        ctx
            Context information for the command
        amount
            Number of pulls to do
        """
        pass

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
            if self.bank.isMember(user.id):
                balance = self.bank.getBalance(user.id)
                collection = self.bank.getCollection(user.id)
                for i in range(0, len(collection)):
                    result.append(f'{collection[i]} {self.bank.Gacha(i).name}')
                result = '\n'.join(result)
                response = f'You have {balance} {self.bank.CURRENCY} and:\n{result}'
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
        target
            User to check the balance of : optional
        """
        user = await self._checkTarget(target, ctx)
        if user:
            balance = self.bank.getBalance(user.id)
            if user == ctx.message.author:
                response = f'You have {balance} {self.bank.CURRENCY}!'
            else:
                response = f'{user.name} has {balance} {self.bank.CURRENCY}!'
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
        target
            User to check the collection of : optional
        """
        user = await self._checkTarget(target, ctx)
        if user:
            collection = self.bank.getCollection(user.id)
            result = []
            for i in range(0, len(collection)):
                result.append(f'{collection[i]} {self.bank.Gacha(i).name}')
            result = '\n'.join(result)
            if user == ctx.message.author:
                response = f'You currently have:\n{result}'
            else:
                response = f'{user.name} currently has:\n{result}'
            await ctx.send(f'{ctx.message.author.mention} {response}')

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
        if not self.bank.isMember(user.id):
            if user == ctx.message.author:
                response = 'You are not a member of the Duckbank!'
            else:
                response = f'{user.name} is not a member of the Duckbank!'
            await ctx.send(f'{ctx.message.author.mention} {response}')
            user = None
        return user
