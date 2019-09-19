# -*- coding: utf-8 -*-
r"""Main module containing the Duckbot class.

The Duckbot class is contained within this module. Any functions or
variables that are deemed crucial to the user are also kept here.

Classes
-------
Duckbot
    Duck themed chat bot.

Attributes
----------
EXIT_CODES : dict
    Exit reasons and their associated numeric value
"""
from typing import Union
import logging

import asyncio
# from datetime import datetime

import duckbot.util.modloader as modloader
from duckbot.clients import DuckDiscordClient

__all__ = ['Duckbot', 'EXIT_CODES']

logger = logging.getLogger(__name__)

EXIT_CODES = {
    'EXIT_OK': 0,
    'BAD_INIT': 10
}


class Duckbot:
    r"""Duck themed chat bot.

    Chat bot with support for both slack and discord clients
    simultaneously.

    Parameters
    ----------
    config : dict or str
        Configuration options or path to config file

        See `Configuration Dictionary`_ for details.

    Attributes
    ----------
    loop : asyncio.AbstractEventLoop
        Event loop for bot
    temporary : bool
        ``True`` if not saving bot state
    muted : bool
        ``True`` if not replying to messages
    tokens : dict
        Bot tokens for Slack and Discord
    clients : dict
        Chat client instances

    Methods
    -------
    run
        Schedule bot tasks and start the event loop

    Raises
    ------
    ValueError
        Bot was created with no client tokens

    Configuration Dictionary
    ------------------------
    slack_token : str or None
        Slack client token
    discord_token : str or None
        Discord client token
    temporary : bool
        ``True`` if bot state should not be saved
    muted : bool
        ``True`` if bot should not respond to messages
    """
    _TICK_ROLLOVER = 3600
    _PREFIXES = [':DUCKBOT:']

    def __init__(self, config: Union[dict, str]):
        r"""Duckbot initialization."""
        # ##FIXME actually support path config like the docs say
        assert type(config) is dict

        self._ticks = 0
        self.loop = asyncio.get_event_loop()
        self.clients = {'slack': None, 'discord': None}
        self._initCommands()

        self.temporary = config['temporary']
        self.muted = config['muted']
        self.tokens = {
            'slack': config['slack_token'],
            'discord': config['discord_token']
        }

#         self.cooldown = 0
#         self.wish_countdown = 0
#         self.wish_time = datetime(1,1,1,16)
#         self.wish_channel = 'random'

        if not any(self.tokens.values()):
            logger.critical('No tokens were provided!')
            raise ValueError('no tokens provided')

        # ##TODO create slack client
        if self.tokens['slack']:
            self.clients['slack'] = None

        if self.tokens['discord']:
            self.clients['discord'] = DuckDiscordClient(
                self._commands,
                self._PREFIXES,
                self.muted
            )
            logger.info('Discord client created')

    def run(self) -> int:
        r"""Duckbot main loop.

        Create and execute event tasks. One for each client and a tick task
        for timer based events.

        Returns
        -------
        int
            Exit reason code
        """
        self._running = True
        exit_code = EXIT_CODES['EXIT_OK']

        if self.clients['discord']:
            client = self.clients['discord']
            token = self.tokens['discord']
            self.loop.create_task(client.start(token))
            logger.info('Discord client task created')

        self.loop.create_task(self._tick())
        logger.info('Duckbot tick task created')

        try:
            logger.info('Executing main event loop')
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.info('Keyboard interrupt detected')
        finally:
            logger.info('Stopping tasks now')
            self._running = False
            self.loop.run_until_complete(self.clients['discord'].logout())
            tasks = asyncio.all_tasks(self.loop)
            self.loop.run_until_complete(asyncio.gather(*tasks))
            self.loop.stop()
        self.loop.close()
        return exit_code

    def _initCommands(self):
        r"""Initialize bot commands."""
        self._commands = modloader.loadBotCommands()
        self._commands['HELP'].COMMANDS = self._commands

    async def _tick(self):
        r"""Duckbot timed event handler."""
        while self._running:
            self._ticks = (self._ticks + 1) % self._TICK_ROLLOVER
            await asyncio.sleep(10)

    # Set time until next wonderful day message
    # Params: None
    # Return: None
#     def _getWishTime(self):
#         # Get current time
#         current_time = datetime.now().replace(year = 1, month = 1, day = 1)
#         self.wish_timer = (self.WISH_TIME - current_time).seconds
