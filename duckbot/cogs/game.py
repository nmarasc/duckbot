# -*- coding: utf-8 -*-
r"""Duckbot Cog for games and gambling activities.

Classes
-------
Game
    Container Cog for gaming and banking commands.
"""
import logging

from discord.ext import commands

from .util.error import GachaRangeError
from .util.error import GachaCostError

logger = logging.getLogger(__name__)


class Game(commands.Cog):
    r"""Container Cog for gaming and banking commands.

    Methods
    -------
    pull
        Pull command handler
    """
    @property
    def description(self):
        r"""Return cog description"""
        desc = ('A collection of commands related to games and gambling.\n'
                'Spend, bet, panic.')
        return desc

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
        bank = ctx.bot.get_cog('Bank')
        try:
            amount = int(amount)
        except (ValueError, TypeError):
            amount = 1
        user = ctx.message.author.id
        if bank.isMember(user):
            if bank.hasFreebie(user):
                bank.setFreebie(False, user)
                response += '\nYour daily free pull result:'
                response += self._interpretPull(bank.freePull(user), bank)
            try:
                response += (
                    '\nYour pull results:'
                    f'{self._interpretPull(bank.pull(user, amount), bank)}'
                )
            except GachaRangeError as err:
                response += f'\nYou are only allowed from {err.rmin} to {err.rmax} pulls at once!'
            except GachaCostError as err:
                response += '\nYou can\'t afford to make that many pulls!'
                response += f'\nPulls are {bank.PULL_COST} {bank.CURRENCY} each.'
                response += f'\nYou currently have: {err.balance} {bank.CURRENCY}'
        else:
            response += 'You are not a member of the Duckbank!'
        await ctx.send(f'{ctx.message.author.mention} {ctx.bot.emoji}{response}')

    def _interpretPull(self, result, bank):
        r"""Convert results of a pull into a message.

        Parameters
        ----------
        result
            Results of the bank's pull call
        bank
            Bank instance

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
                name = bank.Gacha.NAMES(value).name
                response += f'\n\tYou got a {name}'
            else:
                name = bank.Gacha.NAMES(-value).name
                max_pull = bank.Gacha.RANGES[bank.Gacha.MAX]
                if -value == max_pull:
                    response += f'\n\tYou have disappointed {name}. She returns to the pool.'
                else:
                    response += f'\n\tYou lost a {name}'
        return response
