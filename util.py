import re
import random

DEBUG = False
USER_REGEX = "<@(U[A-Z0-9]{8})>$"
#{{{ - Exit codes
EXIT_CODES = {
         "INVALID_BOT_ID"     : 10
        ,"RTM_CONNECT_FAILED" : 11
        }
#}}}
#{{{ - Emoji rolls
EMOJI_ROLLS={\
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
             'HI'     : 0, 'HELLO'      : 0,
             'UPDATE' : 1,
             'HELP'   : 2,
             'ROLL'   : 3, ':GAME_DIE:' : 3,
           }
#}}}

# matchUserId
# Returns True if Id is valid and matching Id, False otherwise
def matchUserId(id_str):
#{{{
    matches = re.search(USER_REGEX,id_str)
    return (True, matches.group(1)) if matches else (False, None)
#}}}

# getBotInfo
# Obtains bot's user Id and channels that it's a member of
def getBotInfo(sc, bot_token):
#{{{
    channels = []
    bot_id = sc.api_call("auth.test")["user_id"]
    response = sc.api_call("channels.list", token=bot_token, exclude_members=True)
    for channel in response["channels"]:
        if channel["is_member"]:
            print("Member of: " + channel["name"])
            channels.append(channel["id"])
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

# uniqueCommands
# Returns only one key of each value in the commands
def uniqueCommands(coms):
#{{{
    keys = []
    values = []
    for key in coms:
        if coms[key] not in values:
            keys.append(key)
            values.append(coms[key])
    return keys
#}}}
