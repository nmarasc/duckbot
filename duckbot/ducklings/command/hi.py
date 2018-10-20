# Valid command names
NAMES = [
    "HI",
    "HELLO"
]

# Command help message
HELP = "Legacy HI command\nUsage: <@{id:s}> " + NAMES[0]

# Say hello
# Params: args - list of arguments, **unused**
# Return: String containing command response
def handle(args):
    return "Kweh! :DUCK:"
