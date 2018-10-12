# Last Updated: 2.3.0
# Project imports
import util.common as util
from util.diagMessage import DiagMessage
from util.event import Event
from datetime import datetime
# Event handler imports
from handlers.event.message import MessageHandler
from handlers.event.bot import BotHandler

# Command handler imports
from handlers.command.roll import RollHandler
from handlers.command.help import HelpHandler
from handlers.command.gamble import GambleHandler

# Duckbot class delegates event handlers and keeps track of time
class Duckbot:

    TICK_ROLLOVER = 3600 # 60 minutes
    WISH_TIME     = datetime(1,1,1,16) # 16:00
    WISH_CHANNEL  = 'random'

    # Constructor for the bot
    # Params: bot_id       - bot user id, used to detect mentions
    #         bot_channels - dict containing channel ids to channel data
    # Return: Duckbot instance
    def __init__(self, bot_id, bot_channels):
    #{{{
        # Param fields
        self.id = bot_id
        self.channels = bot_channels

        self.debug = util.debug
        self.logger = util.logger
        self.ticks = 0
        self.cooldown_g = 0

        self._getWishTime()

        self.logger.log(DiagMessage("BOT0000I"))
        # Create command handlers
        self.roll_handler = RollHandler()
        util.logger.log(DiagMessage("BOT0001D","Roll")) if util.debug else None
        self.help_handler = HelpHandler(bot_id)
        util.logger.log(DiagMessage("BOT0001D","Help")) if util.debug else None
        self.gamble_handler = GambleHandler(bot_channels)
        util.logger.log(DiagMessage("BOT0001D","Gamble")) if util.debug else None
        # Create event handlers
        self.msg_handler = MessageHandler(
            bot_id,
            gamble_handler=self.gamble_handler,
            help_handler=self.help_handler,
            roll_handler=self.roll_handler
        )
        self.logger.log(DiagMessage("BOT0001D","Message")) if self.debug else None
        self.bot_handler = BotHandler()
        self.logger.log(DiagMessage("BOT0001D","Bot")) if self.debug else None
        self.logger.log(DiagMessage("BOT0002I"))
    #}}}

    # Handles incoming events, calling event specific handlers as needed
    # Params: event_p - incoming event to process
    # Return: 0 - everything processed successfully
    #         1 - an error was found
    #         2 - bot needs to update
    def handleEvent(self, event_p):
    #{{{
#         print(event_p)
        # Create standardized event
        event = Event(event_p)

        # No event type, get out
        if event.type == None:
            return 0

        # Message event, pass to message handler
        elif event.type == "message":
        #{{{
            # Display user and their message
            if event.text:
                self.logger.log(DiagMessage("BOT0010U",event.user,event.text))
            response = self.msg_handler.act(event)

            # Send message if one was returned
            if response:
                util.sendMessage(event.channel, response, event.user)
                return 0
            # None response signals an update needed
            elif response == None:
                util.sendMessage(event.channel,
                    "Shutting down for update. Kweh! :duckbot:")
                return 2
            # Otherwise do nothing
            else:
                return 0
        #}}}

        # Bot message event
        elif event.type == "bot_message":
        #{{{
            self.bot_handler.checkBotId(event.user)
            # Do something sassy with the bot
            if not self.cooldown_g:
                self.cooldown_g = 120
                self.bot_handler.act(event)
            return 0
        #}}}

        # Update event, respond based on the event subtype
        elif event.type == "update":
        #{{{
            # channel_purpose and channel_joined require channel list update
            if (event.subtype == "channel_purpose" or
                event.subtype == "channel_joined"):
                self._channelListUpdate(event)
            return 0
        #}}}

        # Unhandled event type
        else:
            # Don't do anything right now
            return 0
    #}}}

    # Handle tick based bot functions
    # Params: None
    # Return: None
    def tick(self):
    #{{{
        # Tick function is called roughly every second, so the tick count rolls
        # over about every hour. Roll over point can be changed if time needs to
        # be tracked longer than an hour at a time.
        self.ticks = (self.ticks + 1) % self.TICK_ROLLOVER
        # Flush the buffer every hour or so if there aren't enough messages
        if self.ticks % util.LOG_TIME == 0:
            self.logger.log(DiagMessage("LOG0010I"), flush=True)
        # Save bank data timer
        if util.bank_file and self.ticks % util.SAVE_STATE_TIME == 0:
            self.gamble_handler.saveState()
        # Tick down the global cooldown
        if self.cooldown_g:
            self.cooldown_g -= 1
        # Regen some bux for the poor people
        if self.ticks % util.REGEN_TIME == 0:
            self.gamble_handler.regenBux()
        # Refresh the free pulls
        if self.gamble_handler.pull_timer:
            self.gamble_handler.pull_timer -= 1
        else:
            self.gamble_handler.refreshPulls()
        # Wonderful day wish
        if self.wish_timer:
            self.wish_timer -= 1
        else:
            util.sendMessage(self.WISH_CHANNEL, "Go, have a wonderful day.")
            self._getWishTime()
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
    #}}}
