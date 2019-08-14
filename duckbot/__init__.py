# -*- coding: utf-8 -*-

# Python imports
import logging
from logging import NullHandler

# Project imports
from .__version__ import __title__, __description__, __url__
from .__version__ import __version__, __author__
from .__version__ import __author_email__, __license__
from .__version__ import __copyright__
# I don't know if I like this import
from .util import common

# Avoids "No handler found" warning when logging is not configured
logging.getLogger(__name__).addHandler(NullHandler())
