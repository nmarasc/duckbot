import util.common as util

# Help handler class
class HelpHandler:
    # Constructor for Help handler
    # Params: bot_id - user id for the bot
    # Return: HelpHandler instance
    def __init__(self, bot_id):
    #{{{
        self.bot_id = bot_id
        #{{{ - Help messages
        self.help_messages = {
             util.COMMANDS["HI"] :\
                ("Legacy HI command\n"
                "Usage: <@" + bot_id + "> HI")
            ,util.COMMANDS["UPDATE"] :\
                ("Causes the bot to shutdown and signal "
                "the monitor script to check for updates\n"
                "Usage: <@" + bot_id + "> UPDATE")
            ,util.COMMANDS["HELP"] :\
                "Don't get smart, you know how to use this"
            ,util.COMMANDS["ROLL"] :\
                ("Rolls dice based on parameters given\n"
                "Usage: <@" + bot_id + "> ROLL ( [d]X | YdX )\n"
                "Where X is the number of faces and Y is the number of dice")
            ,util.COMMANDS["COIN"] :\
                ("Flip a coin\n"
                "Usage: <@" + bot_id + "> COIN")
            ,util.COMMANDS["EIGHTBALL"] :\
                ("Shake the magic 8ball\n"
                "Usage: <@" + bot_id + "> 8BALL")
            ,util.COMMANDS["FACTOID"] :\
                ("Pull out a random and totally true fact\n"
                "Usage: <@" + bot_id + "> FACTOID")
            ,util.COMMANDS["PICKIT"] :\
                ("Pick from a number of things\n"
                "Usage: <@" + bot_id + "> PICKIT <item1> <item2> ...\n"
                "Use quotes to have items with spaces in them :duck:")
            ,util.COMMANDS["JOIN"] :\
                ("Add yourself to the gambler's bank\n"
                "Usage: <@" + bot_id + "> JOIN\n"
                "Can only be used in gambling approved channels :duck:")
            ,util.COMMANDS["CHECKBUX"] :\
                ("Check bank balance of yourself or others\n"
                "Usage: <@" + bot_id + "> CHECKBUX [target]\n"
                "No target defaults to yourself :duck:")
            ,util.COMMANDS["BET"] :\
                ("Bet on a game with bank balance to win big\n"
                "Usage: <@" + bot_id + "> BET <amount> <game> <game-options>\n"
                "List of currently supported games: " + ", ".join(util.GAMES) + "\n"
                "Use HELP BET <game> for details on options")
        }
        #}}}
        #{{{ - Game help messages
        self.game_help_messages = {
             util.GAMES["COIN"] :\
                ("Flip a coin and call it\n"
                "Usage options: COIN ( H[EADS] | T[AILS] )")
            ,util.GAMES["DICE"] :\
                ("Roll the dice and guess even or odd\n"
                "Usage options: DICE ( E[VENS] | O[DDS] )")
        }
        #}}}
    #}}}

    # Retrieve help message based on passed values
    # Params: parms - list of strings to check for help commands
    # Return: requested help messages or generic one if no specific
    def act(self, parms):
    #{{{
        if parms:
            command = util.COMMANDS.get(parms[0],0)
            command = util.COMMANDS_ALT.get(parms[0],0) if not command else command
            if command == util.COMMANDS["BET"] and len(parms) > 1:
                subcommand = util.GAMES.get(parms[1],0)
                response = self.game_help_messages.get(subcommand,
                    parms[1] + " is not a recognized game")
                return response
            else:
                response = self.help_messages.get(command,
                    parms[0] + " is not a recognized command")
                return response
        else:
            return ("Duckbot is a general purpose slackbot for doing various things\n"
                    "To interact with it use <@" + self.bot_id + "> <command>\n"
                    "Supported commands: " + ", ".join(util.COMMANDS) + "\n"
                    "Use <@" + self.bot_id + "> HELP <command> for more details")
    #}}}
