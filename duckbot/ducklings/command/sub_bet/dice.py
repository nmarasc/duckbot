# Duckbot bet subcommand common module
from ducklings.command.sub_bet.common import ERROR
# Duckbot util modules
from util.common import roll
# Python imports
import re

# Valid command names
NAMES = [
   'DICE',
   'ROLL',
   ':GAME_DIE:'
]

# Game regexes and results
EVEN_RGX = [
    re.compile('^E(VENS?)?$'),
    re.compile('^CHO$')
]
ODD_RGX = [
    re.compile('^O(DDS?)?$'),
    re.compile('^HAN$')
]
RESULTS = ['EVEN','ODD']

# Command help variables
PURPOSE = 'Flip a coin and call it'
USAGE = (
    f'Usage: {NAMES[0]} <coin-arg>\n'
    f"Valid command arguments include: {', '.join(RESULTS)}"
)

# Play the dice game
# Params: game_args - list of string arguments for the game
# Return:  0 and result string on loss
#          1 and result string on win
#         -1 and error string otherwise
def play(game_args):
    # Process game arguments
    return_code, processed_val = _processArgs(game_args)
    if return_code = 0:
        # Roll dice and get result
        roll_val = sum(roll(6,2)) % 2
        response = f'You got: {RESULTS[roll_val]}'
        if processed_val == roll_val: # Win condition, otherwise lost
            return_code = 1
    else: # Error condition
        response = processed_val
    return return_code, response

# Retrieve command help message
# Params: None
# Return: String help message
def getHelp():
    return f'{PURPOSE}\n{USAGE}'

# Game argument processor
# Params: game_args - list of strings to check for arguments
# Return:  0 and parsed win condition if valid
#         -1 and error message if not valid
def _processArgs(game_args):
    rc = 0
    # Check for required arguments
    if not game_args:
        rc = -1
        response = ERROR['MISSING_ARGS'].format(
            expect=1, actual=len(game_args), usage=USAGE
        )
    # Check for valid arguments
    elif any(rgx.match(game_args[0]) for rgx in EVEN_RGX): # Matched EVEN
        response = 0
    elif any(rgx.match(game_args[0]) for rgx in ODD_RGX): # Matched ODD
        response = 1
    else: # Did not match
        rc = -1
        response = ERROR['INVALID_ARGS'].format(usage=USAGE)
    return rc, response
