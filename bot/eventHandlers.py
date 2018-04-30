import util
#{{{ - CommandHandler imports
from commandHandlers import HelpHandler
from commandHandlers import RollHandler
from commandHandlers import GambleHandler
#}}}

# Message handler class
class MessageHandler:
#{{{
    DEFAULT_RESPONSE = "Kweh! :DUCK:"

    def __init__(self, bot_id, bot_channels):
    #{{{
        self.bot_id = bot_id
        self.rollHandler = RollHandler()
        self.helpHandler = HelpHandler(bot_id)
        self.gambleHandler = GambleHandler(bot_channels)
    #}}}

    def act(self, event):
    #{{{
        u_parms = ""
        command, o_parms = self._getCommand(event.text)
        # Save old params for nicer messages if needed
        if o_parms:
            u_parms = list(map(str.upper,o_parms))

        # HI command
        if command == util.COMMANDS["HI"]:
            return self.DEFAULT_RESPONSE

        # UPDATE command
        elif command == util.COMMANDS["UPDATE"]:
            return None

        # HELP command
        elif command == util.COMMANDS["HELP"]:
            return self.helpHandler.act(u_parms)

        # ROLL command
        elif command == util.COMMANDS["ROLL"]:
        #{{{
            rc, rolls = self.rollHandler.roll(u_parms)
            if rc == 0:
            #{{{
                add = rolls.pop()
                output = "You rolled: "
                if len(rolls) > 1:
                    output += ", ".join(map(str,rolls)) + "\nYour total: " + str(add)
                else:
                    output += str(rolls[0]) + " " + add
                return output
            # }}}
            elif rc == 1:
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
            else:
                return o_parms[0] + " is not a valid roll."
        #}}}

        # COIN command
        elif command == util.COMMANDS["COIN"]:
            return "You got: " + self.rollHandler.coinRoll()

        # 8BALL command
        elif command == util.COMMANDS["EIGHTBALL"]:
            return self.rollHandler.eightballRoll()

        # FACTOID command
        elif command == util.COMMANDS["FACTOID"]:
            return self.rollHandler.factoidRoll()

        # PICKIT command
        elif command == util.COMMANDS["PICKIT"]:
        #{{{
            rc, response = self.rollHandler.pickitRoll(o_parms)
            if rc == 1:
                return ("Must pick between " + str(min(response)) + " "
                        "and " + str(max(response)) + " things")
            elif rc == 2:
                return "Unmatched quotes! Kweh :duck:"
            else:
                return "I choose: " + response
        #}}}

        # JOIN command
        elif command == util.COMMANDS["JOIN"]:
            return self.gambleHandler.join(event.user, event.channel)

        # CHECKBUX command
        elif command == util.COMMANDS["CHECKBUX"]:
            return self.gambleHandler.checkbux(event.user)

        # No command or unrecognized, either way I don't care
        else:
            return ""
    #}}}

    # Parse message for mention, command, and parms
    def _getCommand(self, text):
    #{{{
        # Message event with no text? Don't even know if it's possible
        # But I'll stop it if it is
        if not text:
            return None, None

        text_arr = text.split(" ")
        temp = text_arr.pop(0).upper()
        _, id_str = util.matchUserId(temp)

        # Check for mention
        if ((id_str == self.bot_id) or
           (temp   == ":DUCKBOT:")) and text_arr:
            c_word = text_arr.pop(0).upper()
            command = util.COMMANDS.get(c_word,0)
            command = util.COMMANDS_ALT.get(c_word,0) if not command else command
            return command, text_arr

        # No mention or no command word, ignore
        else:
            return None, None
    #}}}
#}}}

# Event class
# Standardize event information, hopefully
# Might be a bad idea now that I think about it
# I'll see if this affects performance much
class Event:
#{{{
    def __init__(self, event):
    #{{{
        if "type" in event:
            self.type = event["type"]
        else:
            self.type = None
        self.subtype  = None
        self.user     = None
        self.channel  = None
        self.text     = None
        self.reaction = None
        self.ts       = None
        self.file     = None
        self.ch_data  = None
        if self.type in EVENT_PARSERS:
            EVENT_PARSERS[self.type](self, event)
    #}}}

    def parseMessageEvent(event, old):
    #{{{
        event.channel = old["channel"]
        if "subtype" not in old:
            event.user = old["user"]
            event.text = old["text"]
            event.ts   = old["ts"]
        elif old["subtype"] == "message_changed":
            event.user = old["message"]["user"]
            event.text = old["message"]["text"]
            event.ts   = old["message"]["ts"]
        elif old["subtype"] == "channel_purpose":
            event.user = old["user"]
            event.text = old["purpose"]
            event.ts   = old["ts"]
            event.type = "update"
            event.subtype = "channel_purpose"
    #}}}

    def parseReactionAddedEvent(event, old):
    #{{{
        event.user     = old["user"]
        event.reaction = {
             "emoji" : old["reaction"]
            ,"type"  : old["item"]["type"]
        }
        if event.reaction["type"] == "message":
            event.channel = old["item"]["channel"]
            event.ts      = old["item"]["ts"]

        elif (event.reaction["type"] == "file" or
              event.reaction["type"] == "file_comment"):
            event.file = old["item"]["file"]
    #}}}

    def parseTeamJoinEvent(event, old):
        event.user = old["user"]["id"]

    def parseChannelJoinedEvent(event, old):
    #{{{
        event.type    = "update"
        event.subtype = "channel_joined"
        event.channel = old["channel"]["id"]
        event.ch_data = old["channel"]
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
