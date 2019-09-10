# -*- coding: utf-8 -*-

# Python imports
import logging
from logging import NullHandler

# Project imports
from duckbot.__version__ import __title__, __description__, __url__
from duckbot.__version__ import __version__, __author__
from duckbot.__version__ import __author_email__, __license__
from duckbot.__version__ import __copyright__

# Avoids "No handler found" warning when logging is not configured
logging.getLogger(__name__).addHandler(NullHandler())
