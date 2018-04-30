import re
import util
import shlex

# Help handler class
class HelpHandler:
#{{{
    # Initialize with help messages
    def __init__(self, bot_id):
    #{{{
        self.bot_id = bot_id
        self.HELP_MESSAGES = {
        #{{{
                 util.COMMANDS["HI"] :\
                    ("Legacy HI command\n"
                    "Usage: <@" + bot_id + "> HI")
                ,util.COMMANDS["UPDATE"] :\
                    ("Causes the bot to shutdown and signal "
                    "the monitor script to check for updates\n"
                    "Usage: <@" + bot_id + "> UPDATE")
                ,util.COMMANDS["HELP"] :\
                    "Don't get smart, you know how to use this"
                ,util.COMMANDS["ROLL"] :\
                    ("Rolls dice based on parameters given\n"
                    "Usage: <@" + bot_id + "> ROLL ( [d]X | YdX )\n"
                    "Where X is the size of the die and Y is the number of them")
                ,util.COMMANDS["COIN"] :\
                    ("Flip a coin\n"
                    "Usage: <@" + bot_id + "> COIN")
                ,util.COMMANDS["EIGHTBALL"] :\
                    ("Shake the magic 8ball\n"
                    "Usage: <@" + bot_id + "> 8BALL")
                ,util.COMMANDS["FACTOID"] :\
                    ("Pull out a random and totally true fact\n"
                    "Usage: <@" + bot_id + "> FACTOID")
                ,util.COMMANDS["PICKIT"] :\
                    ("Pick from a number of things\n"
                    "Usage: <@" + bot_id + "> PICKIT <item1> <item2> ...\n"
                    "Use quotes to have items with spaces in them :duck:")
                ,util.COMMANDS["JOIN"] :\
                    ("Add yourself to the gambler's bank\n"
                    "Usage: <@" + bot_id + "> JOIN\n"
                    "Can only be used in gambling approved channels :duck:")
        #}}}
        }
    #}}}

    # Return the appropriate help message based on parameter
    def act(self, parms):
    #{{{
        if parms:
            command = util.COMMANDS.get(parms[0],0)
            command = util.COMMANDS_ALT.get(parms[0],0) if not command else command
            response = self.HELP_MESSAGES.get(command,
                    parms[0] + " is not a recognized command")
            return response
        else:
            return ("Duckbot is a general purpose slackbot for doing various things\n"
                    "To interact with it use <@" + self.bot_id + "> <command>\n"
                    "Supported commands: " + ", ".join(util.COMMANDS) + "\n"
                    "Use <@" + self.bot_id + "> HELP <command> for more details"
                   )
    #}}}
#}}}

