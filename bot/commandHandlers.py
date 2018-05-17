# Python imports
import re
import shlex
# Project imports
import util
from util import DiagMessage

# Help handler class
class HelpHandler:
#{{{

    # Constructor for Help handler
    # Params: bot_id - user id for the bot
    # Return: HelpHandler instance
    def __init__(self, bot_id):
    #{{{
        self.bot_id = bot_id
        #{{{ - Help messages
        self.help_messages = {
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
            ,util.COMMANDS["CHECKBUX"] :\
                ("Check bank balance of yourself or others\n"
                "Usage: <@" + bot_id + "> CHECKBUX [target]\n"
                "No target defaults to yourself :duck:")
        }
        #}}}
    #}}}

    # Retrieve help message based on passed values
    # Params: parms - list of strings to check for help commands
    # Return: requested help messages or generic one if no specific
    def act(self, parms):
    #{{{
        if parms:
            command = util.COMMANDS.get(parms[0],0)
            command = util.COMMANDS_ALT.get(parms[0],0) if not command else command
            response = self.help_messages.get(command,
                    parms[0] + " is not a recognized command")
            return response
        else:
            return ("Duckbot is a general purpose slackbot for doing various things\n"
                    "To interact with it use <@" + self.bot_id + "> <command>\n"
                    "Supported commands: " + ", ".join(util.COMMANDS) + "\n"
                    "Use <@" + self.bot_id + "> HELP <command> for more details")
    #}}}
#}}}

# Roll handler class
class RollHandler:
#{{{
    ROLL_REGEX="^(:[a-z0-9_-]+:|\d+)?D(:[a-z0-9_-]+:|\d+)$"
    #{{{ - CHARACTER_ROLLS
    CHARACTER_ROLLS = [
         ":DRAGON:"
        ,"CHARACTER"
        ,"CHAR"
    ]
    #}}}

    # Constructor for Roll handler
    # Params: None
    # Return: RollHandler instance with ranges and regex initialized
    def __init__(self):
    #{{{
        # Range from 1-100 allowed
        self.die_range=range(1,101)
        # Can pick from 2-20 things
        self.pick_range=range(2,21)
    #}}}

    # Parse roll command parms and return values
    # Params: roll_parms - list of roll parameters
    # Return:  0, list of rolls
    #          1, list of stats
    #         -1, None for bad param
    #         -2, None for no param
    def roll(self, roll_parms):
    #{{{
        if not roll_parms:
            return -2, None
        # Check for character roll
        elif roll_parms[0] in self.CHARACTER_ROLLS:
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
        if (die_num in self.die_range and die_size in self.die_range):
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
    # Params: roll - roll score to rate
    #         die  - total to compare score to
    # Return: emoji string for rating
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
    # Params: None
    # Return: list of stat lists
    def characterRoll(self):
    #{{{
        rolls = []
        for i in range(0,6):
            rolls.append(util.doRolls(6,4))
        return rolls
    #}}}

    # Roll for coin flip
    # Params: None
    # Return: heads or tails
    def coinRoll(self):
    #{{{
        result = util.doRolls(2)[0]
        if result == 1:
            return "HEADS"
        else:
            return "TAILS"
    #}}}

    # Roll for 8ball response
    # Params: None
    # Return: eight ball message
    def eightballRoll(self):
    #{{{
        roll = util.doRolls(len(util.EIGHTBALL_RESPONSES))[0]
        return util.EIGHTBALL_RESPONSES[roll]
    #}}}

    # Roll for pickit response
    # Params: pick_parms - string to split and pick from
    # Return: 0, chosen thing
    #         1, range to pick from for error
    def pickitRoll(self, pick_parms):
    #{{{
        try:
            # Split on spaces while preserving quoted strings,
            # then remove empty strings because people suck
            pick_parms = shlex.split(" ".join(pick_parms))
            pick_parms = [val for val in pick_parms if val != ""]
        except ValueError:
            return 2, None
        if len(pick_parms) in self.pick_range:
            return 0, pick_parms[util.doRolls(len(pick_parms))[0]-1]
        else:
            return 1, self.pick_range
    #}}}

    # Roll for factoid response
    # Params: None
    # Return: Generated factoid (nothing for right now)
    def factoidRoll(self):
        return "Not yet. Kweh :duck:"

#}}}

# Gambling handler class
class GambleHandler:
#{{{

    BAD_CHANNEL_MSG = ("Sorry, this is not an approved "
        "channel for gambling content\n Please keep it to "
        "channels with the :slot_machine: label :duck:")
    CURRENCY = "duckbux"
    STARTING_BUX = 100

    # Constructor for gamble handler
    # Params: channels - list of channels to check for approved labels
    # Return: GambleHandler instance with approved channels added
    def __init__(self, channels):
    #{{{
        self.logger = util.logger
        self.approved_channels = self.getApproved(channels)
        self.bank = {}
    #}}}

    # Go through channel list and get add approved to list
    # Params: channels - dict of channels to channel data to check
    # Return: list of approved channel ids
    def getApproved(self, channels):
    #{{{
        approved = []
        for key, channel in channels.items():
            if util.LABELS["GAMBLE"] in channel["labels"]:
                approved.append(channel["id"])
        return approved
    #}}}

    # Check for required labels and add channel id if good
    # Params: channel - channel to potentially add
    #         lables  - label list to check
    # Return: None
    def checkChannel(self, channel, labels):
    #{{{
        channel_id   = channel["id"]
        channel_name = channel["name"]
        if (util.LABELS["GAMBLE"] in labels and
            channel_id not in self.approved_channels):
            self.approved_channels.append(channel_id)
            if util.debug:
                self.logger.log(DiagMessage("BOT0060D","Added","#"+channel_name))
        elif (util.LABELS["GAMBLE"] not in labels and
              channel_id in self.approved_channels):
            self.approved_channels.remove(channel_id)
            if util.debug:
                self.logger.log(DiagMessage("BOT0060D","Removed","#"+channel_name))
        else:
            if util.debug:
                self.logger.log(DiagMessage("BOT0060D","No change"))
    #}}}

    # Add user to bank if not in already
    # Params: user    - user id to check for bank entry
    #         channel - channel trying to add from
    # Return: Message to send to channel
    def join(self, user, channel):
    #{{{
        if channel not in self.approved_channels:
            return self.BAD_CHANNEL_MSG
        elif user in self.bank:
            return ("You are already a member of this bank :duck:"
                    "\n" + self.checkbux(user))
        else:
            self.bank[user] = {
                 "bux" : self.STARTING_BUX
            }
            return ("You have been added to the bank :duck:"
                    "\n" + self.checkbux(user))
    #}}}

    # Check a user's bank balance
    # Params: user   - user id requesting balance
    #         target - (maybe) user id str to get balance of
    #                  default None gets user balance
    # Return: Message contains users balance
    def checkbux(self, user, target = None):
    #{{{
        if target:
            valid, target = util.matchUserId(target)
            if valid and target in self.bank:
                return ("<@" + target + "> currently has"
                        " " + str(self.bank[target]["bux"]) + " " + self.CURRENCY)
            elif valid:
                return "<@" + target + "> is not currently registered for this bank :duck:"

        if user in self.bank:
            return ("You currently have"
                    " " + str(self.bank[user]["bux"]) + " " + self.CURRENCY)
        else:
            return "You are not currently registered for this bank :duck:"
    #}}}
#}}}
