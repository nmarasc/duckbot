# -*- coding: utf-8 -*-
r"""
"""
import re
import logging
import discord
import emoji

logger = logging.getLogger(__name__)


class DuckDiscordClient(discord.Client):
    r"""Duckbot implementation of the Discord client.

    Parameters
    ----------
    Inherited from ``discord.Client``

    Attributes
    ----------
    Inherited from ``discord.Client``

    Methods
    -------
    on_ready
        Called when successfully logged into client

    Inherited from ``discord.Client``

    Raises
    ------
    Inherited from ``discord.Client``
    """
    def __init__(self, listen, commands):
        self.listen = listen
        self.commands = commands
        super().__init__()

    async def on_ready(self):
        r"""Gather information when logged into client."""
        logger.info(f'Duckbot logged into discord as {self.user}')

    async def on_message(self, message):
        r"""Discord message handler.

        Called when a message is received from Discord. Process the message
        and give the appropriate response, which may be nothing.

        Parameters
        ----------
        message
            Message event from Discord
        """
#         logger.info(f'Message event: {message}')
        message.content = emoji.demojize(message.content)
        logger.info(f'Message from {message.author}: {message.content}')

        response = {'return_code': 0}
        logger.info(f'author: {message.author} user: {self.user}')
        if message.author != self.user:
            # Extract command from event text
            logger.info(message.content)
            cmd, cmd_args = self._getCommand(message.content)
            try: # Attempt to call command handler
                response = self.commands[cmd].handle(
                    message.author.id,
                    message.channel.id,
                    cmd_args
                )
                #TODO: check rc maybe
            except KeyError: # No command or unrecognized, ignore
                response['return_code'] = -1
                response['message'] = None
            logger.info(f"Response: {response['message']}")

    def _getCommand(self, text):
        # Message event with no text? Don't even know if it's possible
        # But I'll stop it if it is
        if not text:
            return None, None

        # Break up the text and try to match the trigger with the bot_id
        text_arr = re.split(r'\s+',text.strip())
        trigger = text_arr.pop(0).upper()
        id_str = re.sub('[<@>]','',trigger)
        logger.info(f'trigger: {trigger} id_str: {id_str}')

        # Check for mention from id or trigger, then get command
        logger.info(f'{id_str == self.user.id}')
        if ((id_str == str(self.user.id)) or
            (trigger   == ":DUCKBOT:")) and text_arr:
            c_word = text_arr.pop(0).upper()
            return c_word, text_arr

        # No mention or no command word, ignore
        else:
            return None, None
