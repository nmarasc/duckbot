# -*- coding: utf-8 -*-
r"""Data related to cogs and commands."""

from enum import Enum

__all__ = ['base_ratings', 'eightball_messages', 'gacha_names']

base_ratings = {
    1: ':clown:',
    13: ':ghost:',
    69: ':eggplant:',
    420: ':herb:'
}

eightball_messages = [
    'It is certain',
    'It is decidedly so',
    'Without a doubt',
    'Yes, definitely',
    'You may rely on it',
    'As I see it, yes',
    'Most likely',
    'Outlook good',
    'Yes',
    'Signs point to yes',
    'Reply hazy, try again',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again',
    "Don't count on it",
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Very doubtful'
]

Gacha = Enum(
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
gacha_names = [
    'Trash',
    'Common',
    'Uncommon',
    'Rare',
    'Super Rare',
    'Ultra Rare',
    'SS Ultra Secret Rare',
    '1000-chan'
]
