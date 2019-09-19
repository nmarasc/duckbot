# -*- coding: utf-8 -*-
r"""Duckbot chat clients.

Class extensions for chat clients to allow for better control of event
handling.
"""
from types import ModuleType
from typing import List
import logging

import re

import discord
import emoji

logger = logging.getLogger(__name__)


class DuckDiscordClient(discord.Client):
    r"""Duckbot implementation of the Discord client.

    Parameters
    ----------
    commands : List[ModuleType]
        Command modules
    prefixes : List[str]
        Bot prefixes not specific to the client
    muted : bool
        ``True`` if bot should not respond to messages

    Inherited from ``discord.Client``

    Attributes
    ----------
    commands : List[ModuleType]
        Bot command modules
    prefixes : List[str]
        Accepted bot prefixes
    muted : bool
        ``True`` if bot is not responding to messages

    Inherited from ``discord.Client``

    Methods
    -------
    on_ready
        Called when successfully logged into client

    on_message
        Called when client receives a message event

    on_message_edit
        Called when client receives a message edit event

    Inherited from ``discord.Client``

    Raises
    ------
    Inherited from ``discord.Client``
    """
    def __init__(self, commands: List[ModuleType], prefixes: List[str],
                 muted: bool):
        self.commands = commands
        self.prefixes = prefixes
        self.muted = muted
        super().__init__()

    async def on_ready(self):
        r"""Gather information when logged into client."""
        self.prefixes.append(self.user.mention)
        logger.info(f'Duckbot logged into discord as {self.user}')

    async def on_message(self, message: discord.Message):
        r"""Discord message handler.

        Called when a message is received from Discord. Process the message
        and send the appropriate response, which may be nothing. If
        `self.muted` is ``True``, no message will be sent.

        Parameters
        ----------
        message : discord.Message
            Message event from Discord
        """
        response = None
        if message.author == self.user:
            return

        message.content = emoji.demojize(message.content, use_aliases=True)
        logger.debug(f'Message from {message.author}: {message.content}')
        cmd, args = self._getCommand(message.content)
        try:
            response = self.commands[cmd].handle(
                message.author.id,
                message.channel.id,
                args
            )
            if cmd in self.commands['HELP'].NAMES:
                response = response.format(bot=self.user.mention)
        except KeyError:
            pass
        if response:
            response = f'{message.author.mention} {response}'
            logger.info(response)
            if not self.muted:
                await message.channel.send(response)

    async def on_message_edit(self, before, after):
        r"""Discord message edit handler.

        Called when a message receives an edit. This can include anything
        from text edits to pins. The message is only passed to the message
        handler if the content of the text has changed.

        Parameters
        ----------
        before : discord.Message
            Message event before the edit
        after : discord.Message
            Message event after the edit
        """
        if before.content != after.content:
            await self.on_message(after)

    def _getCommand(self, text):
        r"""Split command prefix from args.

        Check for valid command prefix and split message text.

        Parameters
        ----------
        text
            Message text from discord

        Returns
        -------
        str
            Command word
        List[str]
            Command arguments
        """
        cmd = None
        args = re.split(r'\s+', text.strip())
        prefix = args.pop(0).upper()
        if prefix in self.prefixes and args:
            cmd = args.pop(0).upper()
        return cmd, args
