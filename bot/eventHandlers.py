import util
#{{{ - CommandHandler imports
from commandHandlers import HelpHandler
from commandHandlers import RollHandler
from commandHandlers import CoinHandler
from commandHandlers import EightballHandler
from commandHandlers import FactoidHandler
from commandHandlers import PickitHandler
#}}}

# Message handler class
class MessageHandler:
#{{{
    DEFAULT_RESPONSE = "Kweh! :DUCK:"

    def __init__(self, bot_id):
    #{{{
        self.bot_id = bot_id
        self.rollHandler = RollHandler()
        self.helpHandler = HelpHandler(bot_id)
        self.coinHandler = CoinHandler()
        self.eightballHandler = EightballHandler()
        self.factoidHandler = FactoidHandler()
        self.pickitHandler = PickitHandler()
    #}}}

    def act(self, event):
    #{{{
        print(event.user + ": " + event.text)
        u_parms = ""
        command, o_parms = self._parseMessage(event.text)
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
            # }}}
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
        elif command == util.COMMANDS["COIN"]:
            return "You got: " + self.coinHandler.act()

        # 8BALL command
        elif command == util.COMMANDS["8BALL"]:
            return self.eightballHandler.act()

        # Factoid command
        elif command == util.COMMANDS["FACTOID"]:
            return self.factoidHandler.act()

        elif command == util.COMMANDS["PICKIT"]:
        #{{{
            rc, response = self.pickitHandler.act(o_parms)
            if rc == 1:
                return ("Must pick between " + str(min(response)) + " "
                        "and " + str(max(response)) + " things")
            elif rc == 2:
                return "Unmatched quotes! Kweh :duck:"
            else:
                return "I choose: " + response
        #}}}

        # No command or unrecognized, either way I don't care
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
           (temp   == ":DUCKBOT:")) and text_arr:
            command = util.COMMANDS.get(text_arr.pop(0).upper(),-1)
            return command, text_arr

        # No mention, ignore
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
        self.user     = None
        self.channel  = None
        self.text     = None
        self.reaction = None
        self.ts       = None
        self.file     = None
        if self.type in EVENT_PARSERS:
            EVENT_PARSERS[self.type](self, event)
    #}}}

    def parseMessageEvent(event, old):
    #{{{
        print("BOT      : Parsing Message event")
        event.channel = old["channel"]
        if "subtype" not in old:
            event.user = old["user"]
            event.text = old["text"]
            event.ts   = old["ts"]
        elif old["subtype"] == "message_changed":
            event.user = old["message"]["user"]
            event.text = old["message"]["text"]
            event.ts   = old["message"]["ts"]
    #}}}

    def parseReactionAddedEvent(event, old):
    #{{{
        print("BOT      : Parsing Reaction event")
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
        print("BOT      : Parsing Join event")
        event.user = old["user"]["id"]
#}}}

#{{{ - EVENT_PARSERS
EVENT_PARSERS = {
     "message"        : Event.parseMessageEvent
    ,"reaction_added" : Event.parseReactionAddedEvent
    ,"team_join"      : Event.parseTeamJoinEvent
}
#}}}
