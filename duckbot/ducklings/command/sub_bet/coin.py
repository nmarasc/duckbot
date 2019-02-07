# Duckbot bet subcommand common module
from ducklings.command.sub_bet.common import ERROR
# Duckbot util modules
from util.common import roll
# Python imports
import re

# Valid command names
NAMES = [
   'COIN'
]

# Game argument regexes and results
HEAD_RGX = '^H(EADS?)?$'
TAIL_RGX = '^T(AILS?)?$'
RESULTS = ['HEADS','TAILS']

# Command help variables
PURPOSE = 'Flip a coin and call it'
USAGE = (
    f'Usage: {NAMES[0]} <coin-arg>\n'
    f"Valid command arguments include: {', '.join(RESULTS)}"
)

# Play the coin game
# Params: game_args - list of string arguments for game
# Return:  0 and result string on loss
#          1 and result string on win
#         -1 and error string otherwise
def play(game_args):
    # Process game arguments
    return_code, processed_val = _processArgs(game_args)
    if return_code == 0:
        # Flip the coin and get result
        roll_val = roll(2)
        response = f'You got: {RESULTS[roll_val - 1]}'
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
# Return:  0 and parsed roll value if valid
#         -1 and error message if invalid
def _processArgs(game_args):
    rc = 0
    # Check for required arguments
    if not game_args:
        rc = -1
        response = ERROR['MISSING_ARGS'].format(
            expect=1, actual=len(game_args), usage=USAGE
        )
    # Check for valid arguments
    elif re.match(HEAD_RGX, game_args[0]): # Matched HEADS
        response = 1
    elif re.match(TAIL_RGX, game_args[0]): # Matched TAILS
        response = 2
    else: # Did not match
        rc = -1
        response = ERROR['INVALID_ARGS'].format(usage=USAGE)
    return rc, response
