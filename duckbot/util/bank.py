# Last Updated: 2.3.0
import random
import copy
from . import choiceFunctions as cFunc


# Bank class
# Manages user accounts and the gacha reserve
# External functions:
#
#   addUser - Create account for an id
class Bank:
    CURRENCY = "dux"
    DEFAULT_POOL  = [-1,-1,500,100,50,10,3,1]
    STARTING_POOL = [0,0,0,0,0,0,0,0]
    STARTING_BUX  = 100

    # Constructor for bank class
    # Params: None
    # Return: Bank instance
    def __init__(self):
    #{{{
        self.players = {}
        if util.bank_file:
            self.readState()
        else:
            self.gacha_pool = self.DEFAULT_POOL
    #}}}

    # Add user to bank
    # Params: user - user id to add to bank
    # Return: None
    def addUser(self, user):
    #{{{
        self.players[user] = {
             "balance" : self.STARTING_BUX
            ,"pool"    : copy.copy(self.STARTING_POOL)
            ,"pull"    : True
        }
    #}}}

    # Get balance of user
    # Params: user - user id to get balance of
    # Return: integer balance of user
    def getBalance(self, user):
        return self._userBalance(user, 0)

    # Add value to user's bank balance
    # Params: user   - user id to adjust
    #         amount - integer amount to adjust by
    # Return: None
    def deposit(self, user, amount):
        self._userBalance(user, amount)

    # Remove value from user's bank balance
    # Params: user   - user id to adjust
    #         amount - integer amount to remove
    # Return: None
    def deduct(self, user, amount):
        self._userBalance(user, -amount)

    # Get balance of user and adjust
    # Params: user   - user to get balance of
    #         adjust - amount to adjust user balance
    # Return: int val of user balance after adjusting
    def _userBalance(self, user, adjust):
        self.players[user]["balance"] += adjust
        return self.players[user]["balance"]

    # Get pool of user
    # Params: user - user to get pool of
    # Return: gacha pool
    def getPool(self, user):
        return self.players[user]["pool"]

    # Regen bux for low players
    # Params: None
    # Return: None
    def regen(self):
    #{{{
        for player in self.players:
            balance = self.players[player]["balance"]
            if balance <= 95:
                self.players[player]["balance"] += 5
            elif balance < 100:
                self.players[player]["balance"] = 100
    #}}}

    # Wipe all player's gacha pools
    # Params: None
    # Return: None
    def nuke(self):
    #{{{
        for player in self.players:
            self.players[player]["pool"] = self.STARTING_POOL
    #}}}

    # Remove the best item from a users gacha pool
    # Params: user - user id to remove from
    # Return: pull id of removed value or -1 if pool was empty
    def removeBest(self, user):
    #{{{
        pool = self.players[user]["pool"]
        try:
            pid = max([ind for ind, val in enumerate(pool) if val > 0])
            pool[pid] -= 1
            self.gacha_pool[pid] += 1
            return pid
        # Pool was empty
        except ValueError:
            return -1
    #}}}

    # Add value to user pool
    # Params: pid  - pull id to increase
    #         user - user id to add to
    # Return: True if added, False otherwise
    def addPool(self, pid, user):
    #{{{
        result = user
        # Attempt to steal because pool was empty
        if (self.gacha_pool[pid] == 0):
            chosen = self._steal(pid, user)
            if chosen: # another user was stolen from
                self.players[chosen]["pool"][pid] -= 1
                result = chosen
            else:      # the user owns them all
                return None
        # Taking from non infinite pool
        elif (self.gacha_pool[pid] > 0):
            self.gacha_pool[pid] -= 1
        self.players[user]["pool"][pid] += 1
        return result
    #}}}

    # Read in bank state file and initialize
    # Params: None
    # Return: None
    # Notes : Please don't write your own bank file.
    # You make mistakes, the bot doesn't
    def readState(self):
    #{{{
        reading_players = True
        try:
            with open("bank.dat","r") as data:
                for line in data:
                    line = line.strip()
                    # Skip comments
                    if line.startswith("#"):
                        pass
                    # Signal switch to pool
                    elif line.startswith(";"):
                        reading_players = False
                    # Parse line for player data
                    elif reading_players and line:
                        player_data = self._parsePlayerData(line.split(":"))
                        if player_data:
                            self.players[player_data[0]] = {
                                 "balance" : player_data[1]
                                ,"pool"    : player_data[2]
                                ,"pull"    : player_data[3]
                            }
                    # Parse line for gacha data
                    elif line:
                        self.gacha_pool = [int(val) for val in line.split(",")]
        # File doesn't exist, can't be read or gacha pool format error
        except (OSError, ValueError):
            self.gacha_pool = self.DEFAULT_POOL
    #}}}

    # Save bank state into file
    # Params: None
    # Return: None
    def saveState(self):
    #{{{
        try:
            with open("bank.dat","w") as data:
                # Write out player data
                data.write("# Players\n")
                for key in self.players:
                    data.write(key + ":" + str(self.players[key]["balance"]))
                    data.write(":" + ",".join(map(str,self.players[key]["pool"])))
                    data.write(":" + str(self.players[key]["pull"]))
                    data.write("\n")
                data.write(";\n")
                # Write pool data
                data.write("# Gacha Pool\n")
                data.write(",".join(map(str,self.gacha_pool)))
        # File couldn't be written
        except OSError:
            pass
    #}}}

    # Check if user in bank
    # Params: user - user id to check member status of
    # Return: True if member, false otherwise
    def isMember(self, user):
        return user in self.players

    # Check for free pull available
    # Params: user - uid to check
    # Return: True if available, False otherwise
    def hasFreePull(self, user):
        return self.players[user]['pull'] == True

    # Set free pull value of users
    # Params: value - boolean value to set user pull to
    #         user  - user id to set, if null sets all users
    # Return: None
    def setFreePull(self, value, user = None):
    #{{{
        if user:
            self.players[user]["pull"] = value
        else:
            for player in self.players:
                self.players[player]["pull"] = value
    #}}}

    # Check if user and channel are valid for gambling
    # Params: user    - user id to check for bank entry
    #         channel - channel id to check for approval
    # Return: integer return code
    def checkEligible(self, user, channel = None):
        return_code = 0
        if not self.isMember(user):
            return_code = 1
        if channel and channel not in self.approved_channels:
            return_code = 2
        return return_code

    # Parse player data of line
    # Params: data - line data
    # Return: player data list or None
    def _parsePlayerData(self, data):
    #{{{
        try:
            if len(data) == 4:
                player_data = [util.matchUserId(data[0])]
                player_data.append(int(data[1]))
                player_data.append([int(val) for val in data[2].split(",")])
                player_data.append(data[3] == "True")
                if player_data[0]:
                    return player_data
        except ValueError:
            pass
        return None
    #}}}

    # Steal pool id from a player
    # Params: pid  - pool id to steal
    #         user - user doing the stealing
    # Return: user id stolen from or None if nothing to steal
    def _steal(self, pid, user):
    #{{{
        players = self._getPlayersWithPid(pid, [user])
        if players: # there's people to steal from
            return cFunc.randomChoice(players)
        else:       # nobody has one
            return None
    #}}}

    # Get list of players that have that have a specfied pool id
    # Params: pid     - pool id to check for
    #         exclude - list of users to ignore
    # Return: list of player ids that have at least one specified pool id
    def _getPlayersWithPid(self, pid, exclude):
    #{{{
        return [player for player in self.players if
                self.players[player]["pool"][pid] and
                player not in exclude]
    #}}}
