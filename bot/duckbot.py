import util
# Event handler imports
from eventHandlers import MessageHandler
from eventHandlers import Event

# Duckbot class
class Duckbot:

    # Construct bot with the slack client instance
    def __init__(self, slackclient, bot_id, bot_channels, logger = None):
    #{{{
        self.sc = slackclient
        self.id = bot_id
        self.channels = bot_channels
        self.messageHandler = MessageHandler(bot_id, bot_channels)
        self.logger = logger
        self.ticks = 0
    #}}}

    # Handle received messages
    def handleEvent(self, event_in):
    #{{{
        # Create standardized event
        event = Event(event_in)
#         print(event_in)

        # No event type, run away
        if event.type == None:
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

        elif event.type == "update":
            if event.subtype == "channel_purpose":
                print("Channel purpose update")
                self.channels = util.updateChannels(self.channels, event)
                event.channel = self.channels[event.channel]
                if self.messageHandler.gambleHandler.checkChannel(event.channel):
                    self.logger.log("Adding channel: " + event.channel["name"])
                else:
                    self.logger.log("Not Adding: " + event.channel["name"])
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
