# -*- coding: utf-8 -*-

# Python imports
import logging
from logging import NullHandler

# Project imports
from duckbot.__version__ import __title__, __description__, __url__
from duckbot.__version__ import __version__, __author__
from duckbot.__version__ import __author_email__, __license__
from duckbot.__version__ import __copyright__
# These imports will fail while setup.py is gathering the above information
# because the dependencies will not have been installed yet. There's
# probably a better way to handle this.
try:
    from duckbot.core import __doc__
    from duckbot.core import Duckbot
    from duckbot.core import EXIT_CODES
except ImportError:
    pass

# Avoids "No handler found" warning when logging is not configured
logging.getLogger(__name__).addHandler(NullHandler())
