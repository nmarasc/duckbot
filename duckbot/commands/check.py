# -*- coding: utf-8 -*-
r"""CHECK command module."""

import logging

# Duckbot util modules
import duckbot.util.modloader as modloader
from duckbot.util.common import matchUserID
# from duckbot.util.common import bank

logger = logging.getLogger(__name__)

DISABLED = False

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
PURPOSE = 'Check bank statistics of users'
USAGE = (
    f'Usage: {{bot}} {NAMES[0]} <subcommand> [target]\n'
    f"Currently supported subcommands: {', '.join(SUBCOMMAND_NAMES)}\n"
    'No target defaults to yourself :duck:'
)

# Prebaked command responses
RESPONSES = {
    'BAD_SUB': f'{{}} is not a valid {NAMES[0]} subcommand',
    'NO_ARGS': f'No arguments provided',
    'NOT_A_MEMBER': (
        'User is not a member of the bank. :duck:'
    )
}

bank = None

# Perform bank statistic checks for users
# Params: user     - user id requesting a balance
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list containing argument text
# Return: String response from command
def handle(user, channel, args):
    target = None
    if len(args) > 1:  # Check for target user
        target = matchUserID(args[1])
        if target:
            user = target
    try:
        subcmd = SUBCOMMANDS.get(args[0].upper(), None)
        if bank.isMember(user):
            response = subcmd.check(user, target is not None, bank)
        # Note: Channel is being omitted from this check since CHECK
        #   commands are valid in any channel, so the related return
        #   code does not need to be checked for
        else:  # User not a member
            response = RESPONSES['NOT_A_MEMBER']
    except IndexError:  # No arguments given
        response = f"{RESPONSES['NO_ARGS']}\n{USAGE}"
    except AttributeError:  # Invalid subcommand
        response = f"{RESPONSES['BAD_SUB'].format(args[0])}\n{USAGE}"
        raise
    return response

# Retrieve command help message
# Params: args - help arguments
# Return: String help message
def getHelp(args):
    try:
        subcmd = SUBCOMMANDS.get(str.upper(args[0]), None)
        response = subcmd.getHelp()
    except IndexError:  # Empty argument list
        response = f'{PURPOSE}\n{USAGE}'
    except AttributeError:  # Invalid subcommand
        response = f"{RESPONSES['BAD_SUB'].format(args[0])}\n{USAGE}"
    return response
