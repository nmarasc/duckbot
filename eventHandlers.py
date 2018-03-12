
# Message handler class
class MessageHandler:

    DEFAULT_RESPONSE = "Kweh! :DUCK:"
    COMMANDS = {\
                 'HI' : 0, 'HELLO' : 0,\
               }

    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.mention = "<@"+bot_id+">"

    def handle(self, event):

        # Some nonstandard message type
        if "subtype" in event:
            return ""

        # Standard message type
        else:
            print(event["user"] + ": " + event["text"])
            command, *parms = self._parseMessage(event["text"])

            # Check command type
            if command is not None:

                # 'HI' command
                if command == 0:
                    return self.DEFAULT_RESPONSE

                # Unknown command
                else:
                    return ""

            else:
                return ""

    # Parse message for mention, command, and parms
    def _parseMessage(self, text):

        text_arr = text.upper().split(" ")

        temp = text_arr.pop(0)
        # Check for mention
        if temp == self.mention or\
           temp == ":DUCKBOT:":

            command = self.COMMANDS.get(text_arr.pop(0),-1)
            return command, text_arr

        # No mention, ignore
        else:
            return None, None

