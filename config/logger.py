# -*- coding: utf-8 -*-
"""Logging config file.

Contains logging configuration dictionary as well as default values for
the log directory and filenames.
"""
# Python imports
import os

# By default the logs are kept in a .log directory at the root of the
# project, assuming the directory structure hasn't changed. It may be
# smarter to keep the logs in a known location like /tmp instead.
_CONF_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_CONF_DIR)

DEFAULT_LOG_DIR = '.log'
DEFAULT_LOG_FN = 'output.log'
DEFAULT_LOG_PATH = os.path.join(
    _ROOT_DIR,
    DEFAULT_LOG_DIR,
    DEFAULT_LOG_FN
)

# This is the dict that gets passed to logging.config.dictConfig() in
# the startup script.
loggerConfigDict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format':
                '%(asctime)s [%(levelname)8s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        # The default logging handler doesn't include DEBUG level
        # messages and prints to a log file instead of the console.
        # This can be changed with the command line flags.
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DEFAULT_LOG_PATH,
            'mode': 'a',
            'maxbytes': 10485760,  # 10MB log files
            'backupCount': 5
        },
    },
    # The root logger can be configured here or in 'loggers' below,
    # this felt more clear and the 'root' keyword takes precedence
    # should both be defined.
    'root': {
        'handlers': ['default'],
        'level': 'INFO'
    },
    'loggers': {
    }
}
