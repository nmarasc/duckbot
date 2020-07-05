# -*- coding: utf-8 -*-
r"""Duckbot client classes module.

API client extention classes for Duckbot.

Classes
-------
DuckbotDiscordClient
    Discord client extension
"""
import logging

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import DefaultHelpCommand
from discord.ext.commands import Paginator
import emoji

# from duckbot.cogs.bank import Bank

logger = logging.getLogger(__name__)


class DuckbotDiscordClient(Bot):
    r"""Duckbot implementation of the Discord client.

    Parameters
    ----------
    isMute : bool
        True if bot should not respond to messages

    Inherited from discord.ext.commands.Bot

    Attributes
    ----------
    isMute : bool
        True if bot is not responding to messages

    Inherited from discord.ext.commands.Bot

    Methods
    -------
    on_ready
        Called when successfully logged into client

    on_message_edit
        Called when client receives a message edit event

    Inherited from discord.ext.commands.Bot

    Raises
    ------
    Inherited from discord.ext.commands.Bot
    """
    def __init__(self, isMute):
        r"""Duckbot client initialization."""
        duckpager = Paginator(prefix='>>> :duck: Kweh!', suffix='')
        duckhelp = DefaultHelpCommand(paginator=duckpager)
        super().__init__(
            None,
            case_insensitive=True,
            help_command=duckhelp
        )
        self.isMute = isMute
#         self.add_cog(Bank(self))

    async def on_ready(self):
        r"""Gather information when logged into client."""
        self.command_prefix = commands.when_mentioned
#         self.wish_channel = self.get_channel(self.wish_channel)
#         logger.info(f'Wish channel set as {self.wish_channel}')
        logger.info(f'Duckbot logged into discord as {self.user}')

    async def on_message_edit(self, before, after):
        r"""Discord message edit handler.

        Called when a message receives an edit. This can include anything
        from text edits to pins. The message is only passed to the message
        handler if the content of the text has changed.

        Parameters
        ----------
        before
            Message event before the edit
        after
            Message event after the edit
        """
        if before.content != after.content:
            await self.on_message(after)

    async def on_wish(self):
        r"""Send a wonderful day farewell message."""
        logger.info('Sending wonderful day message')
        if self.wish_channel and not self.muted:
            await self.wish_channel.send(self.wish_msg)

    async def on_regen(self):
        r"""Regen bank bucks."""
        logger.info('Regen event triggered')
