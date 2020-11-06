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

class RNG(commands.Cog):
r"""
"""

    @commands.command(
        description = 'Roll some dice, get some numbers',
        help = '',
        ignore_extra = True
    )
    async def roll(self, ctx):
    r"""Random dice rolling.

    Parameters
    ----------
    ctx : discord.ext.commands.Context
        Context information for the command
    """
        pass
