# Python imports
import re
import random
from datetime import datetime
from diagCodes import DIAG_CODES

# Util constants
RTM_READ_DELAY = 1
USER_REGEX = "U[A-Z0-9]{8}"
LABEL_REGEX = "\[:LABEL:(:.+:)+\]"
EMOJI_REGEX = ":.+?:"
DEFAULT_FN = "../log.txt"
#{{{ - Exit codes
EXIT_CODES = {
         "INVALID_BOT_ID"     : 10
        ,"RTM_CONNECT_FAILED" : 11
        ,"RTM_BAD_CONNECTION" : 12
        ,"RTM_GENERIC_ERROR"  : 20
        ,"RTM_TIMEOUT_ERROR"  : 21
        }
#}}}
#{{{ - Emoji rolls
EMOJI_ROLLS={
         ":ONE:"        : 1
        ,":TWO:"        : 2
        ,":THREE:"      : 3
        ,":FOUR:"       : 4
        ,":FIVE:"       : 5
        ,":SIX:"        : 6
        ,":SEVEN:"      : 7
        ,":EIGHT:"      : 8
        ,":NINE:"       : 9
        ,":KEYCAP_TEN:" : 10
        ,":100:"        : 100
        ,":HERB:"       : 420
        }
#}}}
#{{{ - Commands
COMMANDS = {
    'HI'        :  1,
    'UPDATE'    :  2,
    'HELP'      :  3,
    'ROLL'      :  4,
    'COIN'      :  5,
    'EIGHTBALL' :  6,
    'FACTOID'   :  7,
    'PICKIT'    :  8,
    'JOIN'      :  9,
    'CHECKBUX'  : 10,
    'BET'       : 11,
           }
COMMANDS_ALT = {
    'HELLO'      : 1, 'KWEH'       : 1,
    '?'          : 3, ':QUESTION:' : 3,
    ':GAME_DIE:' : 4,
    ':8BALL:'    : 6, '8BALL'      : 6,
}
#}}}
#{{{ - Eightball Responses
EIGHTBALL_RESPONSES = [
     "It is certain"
    ,"It is decidedly so"
    ,"Without a doubt"
    ,"Yes, definitely"
    ,"You may rely on it"
    ,"As I see it, yes"
    ,"Most likely"
    ,"Outlook good"
    ,"Yes"
    ,"Signs point to yes"
    ,"Reply hazy, try again"
    ,"Ask again later"
    ,"Better not tell you now"
    ,"Cannot predict now"
    ,"Concentrate and ask again"
    ,"Don't count on it"
    ,"My reply is no"
    ,"My sources say no"
    ,"Outlook not so good"
    ,"Very doubtful"
    ]
#}}}
#{{{ - Channel labels
LABELS = {
     'DUCKBOT' : ':DUCKBOT:'
    ,'GAMBLE'  : ':SLOT_MACHINE:'
}
#}}}

# Slackclient, Logger instance
# debug and permanent bank flag
global sc, logger, debug, bank_file

# Send message to designated channel, and notify user if present
# Params: channel - channel id to send message to
#         message - string message to send
#         user    - user id to notify, not required
# Return: None
def sendMessage(channel, message, user = None):
#{{{
    # Prepend user notification if specified
    if user:
        message = "<@" + user + "> " + message
    sc.rtm_send_message(channel, message)
#}}}

# Search for a user id in a string
# Params: id_str - string to search for id
# Return: user id if found, None otherwise
def matchUserId(id_str):
#{{{
    matches = re.search(USER_REGEX,id_str)
    return matches.group(0) if matches else None
#}}}

# Obtain bot id and workspace channels
# Params: sc        - slackclient instance to make api calls
#         bot_token - connection token for the bot
# Return: bot user id and channel dict
def getBotInfo(bot_token):
#{{{
    bot_id = sc.api_call("auth.test")["user_id"]
    channels = getChannelData(bot_token)
    return bot_id, channels
#}}}

# Request channel list and build channel map
# Params: sc        - slackclient instance to make api calls
#         bot_token - connection token for the bot
# Return: dict of channel ids to channel data
def getChannelData(bot_token):
#{{{
    channels = {}
    response = sc.api_call("channels.list", token=bot_token, exclude_members=True)
    for channel in response["channels"]:
        channels[channel["id"]] = channel
        channels[channel["id"]]["labels"] = parseLabels(channel["purpose"]["value"])
    return channels
#}}}

# Make changes to channels list based on event data
# Params: channels - dict of channels to update
#         event    - event to update from
# Return: updated channel dict
def updateChannels(channels, event):
#{{{
    channel = event.channel
    if event.subtype == 'channel_purpose':
        channels[channel]["purpose"]["value"] = event.text
    elif event.subtype == 'channel_joined':
        if channel not in channels:
            channels[channel] = event.channel_data
    return channels
#}}}

# Split text into a list of labels
# Params: text - string to split up
# Return: list of labels
def parseLabels(text):
#{{{
    labels = []
    text = "".join(text.split()).upper()
    match = re.search(LABEL_REGEX, text, flags=re.IGNORECASE)
    if match:
        text = match.group(1)
        match = re.match(EMOJI_REGEX, text)
        while match:
            labels.append(match.group(0))
            text = text[match.span(0)[1]:]
            match = re.match(EMOJI_REGEX, text)
    return labels
