import re
import util

# Help handler class
class HelpHandler:
#{{{
    # Initialize with help messages
    def __init__(self, bot_id):
    #{{{
        self.bot_id = bot_id
        self.HELP_MESSAGES = {
                 0  : ("Legacy HI command\n"
                      "Usage: <@" + bot_id + "> HI")
                ,1  : ("Causes the bot to shutdown and signal "
                      "the monitor script to check for updates\n"
                      "Usage: <@" + bot_id + "> UPDATE")
                ,2  : "Don't get smart, you know how to use this"
                ,3  : ("Rolls dice based on parameters given\n"
                      "Usage: <@" + bot_id + "> ROLL ( [d]X | YdX )\n"
                      "Where X is the size of the die and Y is the number of them")
                }
    #}}}

    # Return the appropriate help message based on parameter
    def act(self, parms):
    #{{{
        if parms:
            command = util.COMMANDS.get(parms[0],-1)
            response = self.HELP_MESSAGES.get(command,
                    parms[0] + " is not a recognized command")
            return response
        else:
            coms = util.uniqueCommands(util.COMMANDS)
            return ("Duckbot is a general purpose slackbot for doing various things\n"
                    "To interact with it use <@" + self.bot_id + "> <command>\n"
                    "Supported commands: " + ", ".join(coms) + "\n"
                    "Use <@" + self.bot_id + "> HELP <command> for more details"
                   )
    #}}}
#}}}

# Roll handler class
class RollHandler:
#{{{
    # Initialize RollHandler with range of dice allowed and regex for a roll
    def __init__(self):
    #{{{
        # Range from 1-100 allowed
        self.DIE_RANGE=range(1,101)
        self.ROLL_REGEX="^(:[a-z0-9_-]+:|\d+)?D(:[a-z0-9_-]+:|\d+)$"
    #}}}

    # Parse roll command parms and return values
    def act(self, roll_parms):
    #{{{
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
            return rolls
        #}}}
        else:
            return [None, roll_parms[0]]
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
#}}}

# Coin handler class
class CoinHandler:
#{{{
    # Return the result of the coin command
    def act(self):
        result = util.doRolls(2)[0]
        if result == 1:
            return "HEADS"
        else:
            return "TAILS"
#}}}

# Eightball handler class
class EightballHandler:
#{{{
    # Return the 8ball response
    def act(self):
        roll = util.doRolls(len(util.EIGHTBALL_RESPONSES))[0]
        return util.EIGHTBALL_RESPONSES[roll]
#}}}
