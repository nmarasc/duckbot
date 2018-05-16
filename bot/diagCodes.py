''' * Message format *
    INI 001 1 E
      |   | | |
      |   | | Message type
      |   | Message part/variation
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

    MON0010I - Bot exited, RC=xx
    MON0011E - Python error, no restart (RC=01)
    MON0012I - Exit for update          (RC=02)
    MON0013E - RTM generic err, restart (RC=20)
    MON0014E - RTM timeour err, restart (RC=21)
    MON0019E - Unknown RC, restart      (RC=??)

    MON0020I - Bot starting update
    MON0021I - Bot update, success
    MON0021E - Bot update, failure

    MON0030E - Process failed to start, retry
    MON0031E - Process failed to start, quit

    MON0040E - Syntax check failed
'''
DIAG_CODES = {
    # Logger Messages
    # Log file started
     "LOG0000I" : "Starting new log..."
    # Flush
    ,"LOG0010I" : "Auto flushing buffer"
    # Flush buffer on exit
    ,"LOG0011I" : "Flushing buffer before exit"

    # Init Messages
    # Logger up and running
    ,"INI0000I" : "Logger is now running"
    # Display bot token
    ,"INI0010I" : "Bot token"
    # Slackclient connected
    ,"INI0020I" : "Slackclient connected"
    # Display bot id
    ,"INI0030I" : "Bot id"
    # Display bad bot id
    ,"INI0030E" : "Invalid bot id"
    # RTM connection good
    ,"INI0040I" : "RTM successfully connected"
    # RTM returned bad connection (msg)
    ,"INI0040E" : "RTM bad connection"
    # RTM returned bad connection (code)
    ,"INI0041E" : " -- Code"
    # RTM connect failed
    ,"INI0042E" : "Failed to connect to RTM"
    # Bot running
    ,"INI0050I" : "Duckbot now running"
    # Bot running in debug mode
    ,"INI0050D" : "Duckbot now running in debug mode"

    # Bot Messages
    # Starting bot initialization
    ,"BOT0000I" : "Initializing bot handlers..."
    # Handler
    ,"BOT0001I" : "Handler created"
    # Initialized
    ,"BOT0002I" : "Duckbot initialization complete"
    # User message
    ,"BOT0010U" : ""
    # Command processing
    ,"BOT0020I" : "Processing command"
    # RTM Generic error
    ,"BOT0030E" : "RTM read failed"
    # RTM Timeout
    ,"BOT0031E" : "RTM read TimeoutError"
    # Bot info request failed
    ,"BOT0040E" : "Bot info request failed"
    #     text of failed request
    ,"BOT0041E" : " -- Text"
    # Bot id not added
    ,"BOT0050I" : "Bot id not added to handler"
    # Bot id added
    ,"BOT0051I" : "Bot id added to handler"
    # Gamble channel update
    ,"BOT0060I" : "Gamble channel list update"
    #
}
