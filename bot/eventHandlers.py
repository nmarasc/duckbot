import util
#{{{ - CommandHandler imports
from commandHandlers import HelpHandler
from commandHandlers import RollHandler
from commandHandlers import CoinHandler
from commandHandlers import EightballHandler
from commandHandlers import FactoidHandler
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
    #}}}

    def act(self, event):
    #{{{
        #FIXME : Finish Event class and use it

        # Standard message type
        if "subtype" not in event:
        #{{{

            print(event["user"] + ": " + event["text"])
            u_parms = ""
            command, o_parms = self._parseMessage(event["text"])
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
            elif command == util.COMMANDS["COIN"]:
                return "You got: " + self.coinHandler.act()

            # 8BALL command
            elif command == util.COMMANDS["8BALL"]:
                return self.eightballHandler.act()

            # Factoid command
            elif command == util.COMMANDS["FACTOID"]:
                return self.factoidHandler.act()

            # No command or unrecognized, either way I don't care
            else:
                return ""
        #}}}

        # Message changed subtype
        elif event["subtype"] == "message_changed":
            return self.act(event["message"])

        # Unhandled subtype
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
#}}}

# Event class
# Standardize event information, hopefully
class Event:
#{{{
    #{{{ - EVENT_PARSERS
    EVENT_PARSERS = {
         "message"        : self.parseMessageEvent
        ,"reaction_added" : self.parseReactionAddedEvent
        ,"team_join"      : self.parseTeamJoinEvent
    }
    #}}}

    def __init__(self, event):
    #{{{
        self.type     = event["type"]
        self.user     = None
        self.channel  = None
        self.text     = None
        self.reaction = None
        self.ts       = None
        self.file     = None
        self.EVENT_PARSERS[self.type](event)
    #}}}

    def parseMessageEvent(self, event):
    #{{{
        self.channel = event["channel"]
        if "subtype" in event and event["subtype"] == "message_changed":
            self.user = event["message"]["user"]
            self.text = event["message"]["text"]
            self.ts   = event["message"]["ts"]
        else:
            self.user = event["user"]
            self.text = event["text"]
            self.ts   = event["ts"]
    #}}}

    def parseReactionAddedEvent(self, event):
    #{{{
        self.user     = event["user"]
        self.reaction = {
             "emoji" : event["reaction"]
            ,"type"  : event["item"]["type"]
        }
        if self.reaction["type"] == "message":
            self.channel = event["item"]["channel"]
            self.ts      = event["item"]["ts"]

        elif (self.reaction["type"] == "file" or
              self.reaction["type"] == "file_comment"):
            self.file = event["item"]["file"]
    #}}}

    def parseTeamJoinEvent(self, event):
        self.user = event["user"]["id"]
#}}}
