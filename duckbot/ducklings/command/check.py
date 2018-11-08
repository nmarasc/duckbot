# Duckbot util modules
import util.moduleLoader as modloader
from util.common import matchUserID
# from util.common import bank

# Valid command names
NAMES = [
    'CHECK',
    ':HEAVY_CHECK_MARK:',
    ':WHITE_CHECK_MARK:',
    ':BALLOT_BOX_WITH_CHECK:'
]

# Subcommand modules for check
SUBCOMMANDS = modloader.loadSubCommands('check')
SUBCOMMAND_NAMES = list({SUBCOMMANDS[key].NAMES[0] for key in SUBCOMMANDS})

# Command help variables
PURPOSE = 'Check bank statistics of users\n'
USAGE = (
    f'Usage: <@{{id}}> {NAMES[0]} <subcommand> [target]\n'
    f"Currently supported subcommands: {', '.join(SUBCOMMAND_NAMES)}\n"
    'No target defaults to yourself :duck:'
)
HELP = f'{PURPOSE}{USAGE}'

# Prebaked command responses
RESPONSES = {
    'BAD_SUB': f'{{}} is not a valid {NAMES[0]} subcommand\n{{}}',
    'NO_ARGS': f'No arguments provided\n{USAGE}'
}

# Perform bank statistic checks for users
# Params: user     - user id requesting a balance
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing argument text
# Return: String response from command
def handle(user, channel, cmd_args):
    if len(cmd_args) > 1:  # Check for target user
        target = matchUserID(cmd_args[1])
        if target:
            user = target
    try:
        subcmd = SUBCOMMANDS.get(str.upper(cmd_args[0]), None)
        if bank.checkEligible(user) == 0:  # OK return code
            response = subcmd.check(user)
        # Note: Channel is being omitted from this check since CHECK
        #   commands are valid in any channel, so the related return
        #   code does not need to be checked for
        else:  # User not a member
            response = bank.ERROR['NOT_A_MEMBER'].format(user)
    except IndexError:  # No arguments given
        response = RESPONSES['NO_ARGS']
    except AttributeError:  # Invalid subcommand
        response = RESPONSES['BAD_SUB'].format(args[0], USAGE)
    return response

# Retrieve command help message
# Params: args - help arguments
# Return: String help message
def getHelp(args):
    try:
        subcmd = SUBCOMMANDS.get(str.upper(args[0]), None)
        response = subcmd.getHelp()
    except IndexError:  # Empty argument list
        response = HELP
    except AttributeError:  # Invalid subcommand
        response = RESPONSES['BAD_SUB'].format(args[0], USAGE)
    return response
