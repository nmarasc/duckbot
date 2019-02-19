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
# Return: result dict with return code and message
def play(game_args):
    result = {'return_code': 0, 'message': '', 'error': ''}
    # Process game arguments
    processed = _processArgs(game_args)
    if processed['return_code'] == 0:
        # Flip the coin and get result
        roll_val = roll(2)
        result['message'] = f'You got: {RESULTS[roll_val - 1]}'
        if processed['choice'] == roll_val: # Win condition, else lost
            result['return_code'] = 1
    else: # Error condition
        result['error'] = processed['error']
    return result

# Retrieve command help message
# Params: None
# Return: String help message
def getHelp():
    return f'{PURPOSE}\n{USAGE}'

# Game argument processor
# Params: game_args - list of strings to check for arguments
# Return: result dict with return code and choice value or error message
def _processArgs(game_args):
    result = {'return_code': 0, 'choice': 0, 'error': ''}
    # Check for required arguments
    if not game_args:
        result['return_code'] = 1
        result['error'] = ERROR['MISSING_ARGS'].format(
            expect=1, actual=len(game_args), usage=USAGE
        )
    # Check for valid arguments
    elif re.match(HEAD_RGX, game_args[0]): # Matched HEADS
        result['choice'] = 1
    elif re.match(TAIL_RGX, game_args[0]): # Matched TAILS
        result['choice'] = 2
    else: # Did not match
        result['return_code'] = 2
        result['error'] = ERROR['INVALID_ARGS'].format(usage=USAGE)
    return result
