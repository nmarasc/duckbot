# Last Updated: 2.2
# Python imports
import re
# Project imports
import util.common as util
from util.diagMessage import DiagMessage

# Message handler class
class MessageHandler:
    DEFAULT_RESPONSE = "Kweh! :DUCK:"

    # Constructor for message handler
    # Params: bot_id       - bot user id
    #         kwargs       - dict containing handlers
    # Return: MessageHandler instance
    def __init__(self, bot_id, **kwargs):
    #{{{
        self.bot_id = bot_id
        for key in kwargs:
            setattr(self, key, kwargs[key])
    #}}}

    # Call handler functions based on extracted command word
    # Params: event - Event instance with necessary data
    # Return: string message to send to slack
    def act(self, event):
    #{{{
        u_parms = ""
        # Split text into command word and params
        command, o_parms = self._getCommand(event.text)
        # Save old params for nicer messages if needed
        if o_parms:
            u_parms = [str.upper(val) for val in o_parms]

        # Log command being processed
        if util.debug and command:
            util.logger.log(DiagMessage(
                "BOT0020D",
                util.COMMANDS.inverse[command][0]
            ))
###
#        # HI command
#        if command == util.COMMANDS["HI"]:
#            return self.DEFAULT_RESPONSE
###
        # UPDATE command
        elif command == util.COMMANDS["UPDATE"]:
            return None

        # HELP command
        elif command == util.COMMANDS["HELP"]:
            return self.help_handler.act(u_parms)
###
#        # ROLL command
#        elif command == util.COMMANDS["ROLL"]:
#        #{{{
#            roll.handle([u_parms,o_parms])
#        #}}}
###
#        # COIN command
#        elif command == util.COMMANDS["COIN"]:
#            return "You got: " + self.roll_handler.coinRoll()
###
#        # 8BALL command
#        elif command == util.COMMANDS["EIGHTBALL"]:
#            return self.roll_handler.eightballRoll()
###
#        # FACTOID command
#        elif command == util.COMMANDS["FACTOID"]:
#            return self.roll_handler.factoidRoll()
###
#        # PICKIT command
#        elif command == util.COMMANDS["PICKIT"]:
#        #{{{
#            return_code, response = self.roll_handler.pickitRoll(o_parms)
#            # Number of choices out of range
#            if return_code == 1:
#                return ("Must pick between " + str(min(response)) + " "
#                        "and " + str(max(response)) + " things")
#            # Parsing error
#            elif return_code == 2:
#                return "Unmatched quotes! Kweh :duck:"
#            else:
#                return "I choose: " + response
#        #}}}
###
        # JOIN command
        elif command == util.COMMANDS["JOIN"]:
            return self.gamble_handler.join(event.user, event.channel)

        # CHECKBUX command
        elif command == util.COMMANDS["CHECKBUX"]:
            target = u_parms[0] if u_parms else None
            return self.gamble_handler.checkbux(event.user, target)

        # BET command
        elif command == util.COMMANDS["BET"]:
            return self.gamble_handler.bet(event.user, event.channel, o_parms)

        # PULL command
        elif command == util.COMMANDS["PULL"]:
            amount = u_parms[0] if u_parms else None
            return self.gamble_handler.pull(event.user, event.channel, amount)

        # CHECKPOOL command
        elif command == util.COMMANDS["CHECKPOOL"]:
            target = u_parms[0] if u_parms else None
            return self.gamble_handler.checkPool(event.user, target)

        # No command or unrecognized, either way I don't care
        else:
            return ""
    #}}}

    # Parse message for mention, command, and parms
    # Params: text - message text to parse
    # Return: command word and params or None,None if no command
    def _getCommand(self, text):
    #{{{
        # Message event with no text? Don't even know if it's possible
        # But I'll stop it if it is
        if not text:
            return None, None

        # Break up the text and try to match the trigger with the bot_id
        text_arr = re.split(r'\s+',text.strip())
        trigger = text_arr.pop(0).upper()
        id_str = util.matchUserId(trigger)

        # Check for mention from id or trigger, then get command
        if ((id_str == self.bot_id) or
           (trigger   == ":DUCKBOT:")) and text_arr:
            c_word = text_arr.pop(0).upper()
            command = util.COMMANDS.get(c_word,0)
            command = util.COMMANDS_ALT.get(c_word,0) if not command else command
            return command, text_arr

        # No mention or no command word, ignore
        else:
            return None, None
    #}}}
