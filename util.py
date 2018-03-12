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
