# Duckbot
General purpose slack bot

Current version: `2.2`
</br>
`main.py` is the driver for the bot. It handles creating the bot, connecting to slack, and the rtm read loop
</br>`duckbot.py` sets up the event handlers, assigning them appropriately and sending messages
</br>`eventHandlers.py` contains all the event handlers and their specific parsers
</br>`commandHandlers.py` contains the handlers for bot commands
</br>`util.py` contains various utility functions, such as ID matching and exit codes

Bot return codes:</br>
</br>RC=0x exit codes are special meaning codes, usually for signalling monitor script
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=00 , bot exited normally and will not restart
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=01 , there was an uncaught python error and will not restart. Likely needs manual fixing
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=02 , bot exited normally and will restart after updating
</br>
</br>RC=1x exit codes signify an error during bot set up
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=10 , invalid bot id was returned to bot, should restart
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=11 , failed to connect to RTM, possible network hiccup, should restart
</br>
</br>RC=2x exit codes signify an error during rtm use
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=20 , generic error during RTM read, should restart
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=21 , timeout error during RTM read, should restart
</br>
</br>RC=3x exit codes signify an error during command processing
</br>&nbsp;&nbsp;&nbsp;&nbsp;RC=30 , malformed user id found
