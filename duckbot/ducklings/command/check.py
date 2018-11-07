# Duckbot util modules
import util.moduleLoader as modloader
from util.common import matchUserID
from util.common import bank
# Duckbot extension modules
from ducklings.command.sub_check import balance
from ducklings.command.sub_check import collection

# Valid command names
NAMES = [
    'CHECK',
    ':HEAVY_CHECK_MARK:',
    ':WHITE_CHECK_MARK:',
    ':BALLOT_BOX_WITH_CHECK:'
]

# Valid subcommand names
SUBCOMMANDS = modloader.loadSubCommands('check')

# Command help message
HELP = (
    'Check bank statistics of users\n'
    f'Usage: <@{{id}}> {NAMES[0]} <subcommand> [target]\n'
    'List of currently supported subcommands: {}\n'
    'No target defaults to yourself :duck:'
)

# Perform bank statistic checks for users
# Params: user     - user id requesting a balance
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing argument text
# Return: String response from command
def handle(user, channel, cmd_args):
    # bux|pool [target]
    try:
        subcmd = SUBCOMMANDS.get(str.upper(cmd_args[0]), None)
        user = _checkUser(user, cmd_args[1])
        response = subcmd.check(user)
    except IndexError:  # No arguments or no target
        if not cmd_args:
            response = getHelp()
    except AttributeError:  # Invalid command
        response = None
    return response

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args=None):
    return HELP

# Determine eligibility of user id and get balance
# Params: user - user id to check
# Return: integer balance of user or None
def _checkUser(user, args):
    # Note: Channel is being omitted from this check since CHECKBUX
    #   command is valid in any channel, so the related return code
    #   does not need to be checked
    try:
        target = matchUserID(args[0])
        user = target if target else user
    except IndexError:
        target = None
    return not bank.checkEligible(user)
