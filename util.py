import re

USER_REGEX = "<@(U[A-Z0-9]{8})>$"
EXIT_CODES = {\
         "INVALID_BOT_ID"     : 10\
        ,"RTM_CONNECT_FAILED" : 11\
        }


# matchUserId
# Returns True if Id is valid and matching Id, False otherwise
def matchUserId(id_str):
    matches = re.search(USER_REGEX,id_str)
    return (True, matches.group(1)) if matches else (False, None)

# getBotInfo
# Obtains bot's user Id and channels that it's a member of
def getBotInfo(sc, bot_token):
    channels = []
    bot_id = sc.api_call("auth.test")["user_id"]
    response = sc.api_call("channels.list", token=bot_token, exclude_members=True)
    for channel in response["channels"]:
        if channel["is_member"]:
            print("Member of: " + channel["name"])
            channels.append(channel["id"])
    return bot_id, channels
