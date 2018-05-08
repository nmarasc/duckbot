# Project imports
import util
# Event handler imports
from eventHandlers import MessageHandler
from eventHandlers import Event

# Duckbot class delegates event handlers and keeps track of time
class Duckbot:

    # Constructor for the bot
    # Params: slackclient  - connected slackclient instance
    #         bot_id       - bot user id, used to detect mentions
    #         bot_channels - dict containing channel ids to channel data
    #         logger       - logger instance for logging info
    #         debug        - bool to display debug messages or not
    # Return: Duckbot instance
    def __init__(self, slackclient, bot_id, bot_channels, logger = None, debug = False):
    #{{{
        # Param fields
        self.sc = slackclient
        self.id = bot_id
        self.channels = bot_channels
        self.logger = logger
        self.debug = debug

        self.bots = {}
        self.ticks = 0
        self.cooldown_g = 0

        self.msg_handler = MessageHandler(bot_id, bot_channels)
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
                self.logger.log(event.user + ": " + event.text)
            response = self.msg_handler.act(event)

            # Send message if needed, update if told to, ignore otherwise
            if response:
                self._sendMessage(event.user, event.channel, response)
                return 0
            elif response == None:
                self._sendMessage(None, event.channel,
                                  "Shutting down for update. Kweh! :duckbot:")
                return 2
            else:
                return 0
        #}}}

        # Bot message event, probably build a bot message handler soon
        elif event.type == "bot_message":
        #{{{
            # Add the bot to the list if it's not in there
            if event.user not in self.bots:
                response = self.sc.api_call("bots.info", token=self.sc.token, bot=event.user)
                if response["ok"]:
                    self.bots[event.user] = response["bot"]["user_id"]
                # else error
            # Do something sassy with the bot
            if not self.cooldown_g:
                self.cooldown_g = 120
                self._sendMessage(None, event.channel,
                    "Check this out, kweh :duck:")
                self._sendMessage(self.bots[event.user], event.channel, "Hello")
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
        self.ticks = (self.ticks + 1) % 3600
        # Flush the buffer every hour or so if there aren't enough messages
        if self.ticks % self.logger.LOG_TIME == 0:
            self.logger.log("FLUSH    : Auto flushing buffer", flush=True)
        # Tick down the global cooldown
        if self.cooldown_g:
            self.cooldown_g -= 1
    #}}}

    # Send message to designated channel, and notify user if present
    # Params: channel - channel id to send message to
    #         message - string message to send
    #         user    - user id to notify, not required
    # Return: None
    def _sendMessage(self, channel, message, user = None):
    #{{{
        # Prepend user notification if specified
        if user:
            message = "<@" + user + "> " + message
        self.sc.rtm_send_message(channel, message)
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
        gamble_handler = self.msg_handler.gamble_handler
        result = gamble_handler.checkChannel(event.channel["id"], labels)
        # Print debug message if desired
        if self.debug:
            if result == 1:
                self.logger.log("GC INSERT: " + event.channel["name"])
            elif result == -1:
                self.logger.log("GC REMOVE: " + event.channel["name"])
            elif not result:
                self.logger.log("GC STATIC: No change to gamble channels made")
    #}}}
