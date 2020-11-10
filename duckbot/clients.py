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
import emoji

from duckbot.help import DuckbotHelpCommand
from duckbot.cogs.roll import Roll
# from duckbot.cogs.bank import Bank

logger = logging.getLogger(__name__)


class DuckbotDiscordClient(Bot):
    r"""Duckbot implementation of the Discord client.

    Methods
    -------
    on_ready
        Called when successfully logged into client

    on_message_edit
        Called when client receives a message edit event

    Inherited from discord.ext.commands.Bot
    """
    def __init__(self):
        r"""Duckbot client initialization."""
        super().__init__(
            None,
            case_insensitive=True,
            help_command=DuckbotHelpCommand()
        )
        self.add_cog(Roll())
#         self.add_cog(Bank(self))

    async def on_ready(self):
        r"""Gather information when logged into client."""
        self.command_prefix = commands.when_mentioned
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
