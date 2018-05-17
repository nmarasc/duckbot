import re
import util
from util import DiagMessage
#{{{ - CommandHandler imports
from commandHandlers import HelpHandler
from commandHandlers import RollHandler
from commandHandlers import GambleHandler
#}}}

# Message handler class
class MessageHandler:
#{{{
    DEFAULT_RESPONSE = "Kweh! :DUCK:"

    # Constructor for message handler
    # Params: bot_id       - bot user id
    #         bot_channels - dict of channel ids to channel data
    # Return: MessageHandler instance
    def __init__(self, bot_id, bot_channels):
    #{{{
        self.bot_id = bot_id
        self.roll_handler = RollHandler()
        util.logger.log(DiagMessage("BOT0001D","Roll")) if util.debug else None
        self.help_handler = HelpHandler(bot_id)
        util.logger.log(DiagMessage("BOT0001D","Help")) if util.debug else None
        self.gamble_handler = GambleHandler(bot_channels)
        util.logger.log(DiagMessage("BOT0001D","Gamble")) if util.debug else None
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
            u_parms = list(map(str.upper,o_parms))

        # HI command
        if command == util.COMMANDS["HI"]:
            util.logger.log(DiagMessage("BOT0020D","HI")) if util.debug else None
            return self.DEFAULT_RESPONSE

        # UPDATE command
        elif command == util.COMMANDS["UPDATE"]:
            util.logger.log(DiagMessage("BOT0020D","UPDATE")) if util.debug else None
            return None

        # HELP command
        elif command == util.COMMANDS["HELP"]:
            util.logger.log(DiagMessage("BOT0020D","HELP")) if util.debug else None
            return self.help_handler.act(u_parms)

        # ROLL command
        elif command == util.COMMANDS["ROLL"]:
        #{{{
            util.logger.log(DiagMessage("BOT0020D","ROLL")) if util.debug else None
            return_code, rolls = self.roll_handler.roll(u_parms)
            # Regular dice roll
            if return_code == 0:
            #{{{
                # Grab what will be added to the end of the message
                tail = rolls.pop()
                output = "You rolled: "
                # Join all the values if there's more than one
                if len(rolls) > 1:
                    output += ", ".join(map(str,rolls)) + "\nYour total: " + str(tail)
                # Otherwise grab the one and slap the tail on
                else:
                    output += str(rolls[0]) + " " + tail
                return output
            # }}}
            # Character roll
            elif return_code == 1:
            #{{{
                output = ""
                stats = []
                # Go through each set of rolls, drop the lowest and total
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
            elif return_code == -1:
                return o_parms[0] + " is not a valid roll."
            else:
                return "Can't roll without parameters, kweh! :duck:"
        #}}}

        # COIN command
        elif command == util.COMMANDS["COIN"]:
            util.logger.log(DiagMessage("BOT0020D","COIN")) if util.debug else None
            return "You got: " + self.roll_handler.coinRoll()

        # 8BALL command
        elif command == util.COMMANDS["EIGHTBALL"]:
            util.logger.log(DiagMessage("BOT0020D","EIGHTBALL")) if util.debug else None
            return self.roll_handler.eightballRoll()

        # FACTOID command
        elif command == util.COMMANDS["FACTOID"]:
            util.logger.log(DiagMessage("BOT0020D","FACTOID")) if util.debug else None
            return self.roll_handler.factoidRoll()

        # PICKIT command
        elif command == util.COMMANDS["PICKIT"]:
        #{{{
            util.logger.log(DiagMessage("BOT0020D","PICKIT")) if util.debug else None
            return_code, response = self.roll_handler.pickitRoll(o_parms)
            # Number of choices out of range
            if return_code == 1:
                return ("Must pick between " + str(min(response)) + " "
                        "and " + str(max(response)) + " things")
            # Parsing error
            elif return_code == 2:
                return "Unmatched quotes! Kweh :duck:"
            else:
                return "I choose: " + response
        #}}}

        # JOIN command
        elif command == util.COMMANDS["JOIN"]:
            util.logger.log(DiagMessage("BOT0020D","JOIN")) if util.debug else None
            return self.gamble_handler.join(event.user, event.channel)

        # CHECKBUX command
        elif command == util.COMMANDS["CHECKBUX"]:
            util.logger.log(DiagMessage("BOT0020D","CHECKBUX")) if util.debug else None
            target = u_parms[0] if u_parms else None
            return self.gamble_handler.checkbux(event.user, target)

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
        _, id_str = util.matchUserId(trigger)

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
#}}}

