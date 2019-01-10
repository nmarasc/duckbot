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
EVEN_RGX = '^E(VENS?)?$'
ODD_RGX = '^O(DDS?)?$'
RESULTS = ['CHO','HAN']

# Command help variables
PURPOSE = 'Flip a coin and call it'
USAGE = (
    f'Usage: {NAMES[0]} <coin-arg>\n'
    f"Valid command arguments include: {', '.join(RESULTS)}"
)

