# -*- coding: utf-8 -*-
r"""Duckbot Cog for random related commands.

Classes
-------
Random
    Cog for all rng based commands
"""
import logging

import re
import random

from discord.ext import commands

from duckbot.util import etoi

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

    _emoji_regex = r':[a-zA-Z0-9_]{2,32}:'
    _value_regex = '|'.join([_emoji_regex, r'\d+'])
    _roll_regex = f'^({_value_regex})?D({_value_regex})$'
    _roll_regex = re.compile(_roll_regex, flags=re.I)

    _die_max_side = 100
    _die_max_num = 111

    _die_range_side = range(2, _die_max_side+1)
    _die_range_num = range(1, _die_max_num+1)

    _base_ratings = {
        1: ':clown:',
        13: ':ghost:',
        69: ':eggplant:',
        420: ':herb:'
    }

    @property
    def description(self):
        r"""Return cog description"""
        desc = ('A collection of commands related to random numbers.\n'
                'Leave your fate to the will of the bots.')
        return desc

    @commands.command(
        help=('Roll some dice, get some numbers\n'
              '`[roll]` - number or pair of numbers in [d]X or YdX form\n'
              '\te.g. 20, d20, or 2d20'),
        ignore_extra=True,
        aliases=[':game_die:']
    )
    async def roll(self, ctx, roll=None):
        r"""Random dice rolling.

        Parameters
        ----------
        ctx
            Context information for the command
        roll
            user argument to roll command : optional
        """
        logger.debug(f'Roll command called with: {roll}')
        botmoji = str(ctx.bot.bot_emoji)
        if roll is None:
            response = f"Can't roll without parameters, kweh! {botmoji}"
            await ctx.send(f'{ctx.message.author.mention} {response}')
            return

        amount = 1

        regex_result = re.search(self._roll_regex, roll)

        if regex_result:  # if there was a match
            if regex_result.group(1):  # if there's a Y value
                amount = self._parseNumOrEmoji(regex_result.group(1))
            sides = self._parseNumOrEmoji(regex_result.group(2))  # X value
        else:  # No match, just a number (or emoji)
            sides = self._parseNumOrEmoji(roll)

        if (type(amount) == str or amount not in self._die_range_num):
            response = f'{amount} is not in the valid range'
        elif (type(sides) == str or sides not in self._die_range_side):
            response = f'{sides} is not in the valid range'
        else:
            result = self._roll(sides, amount)
            if isinstance(result, list):
                head = ', '.join(map(str, result))
                tail = f'\nYour total: {sum(result)}'
            else:
                head = result
                tail = self._emojiRating(result, sides)
            response = f'You rolled: {head} {tail}'

        logger.info(f'{ctx.command} response: {response}')
        await ctx.send(f'{ctx.message.author.mention} {response}')

    async def cog_command_error(self, ctx, error):
        r"""Cog error handler."""
        logger.error(f'{ctx.command} failed with the following error:')
        logger.error(error)

    def _roll(self, sides, amount=1):
        r"""Random number generation within the specified parameters

        Parameters
        ----------
        sides
            number of sides for the die
        amount
            number of dice to roll : optional
        """
        rolls = []
        for i in range(amount):
            rolls.append(random.randint(1, sides))
        if len(rolls) == 1:
            return rolls[0]
        return rolls

    def _parseNumOrEmoji(self, value):
        r"""Convert string to a number or valid emoji number.

        Parameters
        ----------
        value
            string value to convert to a number
        """
        try:
            value = int(value)
        except ValueError:
            value = etoi(value)
        return value

    def _emojiRating(self, roll, die):
        r"""Give an emoji rating based on roll score.

        Parameters
        ----------
        roll
            score to rate
        die
            maximum score to compare
        """
        emoji = self._base_ratings.get(roll, None)
        if roll == die:
            emoji = ':tada:'
        elif emoji is None:
            if roll <= die/2:
                emoji = ':-1:'
            else:
                emoji = ':ok_hand:'
        return emoji