# Bot handler class
class BotHandler:
#{{{
    # Constructor for bot handler
    # Params: None
    # Return: BotHandler instance
    def __init__(self):
    #{{{
        self.logger = util.logger
        self.bots   = {}
    #}}}

    # Handle bot interaction
    # Params: event - bot message event
    # Return: list of response parameters
    def act(self, event):
    #{{{
        if event.user in self.bots:
            util.sendMessage(event.channel, "Check this out, kweh :duck:")
            util.sendMessage(event.channel, "Hello", self.bots[event.user])
    #}}}

    # Check if bot id is known and add it if not
    # Params: bot_id - bot id to check
    # Return: None
    def checkBotId(self, bot_id):
    #{{{
        # Add the bot to the list if it's not in there
        if bot_id not in self.bots:
            response = util.sc.api_call("bots.info", token=util.sc.token, bot=bot_id)
            if response["ok"]:
                self.bots[bot_id] = response["bot"]["user_id"]
                self.logger.log(DiagMessage("BOT0051D")) if util.debug else None
            else:
                self.logger.log(DiagMessage("BOT0040E"))
                self.logger.log(DiagMessage("BOT0041E", response["error"]))
        else:
            self.logger.log(DiagMessage("BOT0050D")) if util.debug else None
    #}}}
#}}}

# Event class
# This may affect response time negatively, see how it goes
class Event:
#{{{
    # Constructor for Event
    # Params: event_p - incoming slack event to parse
    # Return: Event instance
    def __init__(self, event_p):
    #{{{
        if "type" in event_p:
            self.type = event_p["type"]
        else:
            self.type = None

        # Call the parser based on the event type
        if self.type in EVENT_PARSERS:
            EVENT_PARSERS[self.type](self, event_p)
    #}}}

    # Parser for message type events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseMessageEvent(event_new, event_old):
    #{{{
#         print(event_old)
        event_new.channel = event_old["channel"]
        if "subtype" not in event_old:
            event_new.user = event_old["user"]
            event_new.text = event_old["text"]
            event_new.ts   = event_old["ts"]
        elif event_old["subtype"] == "message_changed":
            event_new.user = event_old["message"]["user"]
            event_new.text = event_old["message"]["text"]
            event_new.ts   = event_old["message"]["ts"]
        elif event_old["subtype"] == "channel_purpose":
            event_new.user = event_old["user"]
            event_new.text = event_old["purpose"]
            event_new.ts   = event_old["ts"]
            event_new.type = "update"
            event_new.subtype = "channel_purpose"
        elif event_old["subtype"] == "bot_message":
            event_new.type = "bot_message"
            event_new.text = event_old["text"]
            event_new.user = event_old["bot_id"]
            event_new.name = event_old["username"]
            event_new.ts   = event_old["ts"]
        # Ignore subtypes not handled
        else:
            event_new.type = None
    #}}}

    # Parser for reaction added events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseReactionAddedEvent(event_new, event_old):
    #{{{
        event_new.user     = event_old["user"]
        event_new.reaction = {
             "emoji" : event_old["reaction"]
            ,"type"  : event_old["item"]["type"]
        }
        if event_new.reaction["type"] == "message":
            event_new.channel = event_old["item"]["channel"]
            event_new.ts      = event_old["item"]["ts"]

        elif (event_new.reaction["type"] == "file" or
              event_new.reaction["type"] == "file_comment"):
            event_new.file = event_old["item"]["file"]
    #}}}

    # Parser for team join events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseTeamJoinEvent(event_new, event_old):
        event_new.user = event_old["user"]["id"]

    # Parser for channel joined events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseChannelJoinedEvent(event_new, event_old):
    #{{{
        event_new.type    = "update"
        event_new.subtype = "channel_joined"
        event_new.channel = event_old["channel"]["id"]
        event_new.channel_data = event_old["channel"]
    #}}}
#}}}

#{{{ - EVENT_PARSERS
EVENT_PARSERS = {
     "message"        : Event.parseMessageEvent
    ,"reaction_added" : Event.parseReactionAddedEvent
    ,"team_join"      : Event.parseTeamJoinEvent
    ,"channel_joined" : Event.parseChannelJoinedEvent
}
#}}}
