# Last Updated: 2.2
# Python imports
import re
from copy import copy
# Duckbot util modules
from util.common import roll

# Valid command names
NAMES = [
    'ROLL',
    ':GAME_DIE:'
]

# Command help message
HELP = (
    "Rolls dice based on parameters given\n"
    "Usage: <@{id:s}> " + NAMES[0] + " ( [d]X | YdX )\n"
    "Where X is the number of faces and Y is the number of dice"
)

# Valid character roll names
NAMES_CHARACTER = [
    "CHARACTER",
    "CHAR",
    ":DRAGON:"
]

# Valid emoji number values
EMOJI_ROLLS = {
    ":ONE:"        : 1,
    ":TWO:"        : 2,
    ":THREE:"      : 3,
    ":FOUR:"       : 4,
    ":FIVE:"       : 5,
    ":SIX:"        : 6,
    ":SEVEN:"      : 7,
    ":EIGHT:"      : 8,
    ":NINE:"       : 9,
    ":KEYCAP_TEN:" : 10,
    ":100:"        : 100,
}

# Base emoji roll ratings
BASE_RATINGS = {
    1: ":hyperbleh:",
    13: ":ghost:",
    69: ":eggplant:",
    420: ":herb:"
}

# Regex used to determine a valid roll format of YdX or dX case
ROLL_REGEX = "^(:[a-zA-Z0-9_-]+:|\d+)?D(:[a-zA-Z0-9_-]+:|\d+)$"
# Range for amount of dice and number of sides per die allowed
DIE_RANGE = range(1,101)

# Get response from proper sub roll command
# Params: args - list of roll parameters
# Return:  String containing the response from the command
def handle(args):
    # Check for no parameters
    if not args:
        response = "Can't roll without parameters, kweh! :duck:"
    # Check for character roll
    elif str.upper(args[0]) in NAMES_CHARACTER:
        response = _characterRoll()
    # Otherwise regular roll command
    else:
        response = _defaultRoll(args[0])
    return response

# Retrieve command help message
# Params: ops - help options, **unused**
# Return: String help message
def getHelp(ops):
    return HELP

# Standard roll command
# Params: roll_str - String containing roll command operator
# Return: String containing reponse from standard roll command
def _defaultRoll(roll_str):
    roll_upper = str.upper(roll_str)
    # Test parameter with regex for YdX or dX case
    regex_result = re.search(ROLL_REGEX, roll_upper)

    if regex_result:  # There was a match
        if regex_result.group(1):  # Y value
            die_num = _parseNum(regex_result.group(1))
        else:
            die_num = 1

        # X value
        die_sides = _parseNum(regex_result.group(2))

    else:             # No match, just a number
        die_num = 1
        die_sides = _parseNum(roll_upper)

    # Check that parameters are in the valid range
    if (die_num in DIE_RANGE and die_sides in DIE_RANGE):
        response = "You rolled: "
        result = roll(die_sides, die_num)
        if isinstance(result, list):
            response += (", ".join(map(str, result)) +
                         "\nYour total: " + str(sum(result)))
        else:
            response += str(result) + " " + _emojiRating(result, die_sides)
    # Invalid ranges
    else:
        response = roll_str + " is not a valid roll."
    return response

# Roll for dnd character stats
# Params: None
# Return: String containing response from character roll command
def _characterRoll():
    response = ''
    stats = []
    for i in range(0,6):  # For each stat
        stat_group = roll(6,4)  # Roll 4d6
        min_group = min(stat_group)
        response += "\nYou rolled: " + ", ".join(map(str,stat_group))
        response += "\nDropping " + str(min_group) + ", "
        stat_group.remove(min_group)  # Remove the lowest value
        stat = sum(stat_group)  # Get the stat total
        stats.append(stat)
        response += "Total: " + str(stat)
    response += "\n\nYour stats are: " + ", ".join(map(str, stats))
    return response

# Give emoji ratings based on roll score
# Params: roll - roll score to rate
#         die  - total to compare score to
# Return: emoji string for rating
def _emojiRating(roll, die):
    ratings = copy(BASE_RATINGS)
    ratings[die] = ":partyparrot:"
    emoji = ratings.get(roll, None)
    if emoji is None:
        if roll <= die/2:
            emoji = ":bleh:"
        else:
            emoji = ":ok_hand:"
    return emoji

# Convert a string containing a number or an emoji to an int
# Params: str_val - String to parse
# Return: int representing the string value, or -1 if invalid
def _parseNum(str_val):
    # Check for a numeric value
    try:
        int_val = int(str_val)
    # Or an emoji value
    # int_val is set to -1 if no emoji value was found
    except ValueError:
        int_val = EMOJI_ROLLS.get(str_val, -1)
    return int_val
