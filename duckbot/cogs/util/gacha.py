# -*- coding: utf-8 -*-
r"""Duckbot gacha management.

Classes
-------
Gacha
    Duckbot gacha pool management
"""
import logging

from enum import Enum

from duckbot.util import Rangedict

from . import roll

__all__ = ['Gacha']

logger = logging.getLogger(__name__)


class Gacha():
    r"""Duckbot gacha pool management.

    Attributes
    ----------
    NAMES
        Enum of gacha pull names
    RANGES
        Range values of gacha pulls

    Methods
    -------
    pull
        Do a gacha pull
    """

    NAMES = Enum(
        value='Gacha',
        names=[
            ('Trash', 0),
            ('Common', 1),
            ('Uncommon', 2),
            ('Rare', 3),
            ('Super Rare', 4),
            ('Ultra Rare', 5),
            ('SS Ultra Secret Rare', 6),
            ('1000-chan', 7)
        ]
    )
    RANGES = Rangedict({
        range(50, 150): 0,
        range(150, 600): 1,
        range(600, 800): 2,
        range(800, 900): 3,
        range(900, 975): 4,
        range(975, 990): 5,
        range(990, 1000): 6,
        range(1000, 1001): 7
    })
    MAX = max(max(RANGES, key=lambda key: max(key)))

    def __init__(self):
        self.pity = {}

    def pull(self):
        r"""Do a gacha pull.

        Returns
        -------
        int
            Value pulled
        """
        return roll(self.MAX)
