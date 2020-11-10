# -*- coding: utf-8 -*-
r"""Duckbot Cog for rng rolling related commands.

Classes
-------
RNG
    Cog for all rolling based commands
"""
import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Roll(commands.Cog):
    r"""chicken chicken chicken"""

    @commands.command(
        description='Roll some dice, get some numbers',
        help='something here',
#         require_var_positional=True,
        ignore_extra=True
    )
    async def roll(self, ctx, roll=None):
        r"""Random dice rolling.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            Context information for the command
        """
        logger.info(f"Roll command called with: {roll}")

    async def cog_command_error(self, ctx, error):
        r"""Cog error handler."""
        logger.info(f"This error happened: {error}")
        logger.info(f"Failed command: {ctx.command}")
