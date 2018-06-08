# Python imports
import re
import shlex
from datetime import datetime, date, time
# Project imports
import util
from util import DiagMessage
from util import Bank
from gameHandlers import *

# Handler instances
global help_handler, roll_handler, gamble_handler

# Help handler class
class HelpHandler:
#{{{

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
                "List of currently supported games: " + ", ".join(GAMES) + "\n"
                "Use HELP BET <game> for details on options")
        }
        #}}}
        #{{{ - Game help messages
        self.game_help_messages = {
             GAMES["COIN"] :\
                ("Flip a coin and call it\n"
                "Usage options: COIN ( H[EADS] | T[AILS] )")
            ,GAMES["DICE"] :\
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
                subcommand = GAMES.get(parms[1],0)
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
#}}}

# Roll handler class
class RollHandler:
#{{{
    ROLL_REGEX="^(:[a-z0-9_-]+:|\d+)?D(:[a-z0-9_-]+:|\d+)$"
    #{{{ - CHARACTER_ROLLS
    CHARACTER_ROLLS = [
         ":DRAGON:"
        ,"CHARACTER"
        ,"CHAR"
    ]
    #}}}

    # Constructor for Roll handler
    # Params: None
    # Return: RollHandler instance with ranges and regex initialized
    def __init__(self):
    #{{{
        # Range from 1-100 allowed
        self.die_range=range(1,101)
        # Can pick from 2-20 things
        self.pick_range=range(2,21)
    #}}}

    # Parse roll command parms and return values
    # Params: roll_parms - list of roll parameters
    # Return:  0, list of rolls
    #          1, list of stats
    #         -1, None for bad param
    #         -2, None for no param
    def roll(self, roll_parms):
    #{{{
        if not roll_parms:
            return -2, None
        # Check for character roll
        elif roll_parms[0] in self.CHARACTER_ROLLS:
            return 1, self.characterRoll()

        results = re.search(self.ROLL_REGEX, roll_parms[0])

        # If we matched a dX or YdX case
        if results:
        #{{{
            # YdX case
            if results.group(1):
                # Numeric
                try:
                    die_num = int(results.group(1))
                # Or emoji
                except ValueError:
                    die_num = util.EMOJI_ROLLS.get(results.group(1),-1)
            else:
                die_num = 1

            # dX half
            # Numeric
            try:
                die_size = int(results.group(2))
            # Or emoji
            except ValueError:
                die_size = util.EMOJI_ROLLS.get(results.group(2),-1)
        #}}}
        # Just X case
        else:
        #{{{
            die_num = 1
            # Numeric
            try:
                die_size = int(roll_parms[0])
            # Or emoji
            except ValueError:
                die_size = util.EMOJI_ROLLS.get(roll_parms[0],-1)
        #}}}

        # Check range for valid rolls
        if (die_num in self.die_range and die_size in self.die_range):
        #{{{
            rolls = util.doRolls(die_size, die_num)
            if die_num == 1:
                rolls.append(self._emojiRating(rolls[0], die_size))
            else:
                rolls.append(sum(rolls))
            return 0, rolls
        #}}}
        else:
            return -1, None
    #}}}

    # Roll for dnd character stats
    # Params: None
    # Return: list of stat lists
    def characterRoll(self):
    #{{{
        rolls = []
        for i in range(0,6):
            rolls.append(util.doRolls(6,4))
        return rolls
    #}}}

    # Roll for coin flip
    # Params: None
    # Return: heads or tails
    def coinRoll(self):
    #{{{
        result = util.doRolls(2)[0]
        if result == 1:
            return "HEADS"
        else:
            return "TAILS"
    #}}}

    # Roll for 8ball response
    # Params: None
    # Return: eight ball message
    def eightballRoll(self):
    #{{{
        roll = util.doRolls(len(util.EIGHTBALL_RESPONSES))[0]
        return util.EIGHTBALL_RESPONSES[roll]
    #}}}

    # Roll for pickit response
    # Params: pick_parms - string to split and pick from
    # Return: 0, chosen thing
    #         1, range to pick from for error
    def pickitRoll(self, pick_parms):
    #{{{
        try:
            # Split on spaces while preserving quoted strings,
            # then remove empty strings because people suck
            pick_parms = shlex.split(" ".join(pick_parms))
            pick_parms = [val for val in pick_parms if val != ""]
        except ValueError:
            return 2, None
        if len(pick_parms) in self.pick_range:
            return 0, pick_parms[util.doRolls(len(pick_parms))[0]-1]
        else:
            return 1, self.pick_range
    #}}}

    # Roll for factoid response
    # Params: None
    # Return: Generated factoid (nothing for right now)
    def factoidRoll(self):
        return "Not yet. Kweh :duck:"

    # Give emoji ratings based on roll score
    # Params: roll - roll score to rate
    #         die  - total to compare score to
    # Return: emoji string for rating
    def _emojiRating(self, roll, die):
    #{{{
        if roll == 1:
            return ":hyperbleh:"
        elif roll == die:
            return ":partyparrot:"
        elif roll == 69:
            return ":eggplant:"
        elif roll == 420:
            return ":herb:"
        elif roll <= die/2:
            return ":bleh:"
        else:
            return ":ok_hand:"
    #}}}

#}}}

# Gambling handler class
class GambleHandler:
#{{{
    BAD_CHANNEL_MSG = ("Sorry, this is not an approved "
        "channel for gambling content\n Please keep it to "
        "channels with the :slot_machine: label :duck:")
    CURRENCY = "duckbux"
    REFRESH_TIME = datetime(1,1,1,12)
    PULL_RANGE = range(1,11)
    #{{{ - Gacha ranges
    GACHA_RANGES = {
         range(50,150)    : [0,"Trash"]
        ,range(150,600)   : [1,"Common"]
        ,range(600,800)   : [2,"Uncommon"]
        ,range(800,900)   : [3,"Rare"]
        ,range(900,975)   : [4,"Super Rare"]
        ,range(975,990)   : [5,"Ultra Rare"]
        ,range(990,1000)  : [6,"SS Ultra Secret Rare"]
        ,range(1000,1001) : [7,"1000-chan"]
    }
    #}}}

    # Constructor for gamble handler
    # Params: channels - list of channels to check for approved labels
    # Return: GambleHandler instance with approved channels added
    def __init__(self, channels):
    #{{{
        self.GAMES = GAMES
        self.logger = util.logger
        self.approved_channels = self._getApproved(channels)
        self.bank = Bank()
        self.pull_timer = self._getRefreshTime()
    #}}}

    # Add user to bank if not in already
    # Params: user    - user id to check for bank entry
    #         channel - channel trying to add from
    # Return: Message to send to channel
    def join(self, user, channel):
    #{{{
        return_code, _ = self._validate(user, channel)
        # RC=4, RC=5 and RC=6 imply bad channel
        if return_code > 4:
            return self.BAD_CHANNEL_MSG
        # RC=0 means good channel and valid id in the bank
        elif return_code == 0:
            return ("You are already a member of this bank :duck:"
                    "\n" + self.checkbux(user))
        # RC=2 means valid user not in bank
        elif return_code == 2:
            self.bank.addUser(user)
            return ("You have been added to the bank :duck:"
                    "\n" + self.checkbux(user))
        # Illegal user id somehow
        else:
            #TODO: Add error code for malformed user id
            return None
    #}}}

    # Check a user's bank balance
    # Params: user   - user id requesting balance
    #         target - (maybe) user id str to get balance of
    #                  default None gets user balance
    # Return: Message contains users balance
    def checkbux(self, user, target = None):
    #{{{
        # There's text to check for a target
        if target:
            return_code, target = self._validate(target)
            # User and in the bank
            if return_code == 0:
                balance = self.bank.balance(target)
                return ("<@" + target + "> currently has"
                        " " + str(balance) + " " + self.CURRENCY)
            # User not in the bank
            elif return_code == 2:
                return "<@" + target + "> is not currently registered for this bank :duck:"

        # Either there was no text for a target or the text wasn't a user
        return_code, _ = self._validate(user)
        # User in the bank
        if return_code == 0:
            balance = self.bank.balance(user)
            return ("You currently have"
                    " " + str(balance) + " " + self.CURRENCY)
        # Or not
        elif return_code == 2:
            return "You are not currently registered for this bank :duck:"
        # Illegal user id
        else:
            # TODO: Malformed user id code
            return None

    #}}}

    # Bet bucks on a game to win more
    # Params: user    - user id of player
    #         channel - channel id playing from
    #         bet_ops - bet options (amount, game, game_ops)
    # Return: Message containing results
    def bet(self, user, channel, bet_ops):
    #{{{
        # See if betting even allowed
        return_code, _ = self._validate(user, channel)
        # RC=4, RC=5 and RC=6 imply bad channel
        if return_code > 4:
            return self.BAD_CHANNEL_MSG
        # RC=2 is just not a member
        elif return_code == 2:
            return ("You are not a member of the bank.\n"
                    "Please use the JOIN command to use gambling features :duck:")
        elif return_code != 0:
            # TODO: Malformed user id
            return None

        # Check parameters
        return_code, bet_ops = self._parseBetOps(bet_ops)
        # RC=1, missing parameters
        if return_code == 1:
            return ("Missing required parameters for BET command.\n"
                   "Please use HELP BET for what is needed :duck:")
        # RC=2, bad bet amount
        elif return_code == 2:
            return ("Invalid betting amount: " + bet_ops)
        # RC=3, bad game type
        elif return_code == 3:
            return ("Invalid game type: " + bet_ops)

        amount, game, game_ops = bet_ops
        # Check bank balance
        if self.bank.balance(user) < amount:
            return ("Your balance is too low to make this bet"
                   "\n" + self.checkbux(user))

        return_code, response = self.GAMES[game](game_ops)
        # Lost
        if return_code == 0:
            self.bank.balance(user, -amount)
            return (response + "\nYou lost! You're down"
                   " " + str(amount) + " " + self.CURRENCY + " "
                   "\n" + self.checkbux(user))
        # Won
        elif return_code == 1:
            self.bank.balance(user, amount)
            return (response + "\nYou won! You've gained"
                   " " + str(2*amount) + " " + self.CURRENCY + " "
                   "\n" + self.checkbux(user))
        # Option error
        else:
            return "Game option error: " + response
    #}}}

    # Buy a gacha pull
    # Params: user    - uid of player
    #         channel - channel id playing from
    #         amount  - number of pulls to do
    # Return: Message containing results
    def pull(self, user, channel, amount):
    #{{{
        return_code, _ = self._validate(user, channel)
        # RC=4, RC=5 and RC=6 imply bad channel
        if return_code > 4:
            return self.BAD_CHANNEL_MSG
        # RC=2 is not a member
        elif return_code == 2:
            return ("You are not a member of the bank.\n"
                    "Please use the JOIN command to use gambling features :duck:")
        elif return_code != 0:
            #TODO: Malformed user id
            return None

        # Check amount
        if amount:
            # Number?
            try:
                amount = int(amount)
            # Emoji?
            except ValueError:
                amount = util.EMOJI_ROLLS.get(amount,1)
        else:
            amount = 1

        if amount in self.PULL_RANGE:
            # Check for free pull
            if self.bank.freePull(user):
                amount -= 1
                roll = util.doRolls(1000)[0]
                for key in self.GACHA_RANGES:
                    if roll in key:
                        pull = self.GACHA_RANGES[key]

        return None
    #}}}

    # Regen some bux when players are low (gets called every five minutes or so)
    # Params: None
    # Return: None
    def regenBux(self):
        self.bank.regen()

    # Check for required labels and add channel id if good
    # Params: channel - channel to potentially add
    #         lables  - label list to check
    # Return: None
    def checkChannel(self, channel, labels):
    #{{{
        channel_id   = channel["id"]
        channel_name = channel["name"]
        if (util.LABELS["GAMBLE"] in labels and
            channel_id not in self.approved_channels):
            self.approved_channels.append(channel_id)
            if util.debug:
                self.logger.log(DiagMessage("BOT0060D","Added","#"+channel_name))
        elif (util.LABELS["GAMBLE"] not in labels and
              channel_id in self.approved_channels):
            self.approved_channels.remove(channel_id)
            if util.debug:
                self.logger.log(DiagMessage("BOT0060D","Removed","#"+channel_name))
        else:
            if util.debug:
                self.logger.log(DiagMessage("BOT0060D","No change"))
    #}}}

    # Go through channel list and get add approved to list
    # Params: channels - dict of channels to channel data to check
    # Return: list of approved channel ids
    def _getApproved(self, channels):
    #{{{
        approved = []
        for key, channel in channels.items():
            if util.LABELS["GAMBLE"] in channel["labels"]:
                approved.append(channel["id"])
        return approved
    #}}}

    # Check if user and channel are appropriate for gambling
    # Params: user    - user id to check for bank entry
    #         channel - channel id to check for approval
    # Return: int value based on failures
    def _validate(self, user, channel = None):
    #{{{
        return_code = 0
        user = util.matchUserId(user)
        if not user:
            return_code += 1
        elif not self.bank.isMember(user):
            return_code += 2
        if channel and channel not in self.approved_channels:
            return_code += 4
        return return_code, user
    #}}}

    # Parse needed values out of bet options
    # Params: bet_ops - list of options to parse out
    # Return: return code and converted bet_ops list
    def _parseBetOps(self, bet_ops):
    #{{{
        # Check for missing options
        if len(bet_ops) < 2:
            return 1, None
        # Grab the options
        u_ops = [x.upper() for x in bet_ops]
        bet_amount, game, *game_ops = u_ops
        # Check bet amount
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            bet_amount = util.EMOJI_ROLLS.get(bet_amount,-1)
        if bet_amount < 1:
            return 2, bet_ops[0]
        # Check game
        if game not in self.GAMES:
            return 3, bet_ops[1]
        # Return everything
        return 0, [bet_amount, game, game_ops]
    #}}}

    # Get the seconds until next pull refresh
    # Params: None
    # Return: Seconds unil daily pulls refresh
    def _getRefreshTime(self):
    #{{{
        # Get current time
        current_time = datetime.now().replace(year = 1, month = 1, day = 1)
        # Send back diff
        return (self.REFRESH_TIME - current_time).seconds
    #}}}

    # Do the gacha pull
    # Params: None
    # Return: Result from gacha ranges
    def _doPull(self, user):
    #{{{
        roll = util.doRolls(1000)[0]
        # Nuke time
        if roll == 1:
            self.bank.nuke()
        # Lost one
        elif roll < 50:
            self.bank.
        for key in self.GACHA_RANGES:
            if roll in key:
                return self.GACHA_RANGES[key]
        return None
    #}}}
#}}}
