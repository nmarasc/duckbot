''' * Message format *
    INI 001 1 E
      |   | | |
      |   | | Message type
      |   | Message part
      |   Message number
      Message issuer
'''
''' * Message issuer/stage *
    LOG - Logger status
    INI - Bot init
    BOT - Bot runtime
    MON - Monitor messages
'''
''' * Message type *
    U - User
    I - Info
    E - Error
    D - Debug
'''
''' * Monitor messages *
    MON0000I - Bot started
    MON0010I - Bot exited, RC=0
    MON0011I - Bot exited, RC=2
    MON0020I - Bot updating, success

    MON0010E - Process failed to start, retry
    MON0011E - Process failed to start, quit
'''
DIAG_CODES = {
    # Logger Info Messages
    # Clear buffer on exit
     "LOG0000I" : "Clearing buffer before exit"

    # Init Info Messages
    # Display bot token
    ,"INI0000I" : "Bot token"

    # Init Error Messages
    # Display bad bot id
    ,"INI0000E" : "Invalid bot id"
    # RTM returned bad connection (msg)
    ,"INI0010E" : "Connection error"
    # RTM returned bad connection (code)
    ,"INI0011E" : " -- Code"
    # RTM connect failed
    ,"INI0020E" : "Failed to connect to RTM"

    # Init Debug Messages
    # Started debug mode
    ,"INI0000D" : "Duckbot running in debug mode"

    # Bot Error Messages
    # RTM Timeout
    ,"BOT0000E" : "RTM read TimeoutError"
    # RTM Generic error
    ,"BOT0010E" : "RTM read failed"
}
