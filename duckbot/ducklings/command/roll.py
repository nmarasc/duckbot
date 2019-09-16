# Last Updated: 2.2
# Python imports
import sys
import re
import logging
# Duckbot util modules
from duckbot.util.common import roll
from duckbot.util.common import parseNum

logger = logging.getLogger(__name__)

# Valid command names
NAMES = [
    'ROLL',
    ':GAME_DIE:'
]

# Command help variables
PURPOSE = 'Rolls dice based on parameters given'
USAGE = (
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

# Base emoji roll ratings
BASE_RATINGS = {
      1: ':hyperbleh:',
     13: ':ghost:',
     69: ':eggplant:',
    420: ':herb:'
}

# Regex used to determine a valid roll format of YdX or dX case
# Don't look at it. It's gross, but it works
EMOJI_REGEX = ':[a-zA-Z0-9_\-+]+:'
VALUE_REGEX = '{}|\d+'.format(EMOJI_REGEX)
ROLL_REGEX = f'^({VALUE_REGEX})?D({VALUE_REGEX})$'

# Dice constants
DIE_MAX_SIDES = sys.maxsize
DIE_MAX_NUM = 111
# Ranges for number of dice and number of sides per die
DIE_RANGE_NUM = range(1, DIE_MAX_NUM)
DIE_RANGE_SIDES = range(2, DIE_MAX_SIDES)

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
    return f'{PURPOSE}\n{USAGE}'

# Standard roll command
# Params: roll_str - String containing roll command argument
# Return: String reponse from standard roll command
def _defaultRoll(roll_str):
    die_num = 1
    roll_upper = str.upper(roll_str)
    # Test parameter with regex for YdX or dX case
    logger.info(f'{ROLL_REGEX} {roll_upper}')
    regex_result = re.search(ROLL_REGEX, roll_upper)

    if regex_result:  # There was a match
        if regex_result.group(1):  # Y value
            die_num = parseNum(regex_result.group(1))
        # X value
        die_sides = parseNum(regex_result.group(2))

    else:  # No match, just a number
        die_sides = parseNum(roll_upper)

    # Check values are in the valid ranges
    if (die_num not in DIE_RANGE_NUM):  # Invalid number of dice
        response = f'{die_num} is not in the valid range'
    elif (die_sides not in DIE_RANGE_SIDES):  # Invalid number of sides
        response = f'{die_sides} is not in the valid range'
    else:  # Ready to roll
        result = roll(die_sides, die_num)
        if isinstance(result, list):  # Rolled more than one number
            response_head = ', '.join(map(str, result))
            response_tail = f'\nYour total: {sum(result)}'
        else:  # Rolled only one number
            response_head = result
            response_tail = _emojiRating(result, die_sides)
        response = f'You rolled: {response_head} {response_tail}'
    logger.info(f'response: {response}')
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

