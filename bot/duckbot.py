import util
# Event handler imports
from eventHandlers import MessageHandler
from eventHandlers import Event

# Duckbot class
class Duckbot:

    # Construct bot with the slack client instance
    def __init__(self, slackclient, bot_id, bot_channels, bots, logger = None, debug = False):
    #{{{
        self.sc = slackclient
        self.id = bot_id
        self.channels = bot_channels
        self.bots = bots
        self.logger = logger
        self.debug = debug
        self.messageHandler = MessageHandler(bot_id, bot_channels)
        self.ticks = 0
    #}}}

    # Handle received messages
    def handleEvent(self, event_in):
    #{{{
        # Create standardized event
        event = Event(event_in)
        print(event_in)

        # No event type, run away
        if event.type == None:
            return 0
        if event.user in self.bots:
            self._sendMessage(event.user, event.channel,
                              "Why hello fellow bot. Shall we take over the world? Kweh! :duck:")
            return 0

        # Message event, pass to message handler
        if event.type == "message":
        #{{{
            if event.text:
                self.logger.log(event.user + ": " + event.text)
            response = self.messageHandler.act(event)

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

        elif event.type == "bot_message":
            self._sendMessage(event.user, event.channel,
                              "Hello fellow bot. Shall we take over the world? Kweh! :duck:")

        elif event.type == "update":
            if (event.subtype == "channel_purpose" or
                event.subtype == "channel_joined"):
                self._channelListUpdate(event)
            return 0

        # Unhandled event type
        else:
            # Don't do anything right now
            return 0
    #}}}

    def tick(self):
    #{{{
        self.ticks = (self.ticks + 1) % 3600
        if self.ticks % self.logger.LOG_TIME == 0:
            self.logger.log("AUTO     : Flushing buffer", flush=True)
    #}}}

    # Send message to designated channel, and notify user if present
    def _sendMessage(self, user, channel, text):
    #{{{
        if user:
            message = "<@" + user + "> " + text
        else:
            message = text

        self.sc.rtm_send_message(channel, message)
    #}}}

    # Do the necessary updates to internal channel list
    def _channelListUpdate(self, event):
    #{{{
        self.channels = util.updateChannels(self.channels, event)
        event.channel = self.channels[event.channel]
        labels = util.parseLabels(event.channel["purpose"]["value"])
        gambleHandler = self.messageHandler.gambleHandler
        result = gambleHandler.checkChannel(event.channel["id"], labels)
        if self.debug:
            if result == 1:
                self.logger.log("GC INSERT: " + event.channel["name"])
            elif result == -1:
                self.logger.log("GC REMOVE: " + event.channel["name"])
            elif not result:
                self.logger.log("GC STATIC: No change to gamble channels made")

    #}}}
