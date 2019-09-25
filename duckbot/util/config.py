import yaml
from datetime import datetime

import ast
from configparser import ConfigParser, ExtendedInterpolation

def parseBotConfig(path: str) -> dict:
    r"""Parse config file for bot.

    Parameters
    ----------
    path
        Location of the bot config file

    Returns
    -------
    dict
        Bot configuration data
    """
    time_format = '%H:%M:%S'
    try:
        with open(path) as conf:
            config = yaml.safe_load(conf)
        time = datetime.strptime(config['wish_time'], time_format)
        config['wish_time'] = time
    except OSError:
        logger.error(f'Bot config not found: {path}')
    except AttributeError:
        config['wish_time'] = None
    except ValueError:
        logger.warning('Wish time is not in HH:MM:SS format')
        config['wish_time'] = None
    return config


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


