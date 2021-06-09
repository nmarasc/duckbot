# -*- coding: utf-8 -*-
r"""Duckbot fun fact generation.

Classes
-------
Fact
    Totally real and true fact generator
"""
import logging

import random
import re

from discord.ext import commands
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Fact(commands.Cog):
    r"""Totally real and true fact generator.

    Methods
    -------
    fact
        Fact command handler
    dbz
        Fact DBZ subcommand handler
    sponge
        Fact sponge subcommand handler
    """

    _DBZ_URL = 'https://dragonball.fandom.com/wiki/Special:Random'
    _SPONGE_URL = 'https://spongebob.fandom.com/wiki/Special:Random'

    @property
    def description(self):
        r"""Return cog description"""
        desc = ('A collection of commands related to fact provisioning.\n'
                'If you\'ve ever wanted to learn something new.')
        return desc

    @commands.group(
        help='Learn a totally new, real fact.',
        ignore_extra=True,
        aliases=['factoid']
    )
    async def fact(self, ctx):
        r"""Produce a fact.

        Parameters
        ----------
        ctx
            Command context information
        """
        if ctx.invoked_subcommand is None:
            subcommands = self.get_commands()[0].commands
            await random.choice(list(subcommands)).callback(self, ctx)

    @fact.command(
        help='Fun and canonical DBZ info.',
        ignore_extra=True,
        aliases=['canon', 'cooldbzfact', 'ssgssj4', 'zeno']
    )
    async def dbz(self, ctx):
        r"""Produce a DBZ fact.

        Parameters
        ----------
        ctx
            Command context information
        """
        await ctx.send(f'Did you know {self._getFact(self._DBZ_URL)}?')

    @fact.command(
        help='Fun sponge facts.',
        ignore_extra=True,
        aliases=['spongebob', 'bob']
    )
    async def sponge(self, ctx):
        r"""Produce a Spongebob fact.

        Parameters
        ----------
        ctx
            Command context information
        """
        await ctx.send(f'Did you know {self._getFact(self._SPONGE_URL)}?')

    def _getFact(self, url):
        r"""Retrieve a sentence of text from a fandom wiki.

        Parameters
        ----------
        url
            Address of fandom wiki to fetch text from

        Returns
        -------
        str
            Sentence from a random wiki
        """
        fact = ''
        badurls = ['disambiguation', 'List', 'gallery']
        while not fact:
            req = requests.get(url)
            if any(map(req.url.__contains__, badurls)):
                logger.info(f'Bad url: {req.url}')
                continue
            soup = BeautifulSoup(req.content, 'html.parser')
            soup.aside.clear()
            div = soup.find('div', {'class': 'mw-parser-output'})
            for p in div.find_all('p', recursive=False):
                if p.find('b'):
                    fact = self._cleaner(p.text.strip())
                    break
        return fact

    def _cleaner(self, txt):
        r"""Clean wiki text and get first sentence.

        Parameters
        ----------
        txt
            Text to clean

        Returns
        -------
        str
            Cleaned text
        """
        txt = re.sub(r' \(.*?\)', '', txt)
        txt = re.sub(r'\[.*?\]', '', txt)
        txt = txt.split('.')[0]
        return txt
