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
from .util.error import GachaRangeError
from .util.error import GachaCostError

logger = logging.getLogger(__name__)


class Game(commands.Cog):
    r"""Container Cog for gaming and banking commands.

    Attributes
    ----------
    bank
        The Duckbank instance

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
    pull
        Pull command handler
    """

    def __init__(self):
        r"""Game initialization."""
        self.bank = Bank()

    @property
    def description(self):
        r"""Return cog description"""
        desc = ('A collection of commands related to the Duckbank and games.\n'
                'Invest, gamble, panic.')
        return desc

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
                    result.append(f'{collection[i]} {self.bank.Gacha.NAMES(i).name}')
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
        target : optional
            User to check the balance of
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
        target : optional
            User to check the collection of
        """
        user = await self._checkTarget(target, ctx)
        if user:
            collection = self.bank.getCollection(user.id)
            result = []
            for i in range(0, len(collection)):
                result.append(f'{collection[i]} {self.bank.Gacha.NAMES(i).name}')
            result = '\n'.join(result)
            if user == ctx.message.author:
                response = f'You currently have:\n{result}'
            else:
                response = f'{user.name} currently has:\n{result}'
            await ctx.send(f'{ctx.message.author.mention} {response}')

    @commands.command(
        help='Spend your hard earned currency on gacha',
        ignore_extra=True
    )
    async def pull(self, ctx, amount=None):
        r"""Spend a user's currency to pull rewards from the gacha pool.

        Parameters
        ----------
        ctx
            Context information for the command
        amount : optional
            Number of pulls to do
        """
        response = ''
        try:
            amount = int(amount)
        except (ValueError, TypeError):
            amount = 1
        user = ctx.message.author.id
        if self.bank.isMember(user):
            if self.bank.hasFreebie(user):
                self.bank.setFreebie(False, user)
                response += '\nYour daily free pull result:'
                response += self._interpretPull(self.bank.freePull(user))
            try:
                response += (
                    '\nYour pull results:'
                    f'{self._interpretPull(self.bank.pull(user, amount))}'
                )
            except GachaRangeError as err:
                response += f'\nYou are only allowed from {err.rmin} to {err.rmax} pulls at once!'
            except GachaCostError as err:
                response += '\nYou can\'t afford to make that many pulls!'
                response += f'\nPulls are {self.bank.PULL_COST} {self.bank.CURRENCY} each.'
                response += f'\nYou currently have: {err.balance} {self.bank.CURRENCY}'
        else:
            response += 'You are not a member of the Duckbank!'
        await ctx.send(f'{ctx.message.author.mention} {ctx.bot.emoji}{response}')

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

    def _interpretPull(self, result):
        r"""Convert results of a pull into a message.

        Parameters
        ----------
        result
            Results of the bank's pull call

        Returns
        -------
        str
            Message friendly interpretation of the pull results
        """
        if not result:
            return (
                '\nYou have set off the nuke! Everyone has returned to the pool.'
                '\nLet the shaming begin!'
            )

        response = ''
        for value in result:
            if value is None:
                response += '\n\tThat was a disappointing pull, but you had nothing to lose!'
            elif value >= 0:
                name = self.bank.Gacha.NAMES(value).name
                response += f'\n\tYou got a {name}'
            else:
                name = self.bank.Gacha.NAMES(-value).name
                max_pull = self.bank.Gacha.RANGES[self.bank.Gacha.MAX]
                if -value == max_pull:
                    response += f'\n\tYou have disappointed {name}. She returns to the pool.'
                else:
                    response += f'\n\tYou lost a {name}'
        return response
