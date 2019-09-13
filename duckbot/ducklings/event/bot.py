# Last Updated: 2.2
import util.common as util

# Bot handler class
class BotHandler:
    # Constructor for bot handler
    # Params: None
    # Return: BotHandler instance
    def __init__(self):
    #{{{
        self.logger = util.logger
        self.bots   = {}
    #}}}

    # Handle bot interaction
    # Params: event - bot message event
    # Return: list of response parameters
    def act(self, event):
    #{{{
        if event.user in self.bots:
            util.sendMessage(event.channel, "Check this out, kweh :duck:")
            util.sendMessage(event.channel, "Hello", self.bots[event.user])
    #}}}

    # Check if bot id is known and add it if not
    # Params: bot_id - bot id to check
    # Return: None
    def checkBotId(self, bot_id):
    #{{{
        # Add the bot to the list if it's not in there
        if bot_id not in self.bots:
            response = util.sc.api_call("bots.info", token=util.sc.token, bot=bot_id)
            if response["ok"]:
                self.bots[bot_id] = response["bot"]["user_id"]
                self.logger.log(DiagMessage("BOT0051D")) if util.debug else None
            else:
                self.logger.log(DiagMessage("BOT0040E"))
                self.logger.log(DiagMessage("BOT0041E", response["error"]))
        else:
            self.logger.log(DiagMessage("BOT0050D")) if util.debug else None
    #}}}
