# Event handler imports
from eventHandlers import MessageHandler
from eventHandlers import Event

# Duckbot class
class Duckbot:

    # Construct bot with the slack client instance
    def __init__(self, slackclient, bot_id, logger = None):
    #{{{
        self.sc = slackclient
        self.messageHandler = MessageHandler(bot_id)
    #}}}

    # Handle received messages
    def handleEvent(self, event_in):
    #{{{
        # Create standardized event
        event = Event(event_in)
        # No event type, run away
        if event.type == None:
            return 0

        # Message event, pass to message handler
        if event.type == "message":
        #{{{
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

        # Unhandled event type
        else:
            # Don't do anything right now
            return 0
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
