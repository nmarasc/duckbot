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

from .util.data import base_ratings
from .util.data import eightball_messages

logger = logging.getLogger(__name__)


class Random(commands.Cog):
    r"""Duckbot Cog for random number generation related commands

    Methods
    -------
    description
        return description of the cog for help command

    roll
        dice rolling command handler
    coin
        coin flipping command handler
    pick
        choice making command handler
    eightball
        magic 8ball command handler

    cog_command_error
        generic handler for unrecognized command errors
    """

    _emoji_regex = r':[a-zA-Z0-9_]{2,32}:'
    _value_regex = '|'.join([_emoji_regex, r'\d+'])
    _roll_regex = f'^({_value_regex})?D({_value_regex})$'
    _roll_regex = re.compile(_roll_regex, flags=re.I)

    _die_max_side = 100
    _die_max_num = 111
    _pick_max = 20

    _die_range_side = range(2, _die_max_side+1)
    _die_range_num = range(1, _die_max_num+1)
    _pick_range = range(2, _pick_max+1)

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

        response = ''
        botmoji = str(ctx.bot.bot_emoji)
        amount = 1

        if roll is None:
            response = f'You probably meant roll 20, kweh! {botmoji}\n'
            roll = '20'

        regex_result = re.search(self._roll_regex, roll)

        if regex_result:  # if there was a match
            if regex_result.group(1):  # if there's a Y value
                amount = self._parseNumOrEmoji(regex_result.group(1))
            sides = self._parseNumOrEmoji(regex_result.group(2))  # X value
        else:  # No match, just a number (or emoji)
            sides = self._parseNumOrEmoji(roll)

        if (type(amount) == str or amount not in self._die_range_num):
            response += f'{amount} is not in the valid range'
        elif (type(sides) == str or sides not in self._die_range_side):
            response += f'{sides} is not in the valid range'
        else:
            result = self._roll(sides, amount)
            if isinstance(result, list):
                head = ', '.join(map(str, result))
                tail = f'\nYour total: {sum(result)}'
            else:
                head = result
                tail = self._emojiRating(result, sides)
            response += f'You rolled: {head} {tail}'

        await ctx.send(f'{ctx.message.author.mention} {response}')

    @commands.command(
        help=('Flip a coin, heads or tails'),
        ignore_extra=True,
        aliases=[':coin:']
    )
    async def coin(self, ctx):
        r"""Flip a coin.

        Parameters
        ----------
        ctx
            Context information for the command
        """
        result = self._roll(2)
        if result == 1:
            message = 'You got: HEADS'
        else:
            message = 'You got: TAILS'
        await ctx.send(f'{ctx.message.author.mention} {message} {ctx.bot.bot_emoji}')

    @commands.command(
        help=('No more choice paralysis\n'
              '`[picks]` - list of things to pick from, can use quotes to preserve spaces'),
        ignore_extra=False,
        aliases=['pickit', 'pikmin', 'choose', 'choice']
    )
    async def pick(self, ctx, *picks):
        r"""Randomly choose from a number of things.

        Parameters
        ----------
        ctx
            Context information for the command
        picks
            list of things to pick from
        """
        if len(picks) in self._pick_range:
            pick = picks[self._roll(len(picks)-1)]
            response = f'I choose: {pick}'
        else:
            botmoji = str(ctx.bot.bot_emoji)
            response = 'Must pick between {} and {} things, kweh! {}'.format(
                min(self._pick_range),
                max(self._pick_range),
                botmoji
            )
        await ctx.send(f'{ctx.message.author.mention} {response} {ctx.bot.bot_emoji}')

    @commands.command(
        help=('Shake the magic 8ball and receive your fortune.'),
        ignore_extra=True,
        aliases=['8ball', ':8ball:']
    )
    async def eightball(self, ctx):
        r"""Give a random magic 8ball response.

        Parameters
        ----------
        ctx
            Context information for the command
        """
        message = eightball_messages[self._roll(len(eightball_messages)-1)]
        await ctx.send(f'{ctx.message.author.mention} {message} {ctx.bot.bot_emoji}')

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
        emoji = base_ratings.get(roll, None)
        if roll == die:
            emoji = ':tada:'
        elif emoji is None:
            if roll <= die/2:
                emoji = ':-1:'
            else:
                emoji = ':ok_hand:'
        return emoji
