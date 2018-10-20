# Duckbot util modules
from util.common import roll

# Valid command names
NAMES = [
    'EIGHTBALL',
    '8BALL',
    ':8BALL:'
]

# Command help message
HELP = (
    "Shake the magic 8ball\n"
    "Usage: <@{id:s}> " + NAMES[0]
)

# Eightball response messages
MESSAGES = [
     "It is certain"
    ,"It is decidedly so"
    ,"Without a doubt"
    ,"Yes, definitely"
    ,"You may rely on it"
    ,"As I see it, yes"
    ,"Most likely"
    ,"Outlook good"
    ,"Yes"
    ,"Signs point to yes"
    ,"Reply hazy, try again"
    ,"Ask again later"
    ,"Better not tell you now"
    ,"Cannot predict now"
    ,"Concentrate and ask again"
    ,"Don't count on it"
    ,"My reply is no"
    ,"My sources say no"
    ,"Outlook not so good"
    ,"Very doubtful"
]

# Randomly select an eightball message
# Params: args - list of arguments, **unused**
# Return: String containing eightball message
def handle(args=None):
    result = roll(len(MESSAGES))
    return MESSAGES[result]
