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
from datetime import datetime

import duckbot.util.modloader as modloader
from duckbot.util.bank import Bank
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
    bank : duckbot.util.bank.Bank
        Bot bank instance
    clients : dict
        Chat client instances
    tokens : dict
        Bot tokens for Slack and Discord

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
    _REGEN_TIMER = 300
    _PREFIXES = [':DUCKBOT:']
    _WISH_TIME = datetime(1, 1, 1, 16)

    def __init__(self, config: Union[dict, str]):
        r"""Duckbot initialization."""
        # ##FIXME actually support path config like the docs say
        assert type(config) is dict

        self.loop = asyncio.get_event_loop()
        self.temporary = config['temporary']
        self.bank = Bank(self.temporary)
        self.clients = {'slack': None, 'discord': None}
        self.tokens = {
                'slack': config['slack_token'],
                'discord': config['discord_token']
                }

        self._ticks = 0
        self._countdowns = {}
        self._initCommands()


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
                config['channel'],
                config['muted']
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
        self.loop.create_task(self._wishTimer())

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
            for task in tasks:
                task.cancel()
            self.loop.run_until_complete(asyncio.gather(*tasks))
            self.loop.stop()
        self.loop.close()
        return exit_code

    def _initCommands(self):
        r"""Initialize bot commands."""
        self._commands = modloader.loadBotCommands()
        self._commands['HELP'].COMMANDS = self._commands
        self._commands['JOIN'].bank = self.bank
        self._commands['CHECK'].bank = self.bank
        self._commands['PULL'].bank = self.bank

    async def _wishTimer(self):
        r"""Set time until next wonderful day message."""
        while self._running:
            time = datetime.now().replace(year=1, month=1, day=1)
            try:
                await asyncio.sleep((self._WISH_TIME - time).seconds)
                await self.clients['discord'].on_wish()
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                logger.warning('Task cancelled: _wishTimer')

    async def _tick(self):
        r"""Duckbot timed event handler."""
        await self.clients['discord'].wait_until_ready()

        while self._running:
            self._ticks = (self._ticks + 1) % self._TICK_ROLLOVER

            if self._ticks % self._REGEN_TIMER == 0:
                self.bank.regen()

            await asyncio.sleep(1)
