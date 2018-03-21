import util
from commandHandlers import RollHandler

# Message handler class
class MessageHandler:

    DEFAULT_RESPONSE = "Kweh! :DUCK:"
    COMMANDS = {\
                 'HI'     : 0, 'HELLO'      : 0,\
                 'UPDATE' : 1,\
                 'ROLL'   : 2, ':GAME_DIE:' : 2,\
               }

    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.rollHandler = RollHandler()

    def act(self, event):

        # Standard message type
        if "subtype" not in event:

            print(event["user"] + ": " + event["text"])
            command, o_parms = self._parseMessage(event["text"])
            u_parms = list(map(str.upper,o_parms))

            # Check command type
            if command is not None:

                # HI command
                if command == 0:
                    return self.DEFAULT_RESPONSE

                # UPDATE command
                elif command == 1:
                    # TODO: update stuff
                    return self.DEFAULT_RESPONSE

                # ROLL command
                elif command == 2:
                    rolls = self.rollHandler.act(u_parms)
                    if rolls[0]:
                        output = "You rolled: " + ", ".join(map(str,rolls))
                        output += "\nYour total: " + str(sum(rolls))
                        return output
                    else:
                        return o_parms[0] + " is not a valid roll."


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

        text_arr = text.split(" ")

        temp = text_arr.pop(0).upper()
        _, id_str = util.matchUserId(temp)
        # Check for mention
        if (id_str == self.bot_id) or\
           (temp   == ":DUCKBOT:"):
            command = self.COMMANDS.get(text_arr.pop(0).upper(),-1)
            return command, text_arr

        # No mention, ignore
        else:
            return None, None

