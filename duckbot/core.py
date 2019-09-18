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
# Python imports
from typing import Union
import asyncio
import logging
from datetime import datetime

import duckbot.util.moduleLoader as modloader
from duckbot.clients import DuckDiscordClient

__all__ = ['Duckbot', 'EXIT_CODES']

logger = logging.getLogger(__name__)

EXIT_CODES = {
    'EXIT_OK': 0,
    'BAD_INIT': 10
}
#     'INVALID_BOT_ID': 11,
#     'RTM_CONNECT_FAILED': 12,
#     'RTM_BAD_CONNECTION': 13,
#     'RTM_GENERIC_ERROR': 20,
#     'RTM_TIMEOUT_ERROR': 21,
#     'MALFORMED_USER_ID': 30


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

    def __init__(self, config: Union[dict, str]) -> None:
        r"""Duckbot initialization."""
        # ##FIXME actually support path config like the docs say
        assert type(config) is dict

        self._ticks = 0
        self.loop = asyncio.get_event_loop()

        self.temporary = config['temporary']
        self.muted = config['muted']

        self.tokens = {
            'slack': config['slack_token'],
            'discord': config['discord_token']
        }
        self.clients = {'slack': None, 'discord': None}
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

    async def _tick(self):
        r"""Duckbot timed event handler."""
        while self._running:
            self._ticks = (self._ticks + 1) % self._TICK_ROLLOVER
            await asyncio.sleep(10)

    def _initCommands(self):
        r"""Initialize bot commands."""
        self._commands = modloader.loadBotCommands()
        self._commands['HELP'].COMMANDS = self._commands

    # Receives events and passes them to the event manager
    # Params: event - incoming event to process
    # Return: dict with return code and message to issue
    def handleEvent(self, event):
        response = self.event_manager.dispatch(event)
        return response

#       # No event type, get out
#       if event.type == None:
#           return 0
###
#         # Message event, pass to message handler
#         elif event.type == "message":
#         #{{{
#             # Display user and their message
#             if event.text:
#                 self.logger.log(DiagMessage("BOT0010U",event.user,event.text))
#             response = self.msg_handler.act(event)
#
#             # Send message if one was returned
#             if response:
#                 util.sendMessage(event.channel, response, event.user)
#                 return 0
#             # None response signals an update needed
#             elif response == None:
#                 util.sendMessage(event.channel,
#                     "Shutting down for update. Kweh! :duckbot:")
#                 return 2
#             # Otherwise do nothing
#             else:
#                 return 0
#         #}}}
#
#         # Bot message event
#         elif event.type == "bot_message":
#         #{{{
#             self.bot_handler.checkBotId(event.user)
#             # Do something sassy with the bot
#             if not self.cooldown_g:
#                 self.cooldown_g = 120
#                 self.bot_handler.act(event)
#             return 0
#         #}}}
#
#         # Update event, respond based on the event subtype
#         elif event.type == "update":
#         #{{{
#             # channel_purpose and channel_joined require channel list update
#             if (event.subtype == "channel_purpose" or
#                 event.subtype == "channel_joined"):
#                 self._channelListUpdate(event)
#             return 0
#         #}}}
#
#         # Unhandled event type
#         else:
#             # Don't do anything right now
#             return 0
    #}}}

    # Handle tick based bot functions
    # Params: None
    # Return: None
#     def tick(self):
#     #{{{
#         # Tick function is called roughly every second, so the tick count rolls
#         # over about every hour. Roll over point can be changed if time needs to
#         # be tracked longer than an hour at a time.
#         self.ticks = (self.ticks + 1) % self.TICK_ROLLOVER
#         # Flush the buffer every hour or so if there aren't enough messages
#         if self.ticks % util.LOG_TIME == 0:
#             self.logger.log(DiagMessage("LOG0010I"), flush=True)
#         # Save bank data timer
# #         if util.bank_file and self.ticks % util.SAVE_STATE_TIME == 0:
# #             self.gamble_handler.saveState()
#         # Tick down the global cooldown
#         if self.cooldown_g:
#             self.cooldown_g -= 1
#         # Regen some bux for the poor people
# #         if self.ticks % util.REGEN_TIME == 0:
# #             self.gamble_handler.regenBux()
#         # Refresh the free pulls
# #         if self.gamble_handler.pull_timer:
# #             self.gamble_handler.pull_timer -= 1
# #         else:
# #             self.gamble_handler.refreshPulls()
#         # Wonderful day wish
#         if self.wish_timer:
#             self.wish_timer -= 1
#         else:
#             util.sendMessage(self.WISH_CHANNEL, "Go, have a wonderful day.")
#             self._getWishTime()
    #}}}

    # Make updates to channel lists
    # Params: event - Event containing data to update with
    # Return: None
    def _channelListUpdate(self, event):
    #{{{
        # Make change to internal channel list
        self.channels = util.updateChannels(self.channels, event)
        # Update gambler channel list
        event.channel = self.channels[event.channel]
        labels = util.parseLabels(event.channel["purpose"]["value"])
        self.gamble_handler.checkChannel(event.channel, labels)
    #}}}

    # Set time until next wonderful day message
    # Params: None
    # Return: None
    def _getWishTime(self):
    #{{{
        # Get current time
        current_time = datetime.now().replace(year = 1, month = 1, day = 1)
        self.wish_timer = (self.WISH_TIME - current_time).seconds
