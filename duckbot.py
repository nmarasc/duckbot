# Event handler imports
from eventHandlers import MessageHandler

# Duckbot class
class Duckbot:

    # Construct bot with the slack client instance
    def __init__(self, slackclient, bot_id):
    #{{{
        self.sc = slackclient
        self.messageHandler = MessageHandler(bot_id)
    #}}}

    # Handle received messages
    def handleEvent(self, event):
    #{{{
        if "type" not in event:
            return 0

        # Message event, pass to message handler
        if event["type"] == "message":

            response = self.messageHandler.act(event)

            if response:
                user    = event["user"]
                channel = event["channel"]
                self._sendMessage(user, channel, response)
            elif response == None:
                channel = event["channel"]
                self._sendMessage(None,channel,\
                                  "Shutting down for update. Kweh! :duckbot:")
                return 2

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
