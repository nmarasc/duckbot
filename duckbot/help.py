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

    Parameters
    ----------
    emoji
        Emoji string to use as the help header

    Methods
    -------
    add_subcommand_formatting
        Formating for subcommand

    get_opening_note
        Returns help command opening note.

    get_command_signature
        Returns signature for the given command
    """
    def __init__(self, emoji):
        r"""Duckbot help command initialization."""
        pager = Paginator(prefix=f'>>> {emoji} Kweh!\n', suffix='')
        aliases = ['hep', 'halp', '?', ':question:', ':grey_question:']
        cmdattrs = {'name': 'help', 'aliases': aliases, 'help': 'Alright, smarty pants'}
        super().__init__(paginator=pager, command_attrs=cmdattrs)

    def add_subcommand_formatting(self, command):
        r"""Adds formatting information on a subcommand.

        Parameters
        ----------
        command
            Bot command to show information of
        """
        prefix = self.clean_prefix
        name = command.qualified_name
        if command.short_doc:
            fmt = f'`{prefix}{name}` \N{EN DASH} {command.short_doc}'
        else:
            fmt = f'`{prefix}{name}`'
        self.paginator.add_line(fmt)

    def get_opening_note(self):
        r"""Returns help command opening note."""
        prefix = self.clean_prefix
        command = self.invoked_with
        return f'Use `{prefix}{command} [command]` for more detailed help'

    def get_command_signature(self, command):
        r"""Return signature for given command

        Parameters
        ----------
        command
            Bot command to get signature of
        """
        prefix = self.clean_prefix
        return f'`{prefix}{command.qualified_name} {command.signature}`'
