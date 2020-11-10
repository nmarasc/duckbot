# -*- coding: utf-8 -*-
r"""Duckbot help command module.

Classes
-------
DuckbotHelpCommand
    Custom extension of the discord HelpCommand
"""
import logging

from discord.ext.commands import MinimalHelpCommand
from discord.ext.commands import Paginator

logger = logging.getLogger(__name__)


class DuckbotHelpCommand(MinimalHelpCommand):
    r"""Custom discord HelpCommand extension.

    Methods
    -------
    get_ending_note
        Returns help command ending note.
    """
    def __init__(self):
        r"""Duckbot help command initialization."""
        pager = Paginator(prefix='>>> :duck: Kweh!', suffix='')
        super().__init__(paginator=pager)