#}}}

# Rolls randomly with the parameters given and returns numbers in a list
# Params: die_size - number of sides on the dice rolling
#         die_num  - number of times to roll the dice
# Return: list of rolls
def doRolls(die_size, die_num = 1):
#{{{
    rolls = []
    for i in range(die_num):
        rolls.append(random.randint(1,die_size))
    return rolls
#}}}

# Logger class
# Buffers and writes messages to a file
class Logger:
#{{{
    BUFFER_MAX = 10
    LOG_TIME = 1800 # 30 minutes

    # Constructor for logger class
    # Params: fn  - file name to use or leave default
    #         log - flag to keep a log file or not
    # Return: Logger instance
    def __init__(self, fn = DEFAULT_FN, log = True):
    #{{{
        self.keep_log = log
        self.fn = fn
        self.log_buffer = []
        if self.keep_log:
            self.log(DiagMessage("LOG0000I"))
    #}}}

    # Append line to internal log buffer, flush if needed
    # Params: diag  - DiagMessage to log
    #         flush - bool flag for flushing buffer early
    # Return: None
    def log(self, diag, flush=False):
    #{{{
        if self.keep_log:
            self.log_buffer.append(str(datetime.now()) + " - " + diag.msg)
            if len(self.log_buffer) >= self.BUFFER_MAX or flush:
                self._write()
        elif not flush:
            print(diag.msg)
    #}}}

    # Write contents of buffer out to file
    # Params: None
    # Return: None
    def _write(self):
    #{{{
        print("Writing log...") if debug else None
        with open(self.fn,'a') as logfile:
            for line in self.log_buffer:
                try:
                    logfile.write(line)
                except TypeError:
                    logfile.write(str(datetime.now())+" - LOG ERR")
                except UnicodeEncodeError:
                    logfile.write(str(line.encode("utf-8","replace")))
                logfile.write("\n")
        del self.log_buffer[:]
    #}}}
#}}}

# Diag Message class
class DiagMessage:
#{{{
    # Constructor for diag message
    # Params: code   - diag code for message
    #         fill   - strings to fill in text
    # Return: DiagMessage instance
    def __init__(self, code, *fill):
    #{{{
        self.code = code
        self.text = DIAG_CODES[code]
        self.msg  = self.code + " " + self.text
        if fill and self.text:
            self.msg += ": " + " - ".join(fill)
        elif fill and not self.text:
            self.msg += ": ".join(fill)
    #}}}
#}}}

# Bank class
class Bank:
#{{{
    DEFAULT_POOL  = [-1,-1,500,100,50,10,3,1]
    STARTING_POOL = [0,0,0,0,0,0,0,0]
    STARTING_BUX  = 100

    # Constructor for bank class
    # Params: None
    # Return: Bank instance
    def __init__(self):
    #{{{
        self.players = {}
        if bank_file:
            self.readState()
        else:
            self.gacha_pool = self.DEFAULT_POOL
    #}}}

    # Read in bank state file and initialize
    # Params: None
    # Return: None
    # Notes : Please don't write your own bank file.
    # You make mistakes, the bot doesn't
    def readState(self):
    #{{{
        try:
            with open("bank.dat","r") as data:
                # Read in players
                for line in data:
                    line = line.strip()
                    # Skip comments
                    if line.startswith("#"):
                        pass
                    # Signal switch to pool
                    elif line.startswith(";"):
                        break
                    # Read the player
                    elif line:
                        line_data = line.split(":")
                        if len(line_data) > 2:
                            self.players[line_data[0]] = {
                                 "balance" : int(line_data[1])
                                ,"pool"    : list(map(int,line_data[2].split(",")))
                            }
                line = data.readline().strip()
                # Skip comments
                while line.startswith("#"):
                    line = data.readline().strip()
                if line:
                    self.gacha_pool = list(map(int,line.split(",")))
        # File doesn't exist or can't be read
        except OSError:
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

    # Add user to bank
    # Params: user - user id to add to bank
    # Return: None
    def addUser(self, user):
    #{{{
        self.players[user] = {
             "balance" : self.STARTING_BUX
            ,"pool"    : self.STARTING_POOL
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
#}}}

# Bidirectional dictionary class
# Credit belongs to a dude on stackoverflow
class bidict(dict):
#{{{
    # Constructor for bidict
    # Params: same as regular dict
    # Return: bidict instance
    def __init__(self, *args, **kwargs):
    #{{{
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value,[]).append(key)
    #}}}

    # Set value in both directions
    # Params: key   - index to map value to
    #         value - value to map key to
    # Return: None
    def __setitem__(self, key, value):
    #{{{
        if key in self:
            self.inverse[self[key]].remove(key)
        super(bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value,[]).append(key)
    #}}}

    # Remove key from dict
    # Params: key - key to remove
    # Return: None
    def __delitem__(self, key):
    #{{{
        self.inverse.setdefault(self[key],[]).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(bidict, self).__delitem__(key)
    #}}}
#}}}
