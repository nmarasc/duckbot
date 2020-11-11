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
    get_opening_note
        Returns help command opening note.
    """
    def __init__(self):
        r"""Duckbot help command initialization."""
        pager = Paginator(prefix='>>> :duck: Kweh!\n', suffix='')
        super().__init__(paginator=pager)

    def get_opening_note(self):
        r"""Returns help command opening note."""
        prefix = self.clean_prefix
        command = self.invoked_with
        return f'Use `{prefix}{command} [command]` for more detailed help'

    def get_command_signature(self, command):
        r"""Return signature for given command"""
        prefix = self.clean_prefix
        return f'`{prefix}{command.qualified_name} {command.signature}`'
