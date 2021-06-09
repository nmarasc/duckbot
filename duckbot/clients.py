# -*- coding: utf-8 -*-
r"""Duckbot client classes module.

API client extention classes for Duckbot.

Classes
-------
DuckbotDiscordClient
    Discord client extension
"""
import logging

import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from mongoengine import connect
from pymongo.errors import ServerSelectionTimeoutError
import emoji

from .help import DuckbotHelpCommand
from .cogs.random import Random
from .cogs.bank import Bank
from .cogs.game import Game
from .cogs.fact import Fact
from .util.database import App, buildGameDB

logger = logging.getLogger(__name__)


class DuckbotDiscordClient(Bot):
    r"""Duckbot implementation of the Discord client.

    Parameters
    ----------
    hostguild
        Guild id of the 'home' server, used for emojis
    steamkey
        Steam WebAPI key

    Methods
    -------
    on_ready
        Called when successfully logged into client
    on_message
        Called when client receives a message
    on_message_edit
        Called when client receives a message edit event
    on_command_error
        Called when an unhandled command error is raised
    on_game_change
        Called when a game change event occurs
    """
    def __init__(self, hostguild, steamkey):
        r"""Duckbot client initialization."""
        super().__init__(
            None,
            case_insensitive=True,
            help_command=None
        )

        if not isinstance(hostguild, int):
            logger.warning('Host id not an int, may not convert properly')
        try:
            self.host_guild = int(hostguild)
        except ValueError:
            self.host_guild = None
        try:
            connect('games')
            if len(App.objects) == 0:
                buildGameDB(steamkey)
            self.db = True
        except ServerSelectionTimeoutError:
            logger.warning('Mongodb not available, cannot build games list')
            self.db = False

        self.add_cog(Random())
        self.add_cog(Bank())
        self.add_cog(Game())
        self.add_cog(Fact())

    async def on_ready(self):
        r"""Gather information when logged into client."""
        self.emoji = None
        prefixes = []

        for guild in self.guilds:
            for gemoji in guild.emojis:
                if gemoji.name == 'duckbot':
                    if guild.id == self.host_guild:
                        self.emoji = gemoji
                    prefixes.append(f'{str(gemoji)} ')

        if self.emoji is None:
            self.emoji = ':duck:'
        self.help_command = DuckbotHelpCommand(str(self.emoji))
        self.command_prefix = commands.when_mentioned_or(*prefixes)
        await self._setGame()
        logger.info(f'Duckbot logged into discord as {self.user}')

    async def on_message(self, message):
        r"""Sanitize emojis from incoming message and pass to super.

        Parameters
        ----------
        message
            Message event received from discord to sanitize
        """
        message.content = emoji.demojize(message.content, use_aliases=True)
        await self.process_commands(message)

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

    async def on_command_error(self, context, exception):
        r"""Default command error handler.

        Override is just to ignore 'no command' errors. The bot can be
        mentioned with no command provided. This prevents the log from
        being populated with useless errors.

        Parameters
        ----------
        context
            Context information for the error
        exception
            Error that was raised
        """
        # Don't bother processing a mention with no command
        if context.command is not None:
            await super().on_command_error(context, exception)

    async def on_wish(self):
        r"""Send a wonderful day farewell message."""
        logger.info('Sending wonderful day message')

    async def on_regen(self):
        r"""Regen bank bucks."""
        logger.info('Regen event triggered')

    async def on_game_change(self):
        r"""Change game status event handler."""
        logger.info('Time to play a new game')
        await self._setGame()

    async def _setGame(self):
        r"""Set a new game status."""
        if self.db:
            playing = discord.Game(random.choice(App.objects).name)
            await self.change_presence(activity=playing)
        else:
            await self.change_presence(activity=discord.Game('duck things'))
