# Last Updated: 2.2
# Python imports
import re
# Duckbot util modules
from util.common import roll

# Valid command names
NAMES = [
    'ROLL',
    ':GAME_DIE:'
]

# Command help message
HELP = (
    'Rolls dice based on parameters given\n'
    f'Usage: <@{{id}}> {NAMES[0]} ( [d]X | YdX )\n'
    'Where X is the number of faces and Y is the number of dice'
)

# Valid special roll names
NAMES_SPECIAL = {
    'CHARACTER': [
        'CHARACTER',
        'CHAR',
        ':DRAGON:'
    ]
}

# Valid emoji number values
EMOJI_ROLLS = {
           ':ONE:': 1,
           ':TWO:': 2,
         ':THREE:': 3,
          ':FOUR:': 4,
          ':FIVE:': 5,
           ':SIX:': 6,
         ':SEVEN:': 7,
         ':EIGHT:': 8,
          ':NINE:': 9,
    ':KEYCAP_TEN:': 10,
           ':100:': 100,
}

# Base emoji roll ratings
BASE_RATINGS = {
      1: ':hyperbleh:',
     13: ':ghost:',
     69: ':eggplant:',
    420: ':herb:'
}

# Regex used to determine a valid roll format of YdX or dX case
# Don't look at it. It's gross, but it works
EMOJI_REGEX = ':[a-zA-Z0-9_-+]+:'
VALUE_REGEX = '{}|\d+'.format(EMOJI_REGEX)
ROLL_REGEX = f'^({VALUE_REGEX})?D({VALUE_REGEX})$'
# Range for amount of dice and number of sides per die allowed
DIE_RANGE = range(1,101)

# Get response from proper sub roll command
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing command argument text
# Return:  String response from the command
def handle(user, channel, cmd_args):
    if not cmd_args:
        response = "Can't roll without parameters, kweh! :duck:"
    # Check for character roll
    elif str.upper(cmd_args[0]) in NAMES_SPECIAL['CHARACTER']:
        response = _characterRoll()
    # Otherwise regular roll command
    else:
        response = _defaultRoll(cmd_args[0])
    return response

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args):
    return HELP

# Standard roll command
# Params: roll_str - String containing roll command argument
# Return: String reponse from standard roll command
def _defaultRoll(roll_str):
    die_num = 1
    roll_upper = str.upper(roll_str)
    # Test parameter with regex for YdX or dX case
    regex_result = re.search(ROLL_REGEX, roll_upper)

    if regex_result:  # There was a match
        if regex_result.group(1):  # Y value
            die_num = _parseNum(regex_result.group(1))
        # X value
        die_sides = _parseNum(regex_result.group(2))

    else:  # No match, just a number
        die_sides = _parseNum(roll_upper)

    # Check that parameters are in the valid range
    if (die_num in DIE_RANGE and die_sides in DIE_RANGE):
        result = roll(die_sides, die_num)
        if isinstance(result, list):  # Rolled more than one number
            response_head = ', '.join(map(str, result))
            response_tail = f'\nYour total: {sum(result)}'
        else:  # Rolled only one number
            response_head = result
            response_tail = _emojiRating(result, die_sides)
        response = f'You rolled: {response_head} {response_tail}'
    # Invalid ranges
    else:
        response = f'{roll_str} is not a valid roll.'
    return response

# Roll for dnd character stats
# Params: None
# Return: String response from character roll command
def _characterRoll():
    stats = []
    results = []
    for i in range(0,6):  # For each stat
        group = roll(6,4)  # Roll 4d6
        group_min = min(group)
        result = (
            f"\nYou rolled: {', '.join(map(str, group))}"
            f'\nDropping {group_min}, Total: {{}}'
        )
        group.remove(group_min)  # Remove the lowest value
        stats.append(sum(group))  # Append sum to list of stats
        results.append(result.format(stats[-1]))
    results = '\n'.join(results)
    return f"{results}\n\nYour stats are: {', '.join(map(str, stats))}"

# Give emoji ratings based on roll score
# Params: roll - roll score to rate
#         die  - total to compare score to
# Return: emoji string for rating
def _emojiRating(roll, die):
    emoji = BASE_RATINGS.get(roll, None)
    if roll == die:
        emoji = ':partyparrot:'
    elif emoji is None:
        if roll <= die/2:
            emoji = ':bleh:'
        else:
            emoji = ':ok_hand:'
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
