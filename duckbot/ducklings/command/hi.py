# Valid command names
NAMES = [
    "HI",
    "HELLO"
]

# Command help message
HELP = (
    "Legacy HI command\n"
    "Usage: <@{id:s}> " + NAMES[0]
)

# Say hello
# Params: args - list of arguments, **unused**
# Return: String containing command response
def handle(args):
    return "Kweh! :DUCK:"

# Retrieve command help message
# Params: ops - help options, **unused**
# Return: String help message
def getHelp(ops):
    return HELP
