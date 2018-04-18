import re
import random
import datetime

DEBUG = False
USER_REGEX = "<@(U[A-Z0-9]{8})>$"
DEFAULT_FN = "log.txt"
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
    'HI'      : 1,
    'UPDATE'  : 2,
    'HELP'    : 3,
    'ROLL'    : 4,
    'COIN'    : 5,
    '8BALL'   : 6,
    'FACTOID' : 7,
    'PICKIT'  : 8,
           }
COMMANDS_ALT = {
    'HELLO'      : 1, 'KWEH'       : 1,
    '?'          : 3, ':QUESTION:' : 3,
    ':GAME_DIE:' : 4,
    ':8BALL:'    : 6,
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

# matchUserId
# Returns True if id is valid and matching id, False otherwise
def matchUserId(id_str):
#{{{
    matches = re.search(USER_REGEX,id_str)
    return (True, matches.group(1)) if matches else (False, None)
#}}}

# getBotInfo
# Obtain bot id, workspace channels and which bot is a member of
def getBotInfo(sc, bot_token):
#{{{
    channels = {}
    channels['memberOf'] = []
    bot_id = sc.api_call("auth.test")["user_id"]
    response = sc.api_call("channels.list", token=bot_token, exclude_members=True)
    for channel in response["channels"]:
        if channel["is_member"]:
            channels['memberOf'].append(channel["id"])
            print("Member of: " + channel["name"])
        channels[channel["name"]] = channel["id"]
    return bot_id, channels
#}}}

# doRolls
# Rolls randomly with the parameters given and returns numbers in a list
def doRolls(die_size, die_num = 1):
#{{{
    rolls = []
    for i in range(die_num):
        rolls.append(random.randint(1,die_size))
    return rolls
#}}}

# uniqueKeys
# Returns list of one keys per value in dict
def uniqueKeys(p_dict):
#{{{
    keys = []
    values = []
    for key in p_dict:
        if p_dict[key] not in values:
            keys.append(key)
            values.append(p_dict[key])
    return keys
#}}}

# Logger class
# Buffers and writes messages to a file
class Logger:
#{{{
    # Initialize Logger with output file name or use default
    def __init__(self, fn = DEFAULT_FN):
    #{{{
        self.fn = fn
        self.LOG_BUFFER = []
        with open(self.fn,'w') as logfile:
            logfile.write("Starting new log file...\n")
    #}}}

    # Append line to internal log buffer
    def buffer(self, text):
        self.LOG_BUFFER.append(text)

    # Write contents of buffer out to file with timestamp
    def write(self, text = ""):
    #{{{
        with open(self.fn,'a') as logfile:
            if text:
                logfile.write(text + "\n")
            else:
                for line in self.LOG_BUFFER:
                    try:
                        logfile.write(str(datetime.datetime.now())+": " + line)
                    except TypeError:
                        logfile.write(str(datetime.datetime.now())+": LOG ERR")
                    except UnicodeEncodeError:
                        logfile.write(str(datetime.datetime.now())+": " +\
                                      str(line.encode("utf-8","replace")))
                    logfile.write("\n")
                del self.LOG_BUFFER[:]
    #}}}
#}}}
