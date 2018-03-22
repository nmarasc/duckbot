import re
import util

# Roll handler class
class RollHandler:
#{{{
    # Initialize RollHandler with range of dice allowed
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
