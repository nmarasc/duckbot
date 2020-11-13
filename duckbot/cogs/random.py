# -*- coding: utf-8 -*-
r"""Duckbot Cog for random related commands.

Classes
-------
Random
    Cog for all rng based commands
"""
import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Random(commands.Cog):
    r"""Duckbot Cog for random number generation related commands

    Methods
    -------
    description
        return description of the cog for help command

    roll
        dice rolling command handler

    cog_command_error
        generic handler for unrecognized command errors
    """

    @property
    def description(self):
        r"""Return cog description"""
        desc = ('A collection of commands related to random numbers.\n'
                'Leave your fate to the will of the bots.')
        return desc

    @commands.command(
        help=('Roll some dice, get some numbers \n'
              '`[roll]` - number or pair of numbers in [d]X or YdX form\n'
              '\te.g. 20, d20, or 2d20'),
        ignore_extra=True,
        aliases=[':game_die:']
    )
    async def roll(self, ctx, roll=None):
        r"""Random dice rolling.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            Context information for the command
        """
        logger.info(f'Roll command called with: {roll}')

    async def cog_command_error(self, ctx, error):
        r"""Cog error handler."""
        logger.error(f'{ctx.command} failed with the following error:')
        logger.error(error)
