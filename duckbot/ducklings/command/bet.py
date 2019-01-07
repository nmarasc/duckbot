# Duckbot check module
from ducklings.command.sub_check import balance
# Duckbot util modules
import util.moduleLoader as modloader
from util.common import matchUserID
from util.common import parseNum
from util.common import bank

# Valid command names
NAMES = [
    'BET'
]

# Game modules for bet
GAMES = modLoader.loadSubCommands('bet')
GAME_NAMES = list({GAMES[key].NAMES[0] for key in GAMES})

# Command help variables
PURPOSE = 'Bet on a game to win big'
USAGE = (
    f'Usage: <@{{id}}> {NAMES[0]} <amount> <game> <game-args>\n'
    f"Currently supported games: {', '.join(GAME_NAMES)}\n"
    f'Use HELP {NAMES[0]} <game> for details on game arguments'
)
#            ,util.GAMES["DICE"] :\
#                ("Roll the dice and guess even or odd\n"
#                "Usage options: DICE ( E[VENS] | O[DDS] )")
# Command responses
RESPONSE = {
    'LOSE': f"{{}}\nYou lost! You're down {{}} {bank.CURRENCY}",
    'WIN': f"{{}}\nYou won! You're up {{}} {bank.CURRENCY}"
}

# Command error responses
ERROR = {
    'BAD_BET': 'Invalid bet amount: {}',
    'BAD_GAME': 'Invalid game type: {}',
    'MISSING_ARGS': 'Not enough arguments: expected at least 2, got {}',
    'LOW_BALANCE': 'Your balance is too low to make this bet',
    'GAME_ARG': 'Game option error: {}'
}

# Bet bucks on a game to win more
# Params: user     - user id of player
#         channel  - channel id playing from
#         cmd_args - list containing argument text
# Return: String response from command
def handle(user, channel, cmd_args):
    # Parse out bet arguments
    bet_args = _parseBetArgs(cmd_args)
    # Check gambling eligibility and argument validity
    status = _checkStatus(user, channel, bet_args)
    if status:  # Some error with status check
        response = status
    else:  # No status error, make bet
        response = _bet(user, *bet_args)
    return response

# Make the bet on the game
# Params: user      - user playing the game
#         amount    - amount being bet
#         game      - game being played
#         game_args - list of arguments for the game
# Return:
def _bet(user, amount, game, game_args):
    # Verify balance
    if bank.getBalance(user) >= amount:
        return_code, result = GAMES[game].play(game_ops)
        # Lost
        if return_code == 0:
            self.bank.deduct(user, amount)
            response = RESPONSE['LOSE'].format(result, amount)
        # Won
        elif return_code == 1:
            self.bank.deposit(user, amount)
            response = RESPONSE['WIN'].format(result, amount)
        # Option error
        else:
            response = ERROR['GAME_ARG'].format(response)
    # Balance too low
    else:
        response = f"{ERROR['LOW_BALANCE']}\n{balance.check(user)}"
    return response

# Parse argument string for bet arguments
# Params: args - list of options to parse out
# Return: parsed argument list
def _parseBetArgs(args):
    upper_args = [a.upper() for a in args]
    if len(upper_args) < 2:
        result = None
    else:
        amount, game, *game_args = upper_args
        result = [parseNum(amount), GAMES.get(game, None), game_args]
    return result

# Check the eligibilty of user and channel for this command
# Params: user    - user id issuing command
#         channel - channel id command issued from
# Return: String error message or None
def _checkStatus(user, channel, bet_args):
    status = None
    return_code = bank.checkEligible(user, channel)
    if return_code == 1:  # Not a member
        status = bank.ERROR['NOT_A_MEMBER'].format(user)
    elif return_code == 2:  # Bad channel
        status = bank.ERROR['BAD_CHANNEL'].format(channel)
    else:
        status = _checkBetArgs(bet_args)
    return status

# Validate betting arguments
# Params: args - list of parsed bet arguments
# Return: String error message or None
def _checkBetArgs(args):
    status = None
    try:
        # Check for an invalid betting amount
        if args[0] < 1:
            status = ERROR['BAD_AMOUNT'].format(amount)
        # Check for an invalid game type
        elif args[1] not in GAMES:
            status = ERROR['BAD_GAME'].format(game)
    # Error if args was None, meaning there were arguments missing
    except TypeError:
        status = ERROR['MISSING_ARGS'].format(len(args))
    return status
