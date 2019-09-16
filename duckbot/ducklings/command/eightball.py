# Duckbot util modules
from duckbot.util.common import roll

# Valid command names
NAMES = [
    'EIGHTBALL',
    '8BALL',
    ':8BALL:'
]

# Command help variables
PURPOSE = 'Shake the magic 8ball'
USAGE = f'Usage: <@{{id}}> {NAMES[0]}'

# Eightball response messages
MESSAGES = [
     'It is certain'
    ,'It is decidedly so'
    ,'Without a doubt'
    ,'Yes, definitely'
    ,'You may rely on it'
    ,'As I see it, yes'
    ,'Most likely'
    ,'Outlook good'
    ,'Yes'
    ,'Signs point to yes'
    ,'Reply hazy, try again'
    ,'Ask again later'
    ,'Better not tell you now'
    ,'Cannot predict now'
    ,'Concentrate and ask again'
    ,"Don't count on it"
    ,'My reply is no'
    ,'My sources say no'
    ,'Outlook not so good'
    ,'Very doubtful'
]

# Randomly select an eightball message
# Params: user     - user id issuing command, **unused**
#         channel  - channel id command was issued from, **unused**
#         cmd_args - list of command arguments, **unused**
# Return: String containing eightball message
def handle(user, channel, cmd_args):
    result = roll(len(MESSAGES))
    return MESSAGES[result-1]

# Retrieve command help message
# Params: args - help arguments, **unused**
# Return: String help message
def getHelp(args):
    return f'{PURPOSE}\n{USAGE}'
