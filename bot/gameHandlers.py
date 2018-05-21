import util

#{{{ - Coin options
COIN_OP = util.bidict({
     "HEADS" : 1
    ,"TAILS" : 2
    ,"H"     : 1
    ,"T"     : 2
})
#}}}

# Play the coin game
# Params: game_ops
# Return: result return code and message
def coinGame(game_ops):
#{{{
    # Check for required option
    if len(game_ops) < 1:
        return -1, ("Missing required option\n"
                    "Use HELP BET COIN command for required options :duck:")
    # Check for valid option
    choice = COIN_OP.get(game_ops[0].upper(),0)
    if not choice:
        return -1, ("Invalid option\n"
                    "Use HELP BET COIN command for valid options :duck:")
    # Flip the coin and report result
    roll = util.doRolls(2)[0]
    response = "You got: " + COIN_OP.inverse[roll][0]
    if choice == roll:
        return 1, response
    else:
        return 0, response
#}}}

#{{{ - Games
GAMES = {
     "COIN" : coinGame
}
#}}}
