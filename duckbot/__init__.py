# -*- coding: utf-8 -*-

import logging

from duckbot.__version__ import __title__, __description__, __url__
from duckbot.__version__ import __version__, __author__
from duckbot.__version__ import __author_email__, __license__
from duckbot.__version__ import __copyright__

from duckbot.core import __doc__
from duckbot.core import Duckbot

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Avoids "No handler found" warning when logging is not configured
logging.getLogger(__name__).addHandler(NullHandler())
