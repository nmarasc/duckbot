import re

# Roll handler class
class RollHandler:

    # Initialize RollHandler with range of dice allowed
    def __init__(self):
        # Range from 1-100 allowed
        self.DIE_RANGE=range(1,101)
        self.ROLL_REGEX="^(:[a-z0-9_-]+:|\d+)?d(:[a-z0-9_-]+:|\d+)$"
        self.EMOJI_ROLLS={\
                ":ONE:"        : 1,\
                ":TWO:"        : 2,\
                ":THREE:"      : 3,\
                ":FOUR:"       : 4,\
                ":FIVE:"       : 5,\
                ":SIX:"        : 6,\
                ":SEVEN:"      : 7,\
                ":EIGHT:"      : 8,\
                ":NINE:"       : 9,\
                ":KEYCAP_TEN:" : 10,\
                ":100:"        : 100,\
                ":HERB:"       : 420,\
                }

    # Parse roll command parms and return values
    def act(self, roll_parms):

        results = re.search(self.ROLL_REGEX, roll_parms)

        # If we matched a dX or YdX case
        if results:
            # YdX case
            if r.group(1):
                # Numeric
                try:
                    die_num = int(r.group(1))
                # Or emoji
                except TypeError:
                    #
