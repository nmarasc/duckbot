import util
#{{{ - CommandHandler imports
from commandHandlers import HelpHandler
from commandHandlers import RollHandler
from commandHandlers import CoinHandler
from commandHandlers import EightballHandler
#}}}

# Message handler class
class MessageHandler:

    DEFAULT_RESPONSE = "Kweh! :DUCK:"

    def __init__(self, bot_id):
    #{{{
        self.bot_id = bot_id
        self.rollHandler = RollHandler()
        self.helpHandler = HelpHandler(bot_id)
        self.coinHandler = CoinHandler()
        self.eightballHandler = EightballHandler()
    #}}}

    def act(self, event):
    #{{{
        # Standard message type
        if "subtype" not in event:
        #{{{

            print(event["user"] + ": " + event["text"])
            u_parms = ""
            command, o_parms = self._parseMessage(event["text"])
            if o_parms:
                u_parms = list(map(str.upper,o_parms))

            # HI command
            if command == 0:
                return self.DEFAULT_RESPONSE

            # UPDATE command
            elif command == 1:
                return None

            # HELP command
            elif command == 2:
                return self.helpHandler.act(u_parms)

            # ROLL command
            elif command == 3:
            #{{{
                rc, rolls = self.rollHandler.act(u_parms)
                if rc == 0:
                #{{{
                    add = rolls.pop()
                    output = "You rolled: "
                    if len(rolls) > 1:
                        output += ", ".join(map(str,rolls)) + "\nYour total: " + str(add)
                    else:
                        output += str(rolls[0]) + " " + add
                    return output
                #}}}
                elif rc == 1:
                #{{{
                    output = ""
                    stats = []
                    for group in rolls:
                        output += "\n\nYou rolled: " + ", ".join(map(str,group))
                        output += "\nDropping " + str(min(group)) + ", "
                        group.remove(min(group))
                        stat = sum(group)
                        stats.append(stat)
                        output += "Total: " + str(stat)
                    output += "\n\nYour stats are: " + ", ".join(map(str,stats))
                    return output
                #}}}
                else:
                    return o_parms[0] + " is not a valid roll."
            #}}}

            # COIN command
            elif command == 4:
                return "You got: " + self.coinHandler.act()

            # 8BALL command
            elif command == 5:
                return self.eightballHandler.act()

            # No command or unrecognized, either way I don't care
            else:
                return ""
        #}}}
        # Message with subtype
        else:
            return ""
    #}}}

    # Parse message for mention, command, and parms
    def _parseMessage(self, text):
    #{{{
        text_arr = text.split(" ")
        temp = text_arr.pop(0).upper()
        _, id_str = util.matchUserId(temp)

        # Check for mention
        if ((id_str == self.bot_id) or
           (temp   == ":DUCKBOT:")):
            command = util.COMMANDS.get(text_arr.pop(0).upper(),-1)
            return command, text_arr

        # No mention, ignore
        else:
            return None, None
    #}}}

