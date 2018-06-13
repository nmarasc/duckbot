import util.common as util

# Bank class
class Bank:
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
            ,"pool"    : self.STARTING_POOL
            ,"pull"    : True
        }
    #}}}

    # Get balance of user and adjust
    # Params: user   - user to get balance of
    #         adjust - amount to adjust user balance
    # Return: int val of user balance
    def balance(self, user, adjust = 0):
    #{{{
        if adjust:
            self.players[user]["balance"] += adjust
        return self.players[user]["balance"]
    #}}}

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
                        self.gacha_pool = list(map(int,line.split(",")))
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

    # Check for free pull available and disable it
    # Params: user - uid to check
    # Return: True if available, False otherwise
    def freePull(self, user):
    #{{{
        if self.players[user]["pull"]:
            self.players[user]["pull"] = False
            return True
        return False
    #}}}

    # Parse player data of line
    # Params: data - line data
    # Return: player data list or None
    def _parsePlayerData(self, data):
    #{{{
        try:
            if len(data) == 4:
                player_data = [util.matchUserId(data[0])]
                player_data.append(int(data[1]))
                player_data.append(list(map(int,data[2].split(","))))
                player_data.append(data[3] == "True")
                if player_data[0]:
                    return player_data
        except ValueError:
            pass
        return None
    #}}}
