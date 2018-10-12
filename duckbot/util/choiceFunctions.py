# Last Updated: 2.3.0
import random

# Randomly get user to steal from
# Params: players - dict of user bank info
# Return: player entry to steal from
def randomChoice(players):
    return players[random.randrange(0,len(players))]
