import re
import random
from datetime import datetime

DEBUG = False
USER_REGEX = "<@(U[A-Z0-9]{8})>$"
LABEL_REGEX = "\[:LABEL:(:.+:)+\]"
EMOJI_REGEX = ":.+?:"
DEFAULT_FN = "../log.txt"
#{{{ - Exit codes
EXIT_CODES = {
         "INVALID_BOT_ID"     : 10
        ,"RTM_CONNECT_FAILED" : 11
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

# matchUserId:
# Returns True if id is valid and matching id, False otherwise
def matchUserId(id_str):
#{{{
    matches = re.search(USER_REGEX,id_str)
    return (True, matches.group(1)) if matches else (False, None)
#}}}

# getBotInfo:
# Obtain bot id, workspace channels and which bot is a member of
def getBotInfo(sc, bot_token):
#{{{
    bot_id = sc.api_call("auth.test")["user_id"]
    channels = getChannelData(sc, bot_token)
    return bot_id, channels
#}}}

# getChannelData:
# Request channel list and build channel map
def getChannelData(sc, bot_token):
#{{{
    channels = {}
    channels["memberOf"] = []
    response = sc.api_call("channels.list", token=bot_token, exclude_members=True)
    for channel in response["channels"]:
        if channel["is_member"]:
            channels["memberOf"].append(channel["id"])
            print("Member of: " + channel["name"])
        channels[channel["id"]] = channel
        channels[channel["id"]]["labels"] = parseLabels(channel["purpose"]["value"])
    return channels
#}}}

# updateChannels:
# Make changes to channels list
def updateChannels(channels, event):
#{{{
    channel = event.channel
    if event.subtype == 'channel_purpose':
        channels[channel]["purpose"]["value"] = event.text
    elif event.subtype == 'channel_joined':
        if channel not in channels:
            channels[channel] = event.ch_data
        channels["memberOf"].append(channel)
    return channels
#}}}

# parseLabels:
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

# doRolls:
# Rolls randomly with the parameters given and returns numbers in a list
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
    # Initialize Logger with output file name or use default
    def __init__(self, fn = DEFAULT_FN, log = True):
    #{{{
        self.BUFFER_MAX = 5
        self.LOG_TIME = 3600 # 60 minutes
        self._log = log
        self.fn = fn
        self.log_buffer = []
        if self._log:
            with open(self.fn,'a') as logfile:
                logfile.write("Starting new log file...\n")
        self.last_log = datetime.now()
    #}}}

    # Append line to internal log buffer, flush if needed
    def log(self, text, flush=False):
    #{{{
        if self._log:
            self.log_buffer.append(str(datetime.now()) + ": " + text)
            timeDiff = (datetime.now() - self.last_log)
            if len(self.log_buffer) >= self.BUFFER_MAX or flush:
                self._write()
                self.last_log = datetime.now()
        elif not flush:
            print(text)
    #}}}

    # Write contents of buffer out to file with timestamp
    def _write(self):
    #{{{
        with open(self.fn,'a') as logfile:
            for line in self.log_buffer:
                try:
                    logfile.write(line)
                except TypeError:
                    logfile.write(str(datetime.now())+": LOG ERR")
                except UnicodeEncodeError:
                    logfile.write(str(line.encode("utf-8","replace")))
                logfile.write("\n")
            del self.log_buffer[:]
    #}}}
#}}}
