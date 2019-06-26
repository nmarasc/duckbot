# Valid command names
NAMES = [
    'PULL'
]

# Command help variables
PURPOSE = 'Spend your bucks on gacha'
USAGE = (
    f'Usage: <@{{id}}> {NAMES[0]} [#-of-pulls]\n'
    f'Up to 10 pulls may be done at once :duck:'
)

# Module constants
PULL_RANGE = range(1, 11)
PULL_COST = 10
GACHA_RANGES = rangedict({
    range(50, 150): 0,
    range(150, 600): 1,
    range(600, 800): 2,
    range(800, 900): 3,
    range(900, 975): 4,
    range(975, 990): 5,
    range(990, 1000): 6,
    range(1000, 1001): 7
})
GACHA_NAMES = [
    'Trash',
    'Common',
    'Uncommon',
    'Rare',
    'Super Rare',
    'Ultra Rare',
    'SS Ultra Secret Rare',
    '1000-chan'
]

# Spend on gacha draws
# Params: user     - user id of player
#         channel  - channel id playing from
#         cmd_args - list containing argument text
# Return: String response from command
def handle(user, channel, cmd_args):
    # Parse out bet arguments
    amount = _parseBetArgs(cmd_args)
    # Check gambling eligibility and argument validity
    status = _checkStatus(user, channel)
    if status['return_code']:  # Some error with status check
        response = status
    else:  # No status error, time to pull
        response = _pull(user, amount)
    return response

# Retrieve command help message
# Params: args - help arguments
# Return: String help message
def getHelp(args):
    return f'{PURPOSE}\n{USAGE}'

# Buy a gacha pull
# Params: user    - uid of player
#         amount  - number of pulls to do
# Return: Message containing results
def _pull(user, amount):
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

# Parse argument string for pull arguments
# Params: args - list of options to parse out
# Return: parsed argument list
def _parsePullArgs(args):
    try:
        # $$$ I can't tell whether a user typed -1 or garbage text with
        #     this function, it may need to be changed later
        result = parseNum(args[0])
        # Just ignore the problem for now
        result = 1 if result == -1
    except IndexError:  # Empty args
        result = 1
    return result

# Check the eligibilty of user and channel for this command
# Params: user    - user id issuing command
#         channel - channel id command issued from
# Return: dict with return code and status message
def _checkStatus(user, channel):
    message = ''
    return_code = bank.checkEligible(user, channel)
    if return_code == 1:  # Not a member
        message = bank.ERROR['NOT_A_MEMBER'].format(user)
    elif return_code == 2:  # Bad channel
        message = bank.ERROR['BAD_CHANNEL'].format(channel)
    return {'return_code': return_code, 'message': message}
