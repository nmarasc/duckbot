from util.bidict import bidict
from util import util

GAME_OPS = {
    #{{{ - Coin options
     "COIN_OPS" : bidict({
         "HEADS" : 1
        ,"TAILS" : 2
        ,"H"     : 1
        ,"T"     : 2
    })
    #}}}
    #{{{ - Dice options
    ,"DICE_OPS" : bidict({
         "EVENS" : 0
        ,"ODDS"  : 1
        ,"E"     : 0
        ,"O"     : 1
        ,"CHO"   : 0
        ,"HAN"   : 1
    })
    #}}}
}

# Play the coin game
# Params: game_ops - list of strings to check for options
# Return: result return code and message
def coinGame(game_ops):
#{{{
    # Process game options
    choice, response = processOps(game_ops, 1, "COIN")
    # Abort if bad
    if choice == -1:
        return choice, response

    # Flip the coin and report result
    roll = util.doRolls(2)[0]
    response = "You got: " + GAME_OPS["COIN_OPS"].inverse[roll][0]
    if choice == roll:
        return 1, response
    else:
        return 0, response
#}}}

# Play the dice game
# Params: game_ops - list of strings to check for options
# Return: result return code and message
def diceGame(game_ops):
#{{{
    # Process game options
    choice, response = processOps(game_ops, 1, "DICE")
    # Abort if bad
    if choice == -1:
        return choice, response

    # Roll the bones and determine result
    rolls = util.doRolls(6,2)
    response = "You rolled: " + ", ".join(map(str,rolls)) + " "
    result = sum(rolls) % 2
    response += "You got: " + GAME_OPS["DICE_OPS"].inverse[result][0]
    if choice == result:
        return 1, response
    else:
        return 0, response
#}}}

# Game option preprocessor
# Params: game_ops - list of strings to check for options
#         req_ops  - number of required options
#         game     - string of game checking
def processOps(game_ops, req_ops, game):
#{{{
    # Check for required options
    if len(game_ops) < req_ops:
        return -1, ("Missing required option(s)\n"
                    "Use HELP BET " + game + " command "
                    "for required options :duck:")
    # Check for valid options
    choice = GAME_OPS[game+"_OPS"].get(game_ops[0].upper(),-1)
    if choice == -1:
        return -1, ("Invalid options\n"
                    "Use HELP BET " + game + "command "
                    "for valid options :duck:")
    return choice, None
#}}}

#{{{ - Games
GAMES = {
     "COIN" : coinGame
    ,"DICE" : diceGame
}
#}}}
