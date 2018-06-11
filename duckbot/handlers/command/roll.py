# Python imports
import re
import shlex
# Project imports
from util import util

# Roll handler class
class RollHandler:
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
                rolls.append(self._emojiRating(rolls[0], die_size))
            else:
                rolls.append(sum(rolls))
            return 0, rolls
        #}}}
        else:
            return -1, None
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

    # Give emoji ratings based on roll score
    # Params: roll - roll score to rate
    #         die  - total to compare score to
    # Return: emoji string for rating
    def _emojiRating(self, roll, die):
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
