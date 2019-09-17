# -*- coding: utf-8 -*-
r"""Duckbot chat clients.

Class extensions for chat clients to allow for better control of event
handling.
"""
from typing import List
from types import ModuleType
import re
import logging
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
    listen : bool
        ``True`` if bot should not respond to messages

    Inherited from ``discord.Client``

    Attributes
    ----------
    Inherited from ``discord.Client``

    Methods
    -------
    on_ready
        Called when successfully logged into client

    on_message
        Called when client receives a message event

    Inherited from ``discord.Client``

    Raises
    ------
    Inherited from ``discord.Client``
    """
    def __init__(self, commands: List[ModuleType], prefixes: List[str],
                 listen: bool):
        self.commands = commands
        self.prefixes = prefixes
        self.listen = listen
        super().__init__()

    async def on_ready(self):
        r"""Gather information when logged into client."""
        self.prefixes.append(self.user.mention)
        logger.info(f'Duckbot logged into discord as {self.user}')

    async def on_message(self, message: discord.Message):
        r"""Discord message handler.

        Called when a message is received from Discord. Process the message
        and send the appropriate response, which may be nothing. If
        `self.listen` is ``True``, no message will be sent.

        Parameters
        ----------
        message : discord.Message
            Message event from Discord
        """
        response = None
        message.content = emoji.demojize(message.content)
        logger.info(f'Message from {message.author}: {message.content}')

        if message.author != self.user:
            cmd, args = self._getCommand(message.content)
            logger.info(f'cmd: {cmd}')
            try:
                response = self.commands[cmd].handle(
                    message.author.id,
                    message.channel.id,
                    args
                )
            except KeyError:
                pass
            if cmd in self.commands['HELP'].NAMES and response:
                response = response.format(bot=self.user.mention)
            logger.info(f"Response: {response}")

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
