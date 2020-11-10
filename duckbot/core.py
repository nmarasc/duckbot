# -*- coding: utf-8 -*-
r"""Main module containing the Duckbot class.

The Duckbot class is contained within this module. Any functions or
variables that are deemed crucial to the user are also kept here.

Classes
-------
Duckbot
    Duck themed discord bot.
"""
import logging
import asyncio
from datetime import datetime

from duckbot.clients import DuckbotDiscordClient
# from duckbot.cogs.bank import Bank

__all__ = ['Duckbot']

logger = logging.getLogger(__name__)


class Duckbot:
    r"""Duck themed discord bot.

    Discord bot with a command interface for both users and administrators.

    Parameters
    ----------
    token : str
        Discord client bot token
    isTemp : bool, optional
        True if bot state should not be saved

    Attributes
    ----------
    token : str
        Discord client bot token
    isTemp : bool
        True if bot state should not be saved
    loop : asyncio.AbstractEventLoop
        Event loop for bot
    client : duckbot.client.DuckbotDiscordClient
        Duckbot discord client instance

    Methods
    -------
    run
        Schedule bot tasks and start the event loop

    Raises
    ------
    ValueError
        Bot was created with no client token
    """
    _TICK_ROLLOVER = 3600
    _REGEN_TIMER = 300
    _WISH_TIME = datetime(1, 1, 1, 16)

    def __init__(self, token, isTemp=False):
        r"""Duckbot initialization."""

        self._ticks = 0

        if not token:
            logger.critical('No token was provided!')
            raise ValueError('no token provided')

        self.token = token
        self.isTemp = isTemp
        self.loop = asyncio.get_event_loop()
        self.client = DuckbotDiscordClient()

        logger.info('Discord client created')

    def run(self):
        r"""Duckbot main loop.

        Create and execute event tasks. One for the discord client and a
        tick task for timer based events.
        """
        self._running = True

        self.loop.create_task(self.client.start(self.token))
        logger.info('Discord client task created')

        self.loop.create_task(self._tick())
        logger.info('Duckbot tick task created')

#         self.loop.create_task(self._timerWish())
#         logger.info('Good wish task created')

        try:
            logger.info('Executing main event loop')
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.info('Keyboard interrupt detected')
        finally:
            logger.info('Stopping tasks now')
            self._running = False
            self.loop.run_until_complete(self.client.logout())
            tasks = asyncio.all_tasks(self.loop)
            for task in tasks:
                task.cancel()
            self.loop.run_until_complete(asyncio.gather(*tasks))
            self.loop.stop()
        self.loop.close()

    async def _tick(self):
        r"""Duckbot timed event handler."""
        await self.client.wait_until_ready()

        while self._running:
            self._ticks = (self._ticks + 1) % self._TICK_ROLLOVER

            try:
                if self._ticks % self._REGEN_TIMER == 0:
                    await self.client.on_regen()

                await asyncio.sleep(1)
            except asyncio.CancelledError:
                logger.warning('Task cancelled: _tick')

    async def _timerWish(self):
        r"""Set time until next wonderful day message."""
        while self._running:
            time = datetime.now().replace(year=1, month=1, day=1)
            try:
                await asyncio.sleep((self._WISH_TIME - time).seconds)
                await self.client.on_wish()
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                logger.warning('Task cancelled: _timerWish')
