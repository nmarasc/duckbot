# Last Updated: 2.3.0
# Python imports
from datetime import datetime
# Project imports
import util.common as util
from util.rangeDict import rangedict
from util.bank import Bank
import util.bankMessage as bank_msgs
import util.games as Games

# Gambling handler class
class GambleHandler:
    REFRESH_TIME = datetime(1,1,1,12)
    PULL_RANGE = range(1,11)
    PULL_COST  = 10
    #{{{ - Gacha ranges
GACHA_RANGES = rangedict({
     range(50,150)    : 0
    ,range(150,600)   : 1
    ,range(600,800)   : 2
    ,range(800,900)   : 3
    ,range(900,975)   : 4
    ,range(975,990)   : 5
    ,range(990,1000)  : 6
    ,range(1000,1001) : 7
})
    #}}}
    #{{{ - Gacha names
    GACHA_NAMES = [
         "Trash"
        ,"Common"
        ,"Uncommon"
        ,"Rare"
        ,"Super Rare"
        ,"Ultra Rare"
        ,"SS Ultra Secret Rare"
        ,"1000-chan"
    ]
    #}}}

    # Constructor for gamble hambler
    # Params: channels - list of channels to check for approved labels
    # Return: GambleHandler instance with approved channels added
    def __init__(self, channels):
    #{{{
        self.GAMES = Games.GAMES
        self.logger = util.logger
        self.approved_channels = self._getApproved(channels)
        self.bank = Bank()
        self.pull_timer = self._getRefreshTime()
    #}}}


    # Buy a gacha pull
    # Params: user    - uid of player
    #         channel - channel id playing from
    #         amount  - number of pulls to do
    # Return: Message containing results
    def pull(self, user, channel, amount):
    #{{{
        return_code, _ = self._checkGambleStatus(user, channel)
        # RC=4, RC=5 and RC=6 imply bad channel
        if return_code > 4:
            return self.BAD_CHANNEL_MSG
        # RC=2 is not a member
        elif return_code == 2:
            return bank_msgs.NOT_A_MEMBER
        elif return_code != 0:
            #TODO: Malformed user id
            # Need infrastructure for return codes with messages
            return None

        # Convert amount
        if amount:
            # Number?
            try:
                amount = int(amount)
            # Emoji?
            except ValueError:
                amount = util.EMOJI_ROLLS.get(amount,1)
        else:
            amount = 1
        # Check amount and total cost
        if amount not in self.PULL_RANGE:
            return (bank_msgs.PULL_RANGE + "\nAllowed range is from"
                " " + str(min(self.PULL_RANGE)) + " to"
                " " + str(max(self.PULL_RANGE)))

        response = ""
        # Check balance for free pull
        if (self.bank.hasFreePull(user) and
           (amount - 1) * self.PULL_COST <= self.bank.balance(user)):

            self.bank.balance(user, -((amount - 1) * self.PULL_COST))
            response += "Free pull was available, -1 pull cost\n"
            self.bank.setFreePull(False, user)
        # Check balance for no free pull
        elif (not self.bank.hasFreePull(user) and
             amount * self.PULL_COST <= self.bank.balance(user)):

            self.bank.balance(user, -(amount * self.PULL_COST))
        # Not enough funds
        else:
            return bank_msgs.INSUFFICIENT_FUNDS

        response += "Your pull results: "
        for i in range(0,amount):
            pull_id = self._doPull(user)
            # Nuked
            if pull_id == -2:
                self.bank.nuke()
                return bank_msgs.NUKE
            # Bad pull
            if pull_id == -1:
                pull_id = self.bank.removeBest(user)

                # Didn't have anything to lose
                if pull_id < 0:
                    response += bank_msgs.NO_LOSS

                else:
                    pull_name = self.GACHA_NAMES[pull_id]
                # Lost the big one
                    if pull_id == self.GACHA_RANGES[1000]:
                        response += (
                            "\nYou have diappointed " + pull_name + ". "
                            "She returns back to the pool"
                        )
                # Lost your best
                    else:
                        response += "\nYou lost a " + pull_name

            # Good pull
            else:
                pull_name = self.GACHA_NAMES[pull_id]
                result = self.bank.addPool(pull_id, user)
                if result:
                    if result == user:
                        response += "\nYou have received a " + pull_name
                    else:
                        response += ("\nYou have stolen a " + pull_name + " "
                                     "from <@" + result + ">")
                else:
                    response += "\nThere were no more " + pull_name

        # Send back results
        return response
    #}}}

    # Regen some bux when players are low (gets called every five minutes or so)
    # Params: None
    # Return: None
    def regenBux(self):
        self.bank.regen()

    # Reset players' daily pull
    # Params: None
    # Return: None
    def refreshPulls(self):
    #{{{
        self.pull_timer = self._getRefreshTime()
        self.bank.setFreePull(True)
    #}}}

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