# Roll handler class
class RollHandler:
#{{{
    #{{{ - CHARACTER_ROLLS
    CHARACTER_ROLLS = [
         ":DRAGON:"
        ,"CHARACTER"
        ,"CHAR"
    ]
    #}}}

    # Initialize RollHandler with range of dice allowed and regex for a roll
    def __init__(self):
    #{{{
        # Range from 1-100 allowed
        self.DIE_RANGE=range(1,101)
        self.ROLL_REGEX="^(:[a-z0-9_-]+:|\d+)?D(:[a-z0-9_-]+:|\d+)$"
        # Can pick from 2-20 things
        self.PICK_RANGE=range(2,21)
    #}}}

    # Parse roll command parms and return values
    def roll(self, roll_parms):
    #{{{
        # Check for character roll
        if roll_parms[0] in self.CHARACTER_ROLLS:
            return 1, self.characterRoll()

        results = re.search(self.ROLL_REGEX, roll_parms[0])

        # If we matched a dX or YdX case
        if results:
        #{{{
            # YdX case
            if results.group(1):
                # Numeric
                try:
                    die_num = int(results.group(1))
                # Or emoji
                except ValueError:
                    die_num = util.EMOJI_ROLLS.get(results.group(1),-1)
            else:
                die_num = 1

            # dX half
            # Numeric
            try:
                die_size = int(results.group(2))
            # Or emoji
            except ValueError:
                die_size = util.EMOJI_ROLLS.get(results.group(2),-1)
        #}}}
        # Just X case
        else:
        #{{{
            die_num = 1
            # Numeric
            try:
                die_size = int(roll_parms[0])
            # Or emoji
            except ValueError:
                die_size = util.EMOJI_ROLLS.get(roll_parms[0],-1)
        #}}}

        # Check range for valid rolls
        if (die_num in self.DIE_RANGE and die_size in self.DIE_RANGE):
        #{{{
            rolls = util.doRolls(die_size, die_num)
            if die_num == 1:
                rolls.append(self.emojiRating(rolls[0], die_size))
            else:
                rolls.append(sum(rolls))
            return 0, rolls
        #}}}
        else:
            return -1, None
    #}}}

    # Give emoji ratings based on roll score
    def emojiRating(self, roll, die):
    #{{{
        if roll == 1:
            return ":hyperbleh:"
        elif roll == die:
            return ":partyparrot:"
        elif roll == 69:
            return ":eggplant:"
        elif roll == 420:
            return ":herb:"
        elif roll <= die/2:
            return ":bleh:"
        else:
            return ":ok_hand:"
    #}}}

    # Roll for dnd character stats
    def characterRoll(self):
    #{{{
        rolls = []
        for i in range(0,6):
            rolls.append(util.doRolls(6,4))
        return rolls
    #}}}

    # Roll for coin flip
    def coinRoll(self):
    #{{{
        result = util.doRolls(2)[0]
        if result == 1:
            return "HEADS"
        else:
            return "TAILS"
    #}}}

    # Roll for 8ball response
    def eightballRoll(self):
    #{{{
        roll = util.doRolls(len(util.EIGHTBALL_RESPONSES))[0]
        return util.EIGHTBALL_RESPONSES[roll]
    #}}}

    # Roll for pickit response
    def pickitRoll(self, pick_parms):
    #{{{
        try:
            # Split on spaces while preserving quoted strings,
            # then remove empty strings because people suck
            pick_parms = shlex.split(" ".join(pick_parms))
            pick_parms = [val for val in pick_parms if val != ""]
        except ValueError:
            return 2, None
        if len(pick_parms) in self.PICK_RANGE:
            return 0, pick_parms[util.doRolls(len(pick_parms))[0]-1]
        else:
            return 1, self.PICK_RANGE
    #}}}

    # Roll for factoid response
    def factoidRoll(self):
        return "Not yet. Kweh :duck:"

#}}}

# Gambling handler class
class GambleHandler:
#{{{

    def __init__(self, channels):
    #{{{
        #{{{ - Required labels
        self.requiredLabels = set([
            util.LABELS["GAMBLE"],
            util.LABELS["DUCKBOT"]
        ])
        #}}}
        self.badChannelMsg = ("Sorry, this is not an approved "
            "channel for gambling content\n Please keep it to "
            "channels with the :slot_machine: label :duck:")
        self.currency = "duckbux"
        self.startingBux = 100

        self.approved_channels = self.getApproved(channels)
        self.bank = {}
    #}}}

    def getApproved(self, channels):
    #{{{
        approved = []
        for key, channel in channels.items():
            if key != 'memberOf':
                if self.requiredLabels.issubset(channel["labels"]):
                    approved.append(channel["id"])
        return approved
    #}}}

    def checkChannel(self, ch_id, labels):
    #{{{
        if (self.requiredLabels.issubset(labels) and
            ch_id not in self.approved_channels):
            self.approved_channels.append(ch_id)
            return 1
        elif (not self.requiredLabels.issubset(labels) and
              ch_id in self.approved_channels):
            self.approved_channels.remove(ch_id)
            return -1
        else:
            return 0
    #}}}

    def join(self, user, channel):
    #{{{
        if channel not in self.approved_channels:
            return self.badChannelMsg
        elif user in self.bank:
            return ("You are already a member of this bank :duck:"
                    "\n" + self.checkbux(user))
        else:
            self.bank[user] = {
                 "bux" : self.startingBux
            }
            return ("You have been added to the bank :duck:"
                    "\n" + self.checkbux(user))
    #}}}

    def checkbux(self, user, target = None):
    #{{{
        if not target:
            return ("You currently have " + str(self.bank[user]["bux"]) + ""
                    " " + self.currency)
    #}}}
#}}}
