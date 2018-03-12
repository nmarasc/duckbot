# Event handler imports
from eventHandlers import MessageHandler

# Duckbot class
class Duckbot:

    # Construct bot with the slack client instance
    def __init__(self, slackclient, bot_id):
        self.sc = slackclient
        self.messageHandler = MessageHandler(bot_id)

    # Handle received messages
    def handleEvent(self, event):

        if "type" not in event:
#             print(event)
            return

        # Message event, pass to message handler
        if event["type"] == "message":

            response = self.messageHandler.act(event)

            if response:
                user    = event["user"]
                channel = event["channel"]
                self._sendMessage(user, channel, response)

        # Unhandled event type
        else:
            # Don't do anything right now
            return

    # Send message to designated channel, and notify user if present
    def _sendMessage(self, user, channel, text):

        if user:
            message = "<@" + user + "> " + text
        else:
            message = text

        self.sc.rtm_send_message(channel, message)
