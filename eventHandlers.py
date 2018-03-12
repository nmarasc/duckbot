import util

# Message handler class
class MessageHandler:

    DEFAULT_RESPONSE = "Kweh! :DUCK:"
    COMMANDS = {\
                 'HI' : 0, 'HELLO' : 0,\
               }

    def __init__(self, bot_id):
        self.bot_id = bot_id

    def act(self, event):

        # Standard message type
        if "subtype" not in event:

            print(event["user"] + ": " + event["text"])
            command, parms = self._parseMessage(event["text"])

            # Check command type
            if command is not None:

                # 'HI' command
                if command == 0:
                    return self.DEFAULT_RESPONSE

                # Unknown command
                else:
                    return ""

            # Regular chat message, do nothing
            else:
                return ""

        # Message with subtype
        else:
            return ""

    # Parse message for mention, command, and parms
    def _parseMessage(self, text):

        text_arr = text.upper().split(" ")

        temp = text_arr.pop(0)
        _, id_str = util.matchUserId(temp)
        # Check for mention
        if (id_str == self.bot_id) or\
           (temp   == ":DUCKBOT:"):

            command = self.COMMANDS.get(text_arr.pop(0),-1)
            return command, text_arr

        # No mention, ignore
        else:
            return None, None

