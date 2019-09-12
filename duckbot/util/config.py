import ast
from configparser import ConfigParser, ExtendedInterpolation

def parseBotConfig(args: dict) -> dict:
    r"""Parse config file for bot.

    Use the provided ``ConfigParser`` to gather bot configuration data
    and then massage the data into a valid format.

    Parameters
    ----------
    args
        Command line arguments
    parser
        ``ConfigParser`` instance to use

    Returns
    -------
    dict
        Bot configuration data
    """
    parser = ConfigParser(
            interpolation=ExtendedInterpolation(),
            allow_no_value=True
            )
    parser.optionxform = str
    parser.read(CONFPATH_BOT)
    # This will be expanded on when more options are added
    return _valueize(parser['clients'])


def _valueize(old: dict) -> dict:
    r"""Convert string values in a dictionary to other primitive types.

    Use ``ast.literal_eval()`` to safely parse string values in a dict
    into other primitive types, such as int and bool. If a value fails
    to be converted, it is left as is.

    Parameters
    ----------
    old
        Dictionary of values to convert

    Returns
    -------
    dict
        Dictionary of converted values

    Notes
    -----
    Does not recursively convert nested dictionaries
    """
    new = {}
    for key, value in old.items():
        try:
            new[key] = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            new[key] = value
    return new


