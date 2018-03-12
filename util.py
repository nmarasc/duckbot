import re

EXIT_CODES = {\
         "INVALID_BOT_ID"     : 10\
        ,"RTM_CONNECT_FAILED" : 11\
        }


# validUserId
# Returns True if Id is valid, False otherwise
def validUserId(id_str):
    pattern = re.compile("^U[A-Z0-9]{8}$")
    return pattern.match(id_str)
